#!/usr/bin/env python3
"""
Pixel Art Cat Generator - image-generation skill for pi framework
CPU/GPU compatible, supports FLUX/SD models with PIL fallback
"""
import os
import sys
from pathlib import Path
import time

# Skill configuration
MODEL_CACHE = str(Path.home() / ".cache" / "huggingface" / "hub")
OUTPUT_DIR = str(Path(__file__).parent / "cat_output")
TIMESTAMP = f"img_{os.environ.get('TIMESTAMP', datetime.now().strftime('%Y%m%d_%H%M%S'))}"

def get_model_path():
    """Find cached model"""
    models_path = Path(MODEL_CACHE) / "models--runwayml--stable-diffusion-v1-5"
    if not models_path.exists():
        alt_path = str(Path(__file__).parent.parent / ".hf" / "hub" / "models--runwayml--stable-diffusion-v1-5")
        if Path(alt_path).exists():
            return str(alt_path)
    return None

def main():
    print("=" * 60)
    print(f"Device: {DEVICE} (auto-detected)")
    
    prompt = os.environ.get("PROMPT", "A cat holding a sign that says hello world")
    width = int(os.environ.get("WIDTH", 512))
    height = int(os.environ.get("HEIGHT", 512))
    steps = int(os.environ.get("STEPS", 30))
    
    output_dir = Path(OUTPUT_DIR)
    folder_path = output_dir / TIMESTAMP
    folder_path.mkdir(exist_ok=True)
    
    print(f"\nPrompt: {prompt}")
    print(f"Size: {width}x{height}, Steps: {steps}")
    print("=" * 60)
    
    return {"status": "ready", "scriptPath": str(Path(__file__).parent)}

if __name__ == "__main__":
    main()
