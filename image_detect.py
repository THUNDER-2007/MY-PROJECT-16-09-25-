from PIL import Image, ImageChops, ImageEnhance
import exifread
import numpy as np
import os

# ----------- ELA CHECK -----------
def ela_check(image_path, save_path='ela_result.png', quality=90):
    """
    Perform Error Level Analysis on an image.
    Returns the ELA image.
    """
    original = Image.open(image_path).convert('RGB')
    
    # Save compressed version
    temp_path = "temp_ela.jpg"
    original.save(temp_path, 'JPEG', quality=quality)
    compressed = Image.open(temp_path)
    
    # Calculate the difference
    diff = ImageChops.difference(original, compressed)
    
    # Enhance the difference
    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    diff = ImageEnhance.Brightness(diff).enhance(scale)
    
    # Save and return
    diff.save(save_path)
    os.remove(temp_path)
    return diff

# ----------- EXIF CHECK -----------
def exif_check(image_path):
    """
    Check EXIF metadata of an image.
    Returns a dictionary of metadata.
    """
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    
    metadata = {}
    for tag in tags.keys():
        metadata[tag] = str(tags[tag])
    
    return metadata

# ----------- IMAGE ANALYSIS -----------
def analyze_image(image_path):
    print(f"Analyzing image: {image_path}\n")
    
    # ELA
    print("Performing Error Level Analysis...")
    ela_image = ela_check(image_path)
    ela_image.show()  # This opens the ELA image
    print("ELA image generated. Look for unusual artifacts (high contrast regions may indicate editing).\n")
    
    # EXIF
    print("Checking EXIF metadata...")
    metadata = exif_check(image_path)
    
    if not metadata:
        print("No EXIF metadata found. This can be suspicious for some images.\n")
    else:
        for key, value in metadata.items():
            print(f"{key}: {value}")
        print("\nCheck for missing camera info, inconsistent timestamps, or editing software.\n")
    
    print("Analysis complete. Note: This is a heuristic method, not 100% accurate.")

# ----------- MAIN -----------
if __name__ == "__main__":
    image_path = input("Enter the path of the image to check: ")
    
    if os.path.exists(image_path):
        analyze_image(image_path)
    else:
        print("File not found! Please check the path.")
