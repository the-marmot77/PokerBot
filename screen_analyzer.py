import pyautogui
from PIL import Image
import os
import time

# Define a directory to save screenshots (temporary storage)
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def capture_screen(region=None):
    """
    Capture a screenshot of the screen or a specific region.
    
    Args:
        region (tuple): A 4-tuple (left, top, width, height) for the region to capture.
                        If None, captures the entire screen.
    
    Returns:
        Image: The captured screenshot as a PIL Image object.
    """
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

def save_and_delete_screenshot(image, filename="screenshot.png", delay=5):
    """
    Save a screenshot temporarily and then delete it after a delay.
    
    Args:
        image (Image): The PIL Image object to save.
        filename (str): The name of the file to save the image as.
        delay (int): The number of seconds to wait before deleting the file.
    """
    filepath = os.path.join(SCREENSHOT_DIR, filename)
    
    # Save the image
    image.save(filepath)
    print(f"Screenshot temporarily saved to {filepath}")

    # Wait before deleting
    print(f"Waiting {delay} seconds before deleting the screenshot...")
    time.sleep(delay)

    # Delete the file
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Screenshot deleted: {filepath}")
    else:
        print(f"Failed to delete {filepath}: File does not exist")

def main():
    # Capture the entire screen
    print("Capturing the entire screen...")
    full_screenshot = capture_screen()
    save_and_delete_screenshot(full_screenshot, "full_screenshot.png", delay=5)

    # Example: Capture a specific region (e.g., top-left corner of 300x300 pixels)
    region = (0, 0, 300, 300)
    print(f"Capturing a region: {region}")
    region_screenshot = capture_screen(region)
    save_and_delete_screenshot(region_screenshot, "region_screenshot.png", delay=5)

if __name__ == "__main__":
    main()
