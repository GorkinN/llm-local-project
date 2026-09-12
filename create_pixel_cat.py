from PIL import Image, ImageDraw

def draw_cute_pixel_cat():
    """Draw a simple pixel art cat using Pillow"""
    size = 64
    
    # Create white background
    img = Image.new('RGB', (size, size), 'white')
    
    # Draw body - rounded rectangle
    d = ImageDraw.Draw(img)
    d.ellipse([8, 32, 56, 58], fill='#d4a070')  # beige/pupur
        
    # Left ear triangle
    d.polygon([(16, 32), (16, 16), (28, 40)], fill='#4a2c2a')
    
    # Right ear triangle  
    d.polygon([(48, 32), (48, 16), (36, 40)], fill='#4a2c2a')
    
    # Draw eyes with pupils
    for eye_x in [24, 40]:
        d.ellipse([eye_x + 4, 42, eye_x + 16, 50], fill='white', outline='black')
        
        # Pupil
        d.ellipse([eye_x + 7, 44, eye_x + 13, 48], fill='black')
    
    # Nose - small pink triangle
    d.polygon([(32, 52), (28, 56), (36, 56)], fill='#ffb7c5')
    
    # Mouth - simple line
    d.line([30, 58, 34, 60], fill='black', width=1)
    
    save_path = "cat_pixel.png"
    img.save(save_path)
    import os
    print(f"[OK] Saved: {save_path} ({os.path.getsize(save_path)} bytes)")

if __name__ == "__main__":
    draw_cute_pixel_cat()
