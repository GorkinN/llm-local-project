#!/usr/bin/env python3
"""
Pixel Art Cat Generator - CPU/GPU Compatible (pi image-generation skill)
===============================================================================
Configurable via environment variables, runs in non-blocking mode
No GPU required - works on Windows 10 Home with only CPU available
===============================================================================

Usage:
  python final_image_gen.py           # Use defaults
  python final_image_gen.py MODEL=flux.../FLUX.1-dev fp16_cpu     # Use FLUX model
  python final_image_gen.py HEIGHT=512 WIDTH=512                   # Override resolution

Environment Variables:
  MODEL       - Model name (SD1.5 or FLUX)
  PROMPT      - Image prompt
  WIDTH       - Image width (default: 512)
  HEIGHT      - Image height (default: 512)
  STEPS       - Inference steps (default: 30)

Output: ./cat_output/cat_timestamp.png
"""

import os
import sys
from pathlib import Path
import time
from datetime import datetime

try:
    import torch
except ImportError:
    print("❌ PyTorch not installed!")
    print("Install with CPU-only: pip install torch -i https://download.pytorch.org/whl/cpu")
    sys.exit(1)

print("\n" + "=" * 60)
print(" Pixel Art Cat Generator (CPU/GPU Compatible)")
print("=" * 60)

# Auto-detect device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Device: {DEVICE}")

# Configuration from environment (non-blocking for skill framework)
MODEL_PATH = os.environ.get("MODEL", "runwayml/stable-diffusion-v1-5")
HEIGHT = int(os.environ.get("HEIGHT", 512))
WIDTH = int(os.environ.get("WIDTH", 512))
STEPS = int(os.environ.get("STEPS", 30))
PROMPT = os.environ.get("PROMPT", "small pixel art picture of a cute fluffy cat, 8bit style")

# Check cached models first
HUGGINGFACE_DIR = Path.home() / ".cache" / "huggingface" / "hub"
MODEL_CACHE = HUGGINGFACE_DIR / "models--runwayml--stable-diffusion-v1-5"
if not MODEL_CACHE.exists():
    print(f"\n⚠️  Cached model not found at: {MODEL_CACHE}")

print(f"\n📐 Image: {WIDTH}x{HEIGHT}px, Steps: {STEPS}")
print("=" * 60)

# Load pipeline with appropriate dtype for CPU/GPU
try:
    from diffusers import StableDiffusionPipeline, FluxPipeline
    
    if "FLUX" in MODEL_PATH.upper() or "flux" in MODEL_PATH.lower():
        print("\n🔄 Loading FLUX model...")
        pipe = FluxPipeline.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float16 if DEVICE == "cuda" else torch.bfloat16
        )
    else:
        print("\n🔄 Loading Stable Diffusion 1.5...")
        pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_PATH,
            torch_dtype=torch.float32 if DEVICE == "cpu" else torch.float16
        )
    
    if DEVICE == "cpu":
        print("⚙️  Optimizing for CPU-only execution")
        pipe.enable_model_cpu_offload()
    
    print(f"✅ Model loaded on {DEVICE}")
except Exception as e:
    print(f"\n❌ Failed to load model: {e}")
    sys.exit(1)

print("\n🎨 Generating pixel art...")
start_time = time.time()

# Generate images (non-blocking operation)
generator = torch.Generator(device).manual_seed(42)
images = pipe(PROMPT, width=WIDTH, height=HEIGHT, num_inference_steps=STEPS, generator=generator).images

end_time = time.time()
elapsed = end_time - start_time
print(f"✅ Generated {len(images)} image(s)")
print(f"⏱️  Time elapsed: {elapsed:.2f} seconds")

# Save output
OUTPUT_DIR = Path(__file__).parent / "cat_output"
OUTPUT_DIR.mkdir(exist_ok=True)

for idx, img in enumerate(images):
    path = OUTPUT_DIR / f"cat_{idx}.png"
    img.save(path)
    print(f"📁 Saved: {path}")

print("\n" + "=" * 60)
print("✅ Done! Check ./cat_output/ for generated images")
print("=" * 60)
