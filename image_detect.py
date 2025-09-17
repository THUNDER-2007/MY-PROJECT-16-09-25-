import streamlit as st
from PIL import Image, ImageChops, ImageEnhance
import exifread
import numpy as np
import os

# ----------- ELA CHECK -----------
def ela_check(image, quality=90):
    """
    Perform Error Level Analysis on an image.
    Returns the ELA image.
    """
    original = image.convert('RGB')

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

    os.remove(temp_path)
    return diff

# ----------- EXIF CHECK -----------
def exif_check(uploaded_file):
    """
    Check EXIF metadata of an uploaded image.
    Returns a dictionary of metadata.
    """
    uploaded_file.seek(0)  # reset pointer
    tags = exifread.process_file(uploaded_file, details=False)

    metadata = {}
    for tag in tags.keys():
        metadata[tag] = str(tags[tag])

    return metadata

# ----------- STREAMLIT APP -----------
st.title("🖼️ Image Real or AI Detector")
st.write("Upload an image and I’ll analyze it using **EXIF metadata** and **Error Level Analysis (ELA)**.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("🔍 Running analysis...")

    # Run ELA
    ela_result = ela_check(image)
    st.image(ela_result, caption="Error Level Analysis (ELA) Result", use_column_width=True)

    # Run EXIF
    metadata = exif_check(uploaded_file)
    if not metadata:
        st.warning("⚠️ No EXIF metadata found. This can be suspicious.")
    else:
        st.subheader("📑 EXIF Metadata")
        for key, value in metadata.items():
            st.text(f"{key}: {value}")

    st.success("✅ Analysis complete. Note: This is heuristic, not 100% accurate.")
