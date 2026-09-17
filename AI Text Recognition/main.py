import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
image_path = "Sample.png"
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not find or open '{image_path}'.")
else:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)
    confidences = []
    for conf in data["conf"]:
        try:
            value = float(conf)
            if value >= 0:
                confidences.append(value)
        except (ValueError, TypeError):
            pass
    average_confidence = sum(confidences) / len(confidences) if confidences else 0
    print("\nDetected Text:")
    print("-" * 30)
    print(text.strip())
    print("\nConfidence:")
    print(f"{average_confidence:.2f}%")
