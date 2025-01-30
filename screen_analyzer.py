import pyautogui
import cv2
import numpy as np

# Define the region to capture (x, y, width, height)
CARD_REGION = (1200, 980, 200, 120)  # Example region for both cards
CARD_SPLIT_X = 1275  # Midpoint to split the region into two cards
COMMUNITY_REGION = (950, 670, 700, 125)  # Example region for community cards

# Path to your templates
TEMPLATES = {
    # Card Numbers
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
    # Suits
    "s": "Suits/Spade.png",
    "h": "Suits/Heart.png",
    "d": "Suits/Diamond.png",
    "c": "Suits/Club.png",
}

def capture_region(region):
    """
    Capture the specified region of the screen and return it as a NumPy array.
    Args:
        region (tuple): The (x, y, width, height) region to capture.
    Returns:
        numpy.ndarray: The captured region as a NumPy array.
    """
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def match_template(image, template_path):
    """
    Perform template matching to find the best match in the image.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val

def analyze_card(card_image):
    """
    Analyze a single card image to detect its rank and suit.
    """
    detected_rank, detected_suit = None, None
    highest_rank_confidence, highest_suit_confidence = 0, 0

    for label, template_path in TEMPLATES.items():
        confidence = match_template(card_image, template_path)
        if label in "akqj1098765432" and confidence > highest_rank_confidence:
            detected_rank = label
            highest_rank_confidence = confidence
        elif label in "shdc" and confidence > highest_suit_confidence:
            detected_suit = label
            highest_suit_confidence = confidence

    return detected_rank, detected_suit

def analyze_region():
    """
    Analyze the captured region, splitting it into two cards and detecting ranks and suits.
    """
    image = capture_region(CARD_REGION)
    left_card = image[:, :CARD_SPLIT_X - CARD_REGION[0]]
    right_card = image[:, CARD_SPLIT_X - CARD_REGION[0]:]

    left_rank, left_suit = analyze_card(left_card)
    right_rank, right_suit = analyze_card(right_card)

    return {"left": (left_rank, left_suit), "right": (right_rank, right_suit)}

def analyze_first_community_card(save_debug_image=False):
    """
    Analyze the community card region to detect the far-left card.
    Optionally save the processed screenshot for debugging.
    Returns:
        str: Detected community card in the format 'as', or None if not found.
    """
    # Capture the community card region
    image = capture_region(COMMUNITY_REGION)

    if save_debug_image:
        # Save the raw community region image for debugging
        cv2.imwrite("community_region_debug.png", image)

    # Define the subregion for the far-left card
    card_width = COMMUNITY_REGION[2] // 5  # Approximate width of one card
    first_card_image = image[:, :card_width]

    if save_debug_image:
        # Save the far-left card subregion image for debugging
        cv2.imwrite("first_card_debug.png", first_card_image)

    # Analyze the first card to detect rank and suit
    rank, suit = analyze_card(first_card_image)
    if rank and suit:
        return f"{rank}{suit}"
    return None

def is_card_contour(contour):
    """
    Determine if a contour corresponds to a card.
    Args:
        contour: Contour to analyze.
    Returns:
        bool: True if the contour corresponds to a card, False otherwise.
    """
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / h
    return 0.5 < aspect_ratio < 2.0 and w > 30 and h > 50  # Example thresholds
