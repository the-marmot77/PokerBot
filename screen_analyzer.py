import cv2
import numpy as np
import pyautogui

# Define the region to capture (x, y, width, height)
CARD_REGION = (1200, 980, 200, 120)  # Example region for both cards
CARD_SPLIT_X = 1275  # Midpoint to split the region into two cards
COMMUNITY_REGION = (950, 670, 700, 125)  # Example region for community cards

# Approximate HSV color ranges for a 4-color deck
SUIT_HSV_RANGES = {
    "h": ([0, 100, 50], [10, 255, 255]),  # Hearts (Deep Red)
    "c": ([40, 50, 50], [90, 255, 255]),  # Clubs (Green)
    "d": ([100, 50, 50], [140, 255, 255]),  # Diamonds (Blue)
    "s": ([0, 0, 0], [180, 50, 70]),  # Spades (Black)
}

# Path to rank templates (Numbers/Letters)
RANK_TEMPLATES = {
    "a": "Cards/14.png",
    "k": "Cards/13.png",
    "q": "Cards/12.png",
    "j": "Cards/11.png",
    "10": "Cards/10.png",
    "9": "Cards/9.png",
    "8": "Cards/8.png",
    "7": "Cards/7.png",
    "6": "Cards/6.png",
    "5": "Cards/5.png",
    "4": "Cards/4.png",
    "3": "Cards/3.png",
    "2": "Cards/2.png",
}


def capture_region(region):
    """Capture the specified region of the screen and return it as a NumPy array."""
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def detect_suit_by_color(card_image, save_debug=False):
    """
    Detect the suit of a card based on its dominant color using HSV filtering.
    """
    height, width, _ = card_image.shape
    suit_region = card_image[
        int(height * 0.55) :, int(width * 0.30) : int(width * 0.70)
    ]  # Adjusted suit crop

    # Convert to HSV
    hsv = cv2.cvtColor(suit_region, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)  # Reduce noise

    detected_suit = None
    max_color_match = 0

    for suit, (lower, upper) in SUIT_HSV_RANGES.items():
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)
        color_match = np.sum(mask)  # Count matching pixels

        if color_match > max_color_match:
            max_color_match = color_match
            detected_suit = suit

    if save_debug:
        cv2.imwrite(f"suit_region_debug_{detected_suit}.png", suit_region)
        cv2.imwrite(f"suit_mask_debug_{detected_suit}.png", mask)

    return detected_suit


def match_template(image, template_path):
    """
    Perform template matching to identify a card rank.
    Returns:
        float: Confidence score of the best match.
    """
    template = cv2.imread(template_path, 0)  # Load template in grayscale
    gray_image = cv2.cvtColor(
        image, cv2.COLOR_BGR2GRAY
    )  # Convert card image to grayscale

    # Match template (TM_CCOEFF_NORMED gives best accuracy)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)  # Get best match confidence

    return max_val


def analyze_card(card_image, save_debug=False):
    """
    Analyze a single card image to detect its rank and suit.
    """
    detected_rank, detected_suit = None, None
    highest_rank_confidence = 0

    # Detect rank using template matching
    for label, template_path in RANK_TEMPLATES.items():
        confidence = match_template(card_image, template_path)
        if confidence > highest_rank_confidence:
            detected_rank = label
            highest_rank_confidence = confidence

    # Detect suit using color
    detected_suit = detect_suit_by_color(card_image, save_debug=save_debug)

    if save_debug:
        cv2.imwrite(f"card_debug_rank_{detected_rank}.png", card_image)

    return detected_rank, detected_suit


def analyze_region():
    """
    Analyze the captured region, splitting it into two cards and detecting ranks and suits.
    """
    image = capture_region(CARD_REGION)
    left_card = image[:, : CARD_SPLIT_X - CARD_REGION[0]]
    right_card = image[:, CARD_SPLIT_X - CARD_REGION[0] :]

    # Extract separate suit regions for each card
    left_rank, left_suit = analyze_card(left_card, save_debug=True)
    right_rank, right_suit = analyze_card(right_card, save_debug=True)

    return {"left": (left_rank, left_suit), "right": (right_rank, right_suit)}


def analyze_first_community_card(save_debug_image=False):
    """
    Detect and return the first community card from the board.
    """
    image = capture_region(COMMUNITY_REGION)

    # Assuming the first community card is in the leftmost part of COMMUNITY_REGION
    card_width = COMMUNITY_REGION[2] // 5  # Divide width into 5 equal parts
    first_card_region = image[:, :card_width]  # Crop the first card

    rank, suit = analyze_card(first_card_region, save_debug=save_debug_image)

    if rank and suit:
        return f"{rank}{suit}"
    return None
