#!/usr/bin/env python3
"""
Pixel Art Cat Generator - pi image-generation skill (CPU compatible)
Configurable via environment variables, no interactive prompts
"""
import sys
import os
from pathlib import Path
import time

try:
    import torch
except ImportError:
    print("PyTorch not installed!")
    print("Install: pip install torch -i https://download.pytorch.org/whl/cpu")
    sys.exit(1)

# Auto-detect device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {DEVICE}")

try:
    from diffusers import StableDiffusionPipeline
except ImportError as e:
    print(f"Missing package: {e}")
    sys.exit(1)

# Configuration from environment (non-blocking for skill framework)
MODEL_NAME = os.environ.get("MODEL", "runwayml/stable-diffusion-v1-5")
HEIGHT = int(os.environ.get("HEIGHT", 512))
WIDTH = int(os.environ.get("WIDTH", 512))
NUM_STEPS = int(os.environ.get("STEPS", 30))
PROMPT = os.environ.get("PROMPT", "small pixel art picture of a cute fluffy cat, 8bit style")

# Check cache first
CACHE_DIR = Path.home() / ".cache" / "huggingface" / "hub"
MODEL_PATH = CACHE_DIR / "models--runwayml--stable-diffusion-v1-5"
if not MODEL_PATH.exists():
    print(f"Cached model not found at: {MODEL_PATH}")

print("=" * 60)
print("Pixel Art Cat Generator")
print(f"Size: {WIDTH}x{HEIGHT}, Steps: {NUM_STEPS}")
print("=" * 60)

# Load model with CPU/GPU support
try:
    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
    )
    if DEVICE == "cpu":
        pipe.enable_model_cpu_offload()
    print("Model loaded")
except Exception as e:
    print(f"Failed to load model: {e}")
    sys.exit(1)

# Generate images
generator = torch.Generator(device).manual_seed(42)
images = pipe(PROMPT, width=WIDTH, height=HEIGHT, num_inference_steps=NUM_STEPS, generator=generator).images
print(f"Generated {len(images)} image(s)")

# Save outputs
OUTPUT_DIR = Path(__file__).parent / "cat_output"
OUTPUT_DIR.mkdir(exist_ok=True)

for idx, img in enumerate(images):
    path = OUTPUT_DIR / f"cat_{idx:03d}.png"
    img.save(path)
    print(f"Saved: {path}")

print("Done")
