import os
import shutil
import cv2
import numpy as np
from PIL import Image
import pytesseract
import streamlit as st

st.set_page_config(page_title="AI Text Recognition", page_icon="🔍", layout="centered")

st.title("🔍 AI Text Recognition")
st.write("Extract text from images using OCR")

if shutil.which("tesseract") is None:
    default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path

uploaded_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    if image.mode != "RGB":
        image = image.convert("RGB")
    image_array = np.array(image)
    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, processed = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    try:
        text = pytesseract.image_to_string(processed)
        data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
        confidences = []
        for conf in data.get("conf", []):
            try:
                value = float(conf)
                if value >= 0:
                    confidences.append(value)
            except (ValueError, TypeError):
                pass
        confidence = sum(confidences) / len(confidences) if confidences else 0

        st.subheader("📝 Detected Text")
        if text.strip():
            st.text_area("OCR Result", text.strip(), height=200)
            st.metric("OCR Confidence", f"{confidence:.2f}%")
            st.download_button("⬇️ Download Text", text.strip(), file_name="extracted_text.txt", mime="text/plain")
        else:
            st.warning("No text detected in the image.")
    except pytesseract.TesseractNotFoundError:
        st.error("Tesseract executable not found. Install Tesseract OCR or configure its path.")

st.markdown("---")
st.subheader("ℹ️ About the Project")
st.write("This AI project uses Optical Character Recognition (OCR) to extract readable text from uploaded images.")
