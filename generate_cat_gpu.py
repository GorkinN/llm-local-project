import torch
from diffusers import FluxPipeline
from PIL import Image
import os

def generate_pixel_art_cat():
    """Generate pixel art cat image using GPU"""
    
    print("=" * 60)
    print("Pixel Art Cat Generator")
    print("=" * 60)
    
    # Check GPU
    if not torch.cuda.is_available():
        print("[x] GPU not found! Using CPU (slow)...")
        device = "cpu"
    else:
        device = "cuda"
        print("[OK] GPU detected:", torch.cuda.get_device_name(0))
        print("[INFO] VRAM:", torch.cuda.get_device_properties(0).total_memory / 1e9, "GB")
    
    # Load model
    print("\n[Info] Loading FLUX.1-dev model...")
    pipe = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32
    )
    
    if device == "cuda":
        pipe = pipe.to(device)
        pipe.enable_model_cpu_offload()
    
    print("[OK] Model loaded")
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), "cat_images")
    os.makedirs(output_dir, exist_ok=True)
    
    # Prompt for pixel art cat
    prompt = "small pixel art picture of a cute fluffy cat, vibrant colors, detailed"
    
    print("\n[Info] Generating:", prompt[:50] + "...")
    print("[Info] Size: 512x512")
    
    # Generate
    print("\n[Info] Generating... (this may take 3-5 minutes on CPU)")
    image = pipe(
        prompt,
        height=512,
        width=512,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=256,
    ).images[0]
    
    # Save
    output_path = os.path.join(output_dir, "pixel_art_cat.png")
    image.save(output_path)
    
    file_size = os.path.getsize(output_path) / 1024 / 1024
    
    print("\n[OK] DONE!")
    print("[Info] File:", output_path.split('\\')[-1])
    print("[Info] Size:", round(file_size, 2), "MB")
    
    return output_path

if __name__ == "__main__":
    try:
        result = generate_pixel_art_cat()
        print("\n[OK] Image ready:", result)
    except Exception as e:
        import traceback
        print("\n[Error]:", str(e)[:200])
        traceback.print_exc()
