import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os
import time

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Load pipeline
pipeline = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5"
)
pipeline = pipeline.to(device)

# Generate pixel art cat
prompt = "small pixel art picture of a cute fluffy cat, 8bit style, vibrant colors"
prompt = prompt.replace('"', '')  # Clean quotes

print(f"Generating: {prompt}")
start_time = time.time()
images = pipeline(prompt).images
end_time = time.time()

# Save images
for i, img in enumerate(images):
    output_path = f"cat_{i}.png"
    img.save(output_path)
    print(f"Saved: {output_path}")

print(f"Generation took {end_time - start_time:.2f} seconds")
