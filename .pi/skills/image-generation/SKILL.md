---
name: image-generation
description: Generate images directly using FLUX.1-dev (diffusers) on local GPU. Save generated images with prompts and metadata.
---

# Image Generation Skill

Directly generates images using Flux.1-dev via diffusers library, leveraging local NVIDIA GPU. No HTTP calls or Ollama required — pure Python execution within the process.

## When to use

Use this skill when:

- You need to generate images directly (not scripts) using diffusion models (Flux/SDXL/etc).
- You have an NVIDIA GPU and CUDA available.
- You want automatic saving with prompt-based folder organization or explicit file paths.
- You need metadata files alongside generated images.

## Input

JSON object with the following fields:

| Field         | Required | Default                         | Description                                                                                            |
| :------------ | :------- | :------------------------------ | :----------------------------------------------------------------------------------------------------- |
| `prompt`      | yes      | —                               | Text prompt describing the image to generate.                                                         |
| `output`      | optional | —                               | Path to save images (file or directory). If omitted, auto folder created in config.OUTPUT_DIR.         |
| `width`       | optional | 1024                           | Image width in pixels (must be within MIN_DIM..MAX_DIM per config).                                   |
| `height`      | optional | 768                            | Image height in pixels (must be within MIN_DIM..MAX_DIM per config).                                  |
| `steps`       | optional | 20                             | Number of diffusion steps (1..MAX_STEPS).                                                             |
| `guidance`    | optional | 7.5                            | Guidance scale (CF strength, 0..20).                                                                   |
| `num_images`  | optional | 1                              | Number of variations to generate (1..config.MAX_BATCH for this model).                                |
| `seed`        | optional | null                           | Random seed (null = auto-generated timestamp-based seed).                                             |

## Usage

```bash
# Generate a simple image, save to specified file
node .pi/skills/image-generation/ImageSkill.js '{"prompt": "A cat holding a sign that says hello", "output": "/path/to/cat.png"}'

# Generate multiple variations into a prompt-named folder
node .pi/skills/image-generation/ImageSkill.js '{"prompt": "Cyberpunk city street at night, neon lights", "num_images": 4}'

# Use custom dimensions and parameters
node .pi/skills/image-generation/ImageSkill.js '{"prompt": "Cozy forest cabin with warm fireplace in snow", "width": 896, "height": 768, "steps": 30}'
```

Accepts prompts like:

- `An astronaut riding a horse on Mars with golden hour lighting`
- `Cozy forest cabin with warm fireplace in snow, winter atmosphere`
- `Futuristic robot holding coffee cup, steaming steam, cinematic lighting`
- `Underwater coral reef scene with schools of tropical fish, vibrant colors`

## Output

### Success (script executed and images created)

```json
{
  "success": true,
  "count": 1,
  "images": [
    {
      "path": "/path/to/output/file.png",
      "width": 1024,
      "height": 768,
      "steps": 20,
      "guidance": 7.5,
      "seed": 3421567,
      "elapsed_sec": 8.4,
      "file_size_mb": 2.1
    }
  ]
}
```

When saving to an auto-created batch folder (output omitted or path without extension):

```json
{
  "success": true,
  "count": 4,
  "images": [
    {"path": "/config/OUTPUT_DIR/timestamp_slug_hash/variation_001.png", ...},
    {"path": "/config/OUTPUT_DIR/timestamp_slug_hash/variation_002.png", ...},
    {"path": "/config/OUTPUT_DIR/timestamp_slug_hash/variation_003.png", ...},
    {"path": "/config/OUTPUT_DIR/timestamp_slug_hash/variation_004.png", ...}
  ],
  "batch_folder": "/config/OUTPUT_DIR/timestamp_slug_hash"
}
```

### Validation error (wrong parameters)

```json
{
  "success": false,
  "error_type": "validation",
  "error": "width должен быть 64..2048, получено 5123"
}
```

### Runtime error (CUDA issues, model loading failures)

```json
{
  "success": false,
  "error_type": "runtime",
  "error": "CUDA недоступна — скилл требует NVIDIA GPU."
}
```

## Saving Behavior

| output_path                     | num_images | Result                                                                |
| :------------------------------ | :--------- | :-------------------------------------------------------------------- |
| `null` (omitted)               | N          | Auto batch folder in `config.OUTPUT_DIR` with `variation_NNN.png` + metadata.json |
| Directory path                 | N          | Inside directory, `variation_NNN.png` or single name if N=1           |
| File path `.png/.jpg` (N=1)    | 1          | Saves exactly to that path                                             |
| File path with stem (N>1)      | >1         | Same stem + `_001`, `_002`, ...                                        |

## Metadata

When generating in auto mode (no explicit file output), a `metadata.json` is saved in each batch folder:

```json
{
  "prompt": "A cat holding a sign",
  "model": "black-forest-labs/FLUX.1-dev",
  "created": "2024-01-15T14:32:10.425123",
  "images": [
    {
      "prompt": "...",
      "width": 1024,
      "height": 768,
      "steps": 20,
      "guidance": 7.5,
      "seed": 3421567,
      "path": "...",
      "elapsed_sec": 8.4,
      "file_size_mb": 2.1
    }
  ]
}
```

## Script Template Features

When generating image generation calls:

- ✅ Model loading via `FluxPipeline.from_pretrained()` from Hugging Face
- ✅ GPU/CPU auto-detection with CUDA check (`torch.cuda.is_available()`)
- ✅ Configurable dimensions (MIN_DIM..MAX_DIM)
- ✅ Adjustable inference steps and guidance scale
- ✅ Batch generation support (multiple variations per prompt)
- ✅ Manual seed control or auto-based on timestamp + hash slug
- ✅ Metadata JSON saving for batch operations
- ✅ Progress logging when verbose mode enabled
- ✅ Error handling: validation, OOM, model loading failures

## Notes

- Direct Python execution using `diffusers` library with FLUX.1-dev.
- Works on CUDA-enabled NVIDIA GPUs (check `torch.cuda.is_available()`).
- Default seed based on `int(time.time() * 1000) % (2**31)`.
- Batch folders name: `{YYYYMMDD_HHMMSS}_{slug[:40]}_{hash6}`.
- Maximum sequence length: 512 for high-res (>=1024px), else 256.
- Supports `enable_attention_slicing()` and `enable_model_cpu_offload()` if configured.
- If diffusers not available, script will fail with import error showing instructions.
