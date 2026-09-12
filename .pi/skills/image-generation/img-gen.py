# image-gen-skill/skill.py
"""
Image Generation Skill.

Локальная генерация изображений на GPU через FLUX.1-dev (diffusers).
Без HTTP, без Ollama — прямой вызов в процессе.

Публичное API:
    ImageSkill(verbose=False).generate(prompt, output_path=..., ...) -> list[GenerationResult]
    handle_generate_image(prompt, output_path=..., ...) -> dict   # для агента

Поведение по сохранению:
    - если output_path задан и это файл  → сохраняем ровно туда
    - если output_path задан и это папка → сохраняем в неё как variation_001.png, ...
    - если output_path не задан         → авто-папка в config.OUTPUT_DIR
"""

from __future__ import annotations

import sys
import time
import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import torch

sys.path.insert(0, str(Path(__file__).parent))
import config


# ─────────────────────────────────────────────────────────────
#  Результат
# ─────────────────────────────────────────────────────────────
@dataclass
class GenerationResult:
    prompt: str
    width: int
    height: int
    steps: int
    guidance: float
    seed: int
    path: str
    elapsed_sec: float
    file_size_mb: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ─────────────────────────────────────────────────────────────
#  Ошибки
# ─────────────────────────────────────────────────────────────
class SkillError(Exception):
    """Базовая ошибка скилла."""


class SkillValidationError(SkillError):
    """Неверные параметры вызова."""


class SkillRuntimeError(SkillError):
    """Ошибка во время генерации."""


# ─────────────────────────────────────────────────────────────
#  Скилл
# ─────────────────────────────────────────────────────────────
class ImageSkill:
    """
    Пайплайн кэшируется на уровне класса — повторные инстансы
    в одном процессе не перезагружают модель.
    """

    _pipe = None

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    # ---------- инфраструктура ----------
    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg, flush=True)

    def _ensure_gpu(self) -> None:
        if not torch.cuda.is_available():
            raise SkillRuntimeError("CUDA недоступна — скилл требует NVIDIA GPU.")
        if self.verbose:
            name = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / 1e9
            self._log(f"GPU: {name} ({vram:.1f} GB VRAM)")

    def _ensure_pipeline(self) -> None:
        if ImageSkill._pipe is not None:
            return

        self._ensure_gpu()

        try:
            from diffusers import FluxPipeline
        except ImportError as e:
            raise SkillRuntimeError(f"Не установлен diffusers: {e}") from e

        self._log(f"Загрузка {config.MODEL_ID}...")
        t0 = time.time()

        dtype = getattr(torch, config.TORCH_DTYPE, torch.bfloat16)
        try:
            pipe = FluxPipeline.from_pretrained(config.MODEL_ID, torch_dtype=dtype)
        except Exception as e:
            raise SkillRuntimeError(f"Не удалось загрузить модель: {e}") from e

        if config.ENABLE_ATTENTION_SLICING:
            pipe.enable_attention_slicing()

        if config.ENABLE_CPU_OFFLOAD:
            pipe.enable_model_cpu_offload()
        else:
            pipe.to("cuda")

        ImageSkill._pipe = pipe
        self._log(f"Модель готова за {time.time() - t0:.1f} сек")

    # ---------- валидация ----------
    @staticmethod
    def _validate(prompt: str, width: int, height: int,
                  steps: int, num_images: int, guidance: float) -> None:
        if not isinstance(prompt, str) or not prompt.strip():
            raise SkillValidationError("prompt обязателен и не может быть пустым")
        if not (config.MIN_DIM <= width <= config.MAX_DIM):
            raise SkillValidationError(
                f"width должен быть {config.MIN_DIM}..{config.MAX_DIM}, получено {width}"
            )
        if not (config.MIN_DIM <= height <= config.MAX_DIM):
            raise SkillValidationError(
                f"height должен быть {config.MIN_DIM}..{config.MAX_DIM}, получено {height}"
            )
        if not (1 <= steps <= config.MAX_STEPS):
            raise SkillValidationError(
                f"steps должен быть 1..{config.MAX_STEPS}, получено {steps}"
            )
        if not (1 <= num_images <= config.MAX_BATCH):
            raise SkillValidationError(
                f"num_images должен быть 1..{config.MAX_BATCH}, получено {num_images}"
            )
        if not (0.0 <= guidance <= 20.0):
            raise SkillValidationError(
                f"guidance должен быть 0..20, получено {guidance}"
            )

    # ---------- пути ----------
    @staticmethod
    def _resolve_targets(output_path: Optional[str | Path],
                         num_images: int) -> list[Path]:
        """
        Возвращает список конкретных файлов, куда сохранять изображения.

        Правила:
          - output_path = None            -> авто-папка (см. ниже), имена variation_NNN.png
          - output_path = путь к папке    -> внутри неё variation_NNN.png (или один файл, если num_images=1)
          - output_path = путь к файлу    -> если num_images=1, ровно этот файл;
                                             если num_images>1, тот же stem + _001.._NNN
        """
        if output_path is None:
            return []  # решается выше, в generate()

        p = Path(output_path)
        is_dir_hint = p.suffix == "" or p.is_dir()

        if is_dir_hint:
            p.mkdir(parents=True, exist_ok=True)
            if num_images == 1:
                return [p / "variation_001.png"]
            return [p / f"variation_{i+1:03d}.png" for i in range(num_images)]

        # путь к файлу
        p.parent.mkdir(parents=True, exist_ok=True)
        if num_images == 1:
            return [p]

        stem, suffix = p.stem, p.suffix or ".png"
        return [p.parent / f"{stem}_{i+1:03d}{suffix}" for i in range(num_images)]

    # ---------- основное API ----------
    def generate(
        self,
        prompt: str,
        width: int = config.DEFAULT_WIDTH,
        height: int = config.DEFAULT_HEIGHT,
        steps: int = config.DEFAULT_STEPS,
        guidance: float = config.DEFAULT_GUIDANCE,
        num_images: int = config.DEFAULT_NUM_IMAGES,
        seed: Optional[int] = None,
        output_path: Optional[str | Path] = None,
    ) -> list[GenerationResult]:
        """
        Сгенерировать изображения и сохранить их.

        output_path:
            - None                → авто-папка в config.OUTPUT_DIR
            - путь к папке        → туда, имена variation_NNN.png
            - путь к файлу        → ровно туда (при num_images=1)
        """
        self._validate(prompt, width, height, steps, num_images, guidance)
        self._ensure_pipeline()

        if seed is None:
            seed = int(time.time() * 1000) % (2**31)

        # Куда сохранять
        if output_path is None:
            batch_dir = self._make_batch_dir(config.OUTPUT_DIR, prompt)
            self._log(f"Папка: {batch_dir}")
            targets = [batch_dir / f"variation_{i+1:03d}.png" for i in range(num_images)]
        else:
            targets = self._resolve_targets(output_path, num_images)
            self._log(f"Сохранение в: {targets[0].parent}")

        results: list[GenerationResult] = []
        max_seq = 512 if max(width, height) >= 1024 else 256

        for i in range(num_images):
            current_seed = seed + i
            self._log(f"[{i+1}/{num_images}] {width}x{height}, "
                      f"{steps} steps, seed={current_seed}")

            t0 = time.time()
            try:
                generator = torch.Generator("cpu").manual_seed(current_seed)
                image = ImageSkill._pipe(
                    prompt=prompt,
                    height=height,
                    width=width,
                    guidance_scale=guidance,
                    num_inference_steps=steps,
                    max_sequence_length=max_seq,
                    generator=generator,
                ).images[0]
            except torch.cuda.OutOfMemoryError as e:
                torch.cuda.empty_cache()
                raise SkillRuntimeError(
                    f"CUDA OOM при {width}x{height}. Уменьши размер "
                    f"или включи ENABLE_CPU_OFFLOAD в config.py"
                ) from e
            except Exception as e:
                torch.cuda.empty_cache()
                raise SkillRuntimeError(f"Ошибка генерации: {e}") from e

            elapsed = time.time() - t0
            img_path = targets[i]
            img_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(img_path)
            size_mb = img_path.stat().st_size / 1024 / 1024

            results.append(GenerationResult(
                prompt=prompt,
                width=width, height=height,
                steps=steps, guidance=guidance,
                seed=current_seed,
                path=str(img_path),
                elapsed_sec=round(elapsed, 2),
                file_size_mb=round(size_mb, 3),
            ))
            self._log(f"  {img_path.name} ({size_mb:.1f} MB, {elapsed:.1f} сек)")

        # Метаданные — только если сохраняли в авто-папку
        if output_path is None:
            self._write_batch_meta(targets[0].parent, prompt, results)

        torch.cuda.empty_cache()
        return results

    # ---------- вспомогательное ----------
    @staticmethod
    def _make_batch_dir(base: Path, prompt: str) -> Path:
        base.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = "".join(
            c for c in prompt[:40] if c.isalnum() or c in " -_"
        ).strip().replace(" ", "_") or "image"
        h = hashlib.sha256(prompt.encode()).hexdigest()[:6]
        d = base / f"{ts}_{slug}_{h}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    @staticmethod
    def _write_batch_meta(batch_dir: Path, prompt: str,
                          results: list[GenerationResult]) -> None:
        meta = {
            "prompt": prompt,
            "model": config.MODEL_ID,
            "created": datetime.now().isoformat(),
            "images": [r.to_dict() for r in results],
        }
        (batch_dir / "metadata.json").write_text(
            json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
        )


# ─────────────────────────────────────────────────────────────
#  Точка входа для агента
# ─────────────────────────────────────────────────────────────
_SKILL_SINGLETON: Optional[ImageSkill] = None


def _get_skill() -> ImageSkill:
    global _SKILL_SINGLETON
    if _SKILL_SINGLETON is None:
        _SKILL_SINGLETON = ImageSkill(verbose=False)
    return _SKILL_SINGLETON


def handle_generate_image(
    prompt: str,
    output_path: str,
    width: int = config.DEFAULT_WIDTH,
    height: int = config.DEFAULT_HEIGHT,
    steps: int = config.DEFAULT_STEPS,
    guidance: float = config.DEFAULT_GUIDANCE,
    num_images: int = 1,
    seed: Optional[int] = None,
) -> dict[str, Any]:
    """
    Точка входа для агента. Никогда не бросает исключений.

    output_path — куда сохранить:
        - путь к файлу (.png/.jpg)   → ровно этот файл (при num_images=1)
        - путь к папке              → внутри неё variation_NNN.png

    Возвращает JSON-совместимый dict:
        {"ok": True,  "images": [{"path": ..., "seed": ..., ...}, ...]}
        {"ok": False, "error": "...", "error_type": "..."}
    """
    try:
        results = _get_skill().generate(
            prompt=prompt,
            width=int(width), height=int(height),
            steps=int(steps), guidance=float(guidance),
            num_images=int(num_images), seed=seed,
            output_path=output_path,
        )
    except SkillValidationError as e:
        return {"ok": False, "error": str(e), "error_type": "validation"}
    except SkillRuntimeError as e:
        return {"ok": False, "error": str(e), "error_type": "runtime"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "error_type": "unexpected"}

    return {
        "ok": True,
        "count": len(results),
        "images": [r.to_dict() for r in results],
    }


# ─────────────────────────────────────────────────────────────
#  Ручной запуск (только для отладки)
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Image Generation Skill — manual run")
    p.add_argument("prompt")
    p.add_argument("-o", "--output-path", required=True,
                   help="Путь к файлу или папке для сохранения")
    p.add_argument("-w", "--width", type=int, default=config.DEFAULT_WIDTH)
    p.add_argument("-H", "--height", type=int, default=config.DEFAULT_HEIGHT)
    p.add_argument("-s", "--steps", type=int, default=config.DEFAULT_STEPS)
    p.add_argument("-g", "--guidance", type=float, default=config.DEFAULT_GUIDANCE)
    p.add_argument("-n", "--num-images", type=int, default=1)
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    res = handle_generate_image(
        prompt=args.prompt,
        output_path=args.output_path,
        width=args.width, height=args.height,
        steps=args.steps, guidance=args.guidance,
        num_images=args.num_images, seed=args.seed,
    )
    print(json.dumps(res, indent=2, ensure_ascii=False))
    sys.exit(0 if res.get("ok") else 1)