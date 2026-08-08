import ssl
import easyocr

# Disable SSL verification for model downloading if needed
ssl._create_default_https_context = ssl._create_unverified_context

# Global variable to hold model in memory after first use
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        print("Lazy-loading EasyOCR reader...")
        _reader = easyocr.Reader(['en'], gpu=False)
    return _reader

def extract_text_from_image(image_path):
    """
    Extracts text from an image file using EasyOCR.
    """
    try:
        reader = get_reader()
        results = reader.readtext(image_path, detail=0)
        extracted_text = " ".join(results)
        return extracted_text.strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

if __name__ == "__main__":
    print("Testing EasyOCR engine...")
    reader = get_reader()
    print("EasyOCR engine loaded successfully!")