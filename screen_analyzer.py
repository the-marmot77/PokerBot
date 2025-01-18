import pyautogui
from PIL import Image, ImageOps
import pytesseract

# Configure Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def capture_player_cards():
    """
    Capture the region where the player's cards are located and extract text.
    Returns:
        str: Extracted text representing the player's cards.
    """
    # Define the region for player's cards (x, y, width, height)
    left = 1200
    top = 980
    width = 200
    height = 120

    print(f"Capturing player cards from region: ({left}, {top}, {width}, {height})")
    # Capture a screenshot of the card region
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    
    # Save the raw region for debugging
    raw_image_path = "debug_raw_card_region.png"
    screenshot.save(raw_image_path)
    print(f"Raw screenshot saved to '{raw_image_path}' for verification.")
    
    # Preprocess the image
    processed_image = preprocess_image(screenshot)
    
    # Save the preprocessed region for debugging
    processed_image_path = "debug_preprocessed_card_region.png"
    processed_image.save(processed_image_path)
    print(f"Preprocessed screenshot saved to '{processed_image_path}' for verification.")
    
    # Use Tesseract to extract text
    print("Extracting text from the card region...")
    custom_config = r'-c tessedit_char_whitelist=AKQJ1098765432♠♥♦♣ --psm 6'
    card_text = pytesseract.image_to_string(processed_image, config=custom_config)
    
    return card_text.strip()

def preprocess_image(image):
    """
    Preprocess the image to enhance OCR accuracy.
    Args:
        image (Image): The PIL Image object to preprocess.
    Returns:
        Image: The preprocessed image.
    """
    print("Preprocessing the image...")
    # Convert to grayscale
    grayscale = ImageOps.grayscale(image)
    
    # Resize for better OCR (optional, doubles the size)
    resized = grayscale.resize((grayscale.width * 2, grayscale.height * 2), Image.Resampling.LANCZOS)
    
    # Apply binary thresholding
    processed = resized.point(lambda x: 0 if x < 128 else 255, '1')
    return processed

def main():
    # Capture and extract your cards
    player_cards = capture_player_cards()
    print(f"Your Cards: {player_cards}")

if __name__ == "__main__":
    main()
