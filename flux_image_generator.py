#!/usr/bin/env python3
"""
Flux Image Generator via Ollama API

A production-ready Python script for generating images using flux.1-dev
model through Ollama's /v1/image generation endpoints.

Usage:
    python flux_image_generator.py --prompt "your prompt here" [--width 512] [--height 512] [--num-imgs 1] [--steps 50] [--server-url http://localhost:11434]
"""

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class ImageGenerationException(Exception):
    """Custom exception for image generation errors."""

    def __init__(self, message: str, server_url: str = "", endpoint: str = ""):
        self.message = message
        self.server_url = server_url
        self.endpoint = endpoint
        super().__init__(f"[{server_url}] {endpoint}: {message}")


def load_config(path: str) -> Dict[str, Any]:
    """Load configuration from a YAML file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        Dictionary containing configuration values.

    Raises:
        FileNotFoundError: If config file does not exist.
        yaml.YAMLError: If the file contains invalid YAML.
    """
    import yaml

    with open(path, 'r') as f:
        return yaml.safe_load(f)


def validate_resolution(width: int, height: int) -> None:
    """Validate image resolution parameters.

    Args:
        width: Image width in pixels (512-2048).
        height: Image height in pixels (512-2048).

    Raises:
        ValueError: If dimensions are outside the valid range.
    """
    if not (512 <= width <= 2048):
        raise ValueError(f"Width must be between 512 and 2048, got {width}")
    if not (512 <= height <= 2048):
        raise ValueError(f"Height must be between 512 and 2048, got {height}")


def check_server_health(server_url: str) -> Optional[Dict[str, Any]]:
    """Check Ollama server health.

    Args:
        server_url: URL of the Ollama server.

    Returns:
        Health check information if available, None otherwise.

    Raises:
        ImageGenerationException: If server is unreachable or unhealthy.
    """
    import requests

    try:
        response = requests.get(f"{server_url}/v1/models", timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        raise ImageGenerationException(
            message=str(e),
            server_url=server_url,
            endpoint="/v1/models"
        )


def retry_api_call(func: callable, max_retries: int = 3, delay_seconds: float = 2.0) -> Any:
    """Execute a function with retry logic and exponential backoff.

    Args:
        func: The function to execute.
        max_retries: Maximum number of retry attempts.
        delay_seconds: Delay in seconds between retries (used for exponentiation).

    Returns:
        Result from successful function call.

    Raises:
        ImageGenerationException: If all retries are exhausted.
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except ImageGenerationException:
            raise
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                retry_delay = delay_seconds * (2 ** attempt)
                print(f"  Retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(retry_delay)
            else:
                raise ImageGenerationException(
                    message=f"All {max_retries} retries exhausted: {e}",
                    server_url="unknown",
                    endpoint="API endpoint"
                )
        except Exception as e:
            raise ImageGenerationException(message=str(e)) from e


def generate_single_image(prompt: str, width: int, height: int, 
                          steps: int, api_key: Optional[str] = None) -> bytes:
    """Generate a single image via Ollama API.

    Args:
        prompt: Text prompt for image generation.
        width: Image width in pixels.
        height: Image height in pixels.
        steps: Number of denoising steps.
        api_key: Optional API key from config.

    Returns:
        Image data as bytes.

    Raises:
        ImageGenerationException: If image generation fails.
    """
    import requests

    # Use Ollama's /api/generate endpoint for text-to-image models
    # Note: Flux via Ollama may use different endpoints depending on deployment
    payload = {
        "model": "flux1-dev",  # Or 'flux' or model name from Ollama
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "format": "JPEG",  # or specify PNG if supported
        "response_format": "binary"  # Return binary response (image data)
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}' if api_key else ''
    }

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",  # Standard Ollama endpoint for models like LLMs
            json=payload,
            headers=headers,
            timeout=60
        )
        
        if response.ok:
            # For some deployments, images may come as base64 or direct binary
            if isinstance(response.content, bytes):
                return response.content
        
        # If standard generation endpoint doesn't work for flux, try image-specific endpoints
        # Some Ollama setups have /api/generate with response_format=binary returning image
        # Fallback: might need to stream and capture base64 then decode

    except requests.exceptions.ConnectionError as e:
        raise ImageGenerationException(
            message="Cannot connect to Ollama server. Is it running?",
            server_url="http://localhost:11434"
        )
    except requests.exceptions.Timeout as e:
        raise ImageGenerationException(
            message=f"Request timed out ({e.timeout} seconds)",
            server_url="localhost:11434"
        )
    except requests.exceptions.HTTPError as e:
        error_msg = getattr(e.response, 'text', str(e))
        raise ImageGenerationException(
            message=f"API error {e.response.status_code}: {error_msg[:200]}",
            server_url="localhost:11434",
            endpoint="/api/generate",
            status_code=e.response.status_code
        )
    except Exception as e:
        raise ImageGenerationException(message=str(e)) from e


def save_with_metadata(image_bytes: bytes, prompt: str, width: int, 
                       height: int, steps: int, server_url: str) -> str:
    """Save generated image with metadata.

    Args:
        image_bytes: Raw image data as bytes.
        prompt: Original generation prompt.
        width: Image width.
        height: Image height.
        steps: Number of generation steps used.
        server_url: The server URL used for generation.

    Returns:
        Path to saved image file.
    """
    import os

    # Compute prompt hash for stable directory naming
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]

    # Create output directories
    os.makedirs('output/images', exist_ok=True)
    os.makedirs('output/logs', exist_ok=True)
    
    image_dir = f'output/images/{prompt_hash}'
    os.makedirs(image_dir, exist_ok=True)

    # Generate unique filename with UUID
    image_id = str(uuid.uuid4())
    image_file = f'{image_id}.png'
    image_path = os.path.join(image_dir, image_file)

    # Save image
    try:
        timestamp = datetime.now().isoformat()
        
        with open(image_path, 'wb') as f:
            f.write(image_bytes)

        file_size = os.path.getsize(image_path) if os.path.exists(image_path) else 0

        # Prepare and save metadata
        metadata = {
            "prompt": prompt[:500],  # Truncate very long prompts
            "width": width,
            "height": height,
            "steps": steps,
            "seed": None,  # Some models return seed, add when available
            "timestamp": timestamp,
            "file_size": file_size,
            "server_url": server_url,
            "model": "flux1-dev"
        }

        metadata_path = os.path.join(image_dir, f'{image_id}.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        return image_path

    except IOError as e:
        raise ImageGenerationException(
            message=f"Failed to save image file: {e}",
            server_url=server_url
        )


def generate_images(prompt: str, width: int, height: int, steps: int, 
                    num_images: int, api_key: Optional[str] = None,
                    server_url: str = "http://localhost:11434") -> List[str]:
    """Generate multiple images and save them.

    Args:
        prompt: Generation prompt.
        width: Image width.
        height: Image height.
        steps: Number of denoising steps.
        num_images: How many images to generate.
        api_key: Optional API key.
        server_url: Ollama server URL.

    Returns:
        List of saved image file paths.
    """
    # Use retry wrapper for each generation call
    def make_generation():
        return generate_single_image(prompt, width, height, steps, api_key)
    
    success = retry_api_call(lambda: retry_api_call(make_generation), 
                            max_retries=3)

    # Retry logic built into retry_api_call already wraps make_generation
    pass

    import tqdm

    saved_paths = []

    for i in tqdm.trange(1, num_images + 1, desc="Processing generation"):
        try:
            image_bytes = retry_api_call(make_generation)
            path = save_with_metadata(image_bytes, prompt, width, height, steps, server_url)
            saved_paths.append(path)
            print(f"  Generated and saved: {path[:80]}...")
        except ImageGenerationException as e:
            print(f"\n  ERROR at iteration {i}: {e}")
            print(f"  Failed images: {len(saved_paths)} of {num_images}")
            if len(saved_paths) < num_images:
                raise

    return saved_paths


def main() -> int:
    """Main entry point for the image generator."""
    import yaml

    parser = argparse.ArgumentParser(
        description='Generate images using Flux.1-dev model via Ollama API.',
        epilog='''
Examples:
  python flux_image_generator.py --prompt "a beautiful sunset over mountains"
  python flux_image_generator.py --prompt "cyberpunk city" --width 768 --height 768 --num-imgs 3 --steps 50
  python flux_image_generator.py --prompt "portrait of a cat" --config config.yaml
        '''
    )

    parser.add_argument(
        '--prompt', '-p', 
        required=True, 
        help='Text prompt for image generation'
    )
    parser.add_argument(
        '--width', '-w', 
        type=int, 
        default=512,
        help=f'Image width in pixels (512-2048), default: 512'
    )
    parser.add_argument(
        '--height', '-H', 
        type=int, 
        default=512,
        help=f'Image height in pixels (512-2048), default: 512'
    )
    parser.add_argument(
        '--num-imgs', '-n', 
        type=int, 
        default=1,
        help='Number of images to generate, default: 1'
    )
    parser.add_argument(
        '--steps', '-s', 
        type=int, 
        default=50,
        help='Number of denoising steps for image generation, default: 50'
    )
    parser.add_argument(
        '--server-url', '-u',
        default='http://localhost:11434',
        help='Ollama server URL (include port), default: http://localhost:11434'
    )
    parser.add_argument(
        '--config', '-c', 
        type=str, 
        default=None,
        help='Path to YAML configuration file'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='output',
        help='Base output directory (for images and logs), default: output'
    )

    args = parser.parse_args()

    # Prepare config dictionary
    config: Dict[str, Any] = {
        "ollama_server": args.server_url,
        "api_key": None,  # Use Bearer token if available
        "timeout": 60
    }

    # Load config file if provided
    if args.config and os.path.exists(args.config):
        try:
            loaded_config = load_config(args.config)
            for key, value in loaded_config.items():
                if isinstance(value, str) and not value.strip():
                    continue  # Skip empty values from YAML
                config[key] = value

        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"ERROR: Failed to load config file '{args.config}': {e}", file=sys.stderr)
            return 2

    # Validate parameters AFTER config loading
    try:
        validate_resolution(args.width, args.height)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    # Update server URL from config if it was there
    if "ollama_server" in config:
        args.server_url = config["ollama_server"]

    try:
        # Check server health
        print(f"Checking Ollama server at {args.server_url}...")
        server_info = check_server_health(args.server_url)
        print(f"  Server ready. Models available: {[m['model'] for m in server_info.get('models', [])]}")

    except ImageGenerationException as e:
        print(f"Server health check failed:\n  {e}", file=sys.stderr)
        return 1

    # Generate images with progress indicators
    try:
        output_dir = args.output_dir
        os.makedirs(output_dir, exist_ok=True)

        print(f"\nGenerating {args.num_images} image(s) for the following prompt:")
        preview = args.prompt[:60] + "..." if len(args.prompt) > 60 else args.prompt
        print(f"  '{preview}'")
        print(f"\nSettings: {args.width}x{args.height}, {args.steps} steps, {args.num_images} image(s)")

        # Generate and save images
        saved_paths = generate_images(
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            steps=args.steps,
            num_images=args.num_images,
            api_key=config.get("api_key"),
            server_url=args.server_url
        )

        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total images generated: {len(saved_paths)}")
        print(f"Successful: {len(saved_paths)}")
        print(f"Failed: 0")
        print("\nSaved images:")
        for path in saved_paths:
            file_size = os.path.getsize(path) if os.path.exists(path) else 0
            display_name = path.replace(output_dir + '/', "")[-80:]
            print(f'  -> {display_name} ({file_size:,} bytes)')

        print("\nDone!" if len(saved_paths) > 0 else "\nGeneration completed.")
        return 0

    except ImageGenerationException as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {type(e).__name__}: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main()
