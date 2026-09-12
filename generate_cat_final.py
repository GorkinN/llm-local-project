#!/usr/bin/env python3
"""
Pixel Art Cat Generator - CPU Compatible
Generates pixel-art style cat images using Stable Diffusion
"""
import sys
from pathlib import Path
import time
from datetime import datetime

try:
    import torch
except ImportError:
    print("Install PyTorch first:")
    print("  pip install torch -i https://download.pytorch.org/whl/cpu")
    sys.exit(1)

try:
    from diffusers import StableDiffusionPipeline
except ImportError:
    print("Install diffusers:")
    print("  pip install diffusers")
    sys.exit(1)


def main():
    # Configuration
    output_dir = Path(__file__).parent / "cat_images"
    prompt = "pixel art style cute fluffy cat, white background, simple clean lines, digital illustration"
    
    # CPU-only setup
    print("=" * 60)
    print("Pixel Art Cat Generator")
    print("=" * 60)
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    
    print(f"Device: {device}")
    print()
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Check HuggingFace cache first
    hub_cache = Path.home() / ".cache" / "huggingface" / "hub" / "models--black-forest-labs--FLUX.1-dev"
    
    if not hub_cache.exists():
        print("No cached FLUX model found...")
        print("Please check your ~/.cache/huggingface/ directory first.")
        print()
        print("Alternatively, download model manually or use:")
        print("  python -c 'from diffusers import FluxPipeline; p=FluxPipeline.from_pretrained(\"black-forest-labs/FLUX.1-dev\")'")
        sys.exit(1)
    
    # Try loading from cache with fallback options
    models_cache = Path(__file__).parent / ".cache" / "models--black-forest-labs--FLUX.1-dev"
    if not hub_cache.exists() and not models_cache.exists():
        print("No FLUX model found in HuggingFace cache.")
        print("Generating a simple pixel cat instead (no GPU needed)!")
        
        # Simple PIL-based fallback
        from PIL import Image
        size = 512
        
        img = Image.new('RGB', (size, size), 'white')
        cx, cy = size // 2, size // 2
        
        # Draw basic pixel cat shape using loops
        body_size = int(size * 0.6)
        
        # Left ear
        for x in range(cx - body_size // 2 - 20, cx - body_size // 4):
            for y in range(cy, cy + 15):
                img.putpixel((x, y), (80, 30, 30))
        
        # Right ear  
        for x in range(cx + body_size // 4 - 20, cx + body_size // 2 + 20 - 19):
            for y in range(cy, cy + 15):
                img.putpixel((x, y), (80, 30, 30))
        
        # Body/circle main shape
        for x in range(cx - body_size // 2, cx + body_size // 2):
            dist = abs(x - cx)
            if dist <= body_size // 2:
                y_start = cy - int((body_size / 2)**2 - dist**2)**0.5
                for y in range(y_start, min(cy + body_size // 2, size)):
                    img.putpixel((x, y), (139, 87, 60))
        
        # Eyes area
        eye_x_left = cx - body_size // 6
        eye_x_right = cx + body_size // 4
        
        for x in range(eye_x_left, min(eye_x_right + 20, size)):
            img.putpixel((x, cy - 8), (255, 255, 255))
        
        # Pupils
        img.putpixel((eye_x_left + 8, cy - 4), (0, 0, 0))
        img.putpixel((eye_x_right - 6, cy - 4), (0, 0, 0))
        
        # Save pixel fallback cat
        pixel_cat_path = output_dir / "pixel_fallback.png"
        img.save(pixel_cat_path)
        print(f"[OK] Created simple pixel cat: {pixel_cat_path}")
        return
    
    load_start = time.time()
    
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            "black-forest-labs/FLUX.1-dev",
            torch_dtype=torch.float32 if device == "cpu" else torch.bfloat16
        )
        
        if device == "cpu":
            pipe.enable_model_cpu_offload()
        
        print(f"Model loaded in {time.time() - load_start:.1f}s")
        print("=" * 60)
    
    except Exception as e:
        print(f"Model error: {e}")
        print("Using PIL fallback pixel cat...")
        from PIL import Image
        size = 512
        img = Image.new('RGB', (size, size), 'white')
        
        cx, cy = size // 2, size // 2
        
        # Draw pixel art style cat body and ears
        for x in range(size):
            for y in range(size):
                dist = abs(x - cx) / (abs(y - cy))
                
                if not dist or dist > 5:
                    continue
                
                # Cat head/body area
                if dist <= 4.5 and py := min(10, cy + abs(dist - 1)):
                    img.putpixel((x, y), (139, 87, 60))
        
        # Save fallback
        pixel_cat_path = output_dir / "fallback.png"
        img.save(pixel_cat_path)
        print(f"[OK] Fallback: {pixel_cat_path}")
        return

    num_steps = int(input("Number of inference steps (10-50, default=30): ") or 30)
    
    generator = torch.Generator(device).manual_seed(42)
    
    print(f"\nGenerating pixel-art cat...")
    start_time = time.time()
    
    image = pipe(
        prompt,
        num_inference_steps=num_steps,
        width=512,
        height=512,
        generator=generator,
    ).images[0]
    
    elapsed = time.time() - start_time
    
    save_path = output_dir / "pixel_art_cat.png"
    image.save(save_path)
    
    print("=" * 60)
    print(f"[OK] Saved: {save_path}")
    print(f"      Generated in {elapsed:.1f} seconds")
    print(f"      Size: {(save_path.stat().st_size / 1024):.1f} KB")
    print("=" * 60)


if __name__ == "__main__":
    main()
