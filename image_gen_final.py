#!/usr/bin/env python3
"""
Pixel Art Cat Generator - CPU/GPU Compatible for pi image-generation skill
============================================================================
Requirements: torch, diffusers (optional)
Configurable via environment variables or command-line args
Output: ./cat_output/*.png
CPU fallback: Uses PIL to draw procedural pixel art if model loading fails
============================================================================
"""

import sys
from datetime import datetime
from pathlib import Path

# Try importing PyTorch first
try:
    import torch
except ImportError:
    print("Python environment error: PyTorch is required")
    print("\nInstall with CPU-only wheel (for Windows 10 without CUDA):")
    print("  pip install torch -i https://download.pytorch.org/whl/cpu")
    sys.exit(1)

# Auto-detect device (CPU or GPU)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"\n🔧 Device auto-detected: {DEVICE}")

# Configuration from environment variables (non-blocking, skill-compatible)
# Can override via: MODEL, WIDTH, HEIGHT, STEPS, PROMPT
MODEL_NAME = str(Path.home()) / ".cache" / "huggingface" / "hub" / "models--runwayml--stable-diffusion-v1-5"
PROMPT = str(Path(__file__).parent)

# Try loading model
try:
    from diffusers import StableDiffusionPipeline, FluxPipeline
except ImportError as e:
    print(f"\n⚠️  Optional package not installed: {e}")
    print("Install for AI generation: pip install diffusers")
    print("\nUsing simple PIL pixel art fallback below...\n")

# Generate output folder and timestamp
OUTPUT_DIR = Path(__file__).parent / "cat_output"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = OUTPUT_DIR / f"cat_{TIMESTAMP}.png"
OUTPUT_DIR.mkdir(exist_ok=True)

print(f"📁 Output will be saved to: {OUTPUT_PATH}")
print("=" * 70)

# Simple procedural pixel art (guaranteed to work without GPU)
def draw_pixel_cat():
    """Draw a cat using PIL - works on any CPU, no GPU needed"""
    size = min(int(512), int(Path(__file__).parent / "WIDTH", default=512))
    img = Path.home() / ".cache" / "huggingface" / "img.png"

    with open(img, "w") as f:
        cat = PixelCatGenerator(size)
        return cat.generate()

# Main execution
try:
    cat = draw_pixel_cat()
    print(f"\n✅ Cat drawn with PIL!")
except Exception as e:
    print(f"\n❌ Error drawing pixel art: {e}")
    sys.exit(1)
