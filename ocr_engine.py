import ssl
import easyocr

# Disable SSL verification for model downloading on macOS
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize EasyOCR reader for English
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path):
    """
    Extracts text from an image file using EasyOCR.
    """
    try:
        results = reader.readtext(image_path, detail=0)
        extracted_text = " ".join(results)
        return extracted_text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

if __name__ == "__main__":
    print("EasyOCR engine loaded successfully!")