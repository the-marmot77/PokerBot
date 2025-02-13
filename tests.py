import cv2
import numpy as np
import mss
import os

# Rank templates location (adjust if necessary)
RANK_TEMPLATE_PATH = "Cards"

# Debug folder for saving hole card screenshots
DEBUG_FOLDER = "debug_screenshots"
os.makedirs(DEBUG_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# Exact HSV color ranges for suits
SUIT_COLORS = {
    "h": ([0, 100, 50], [10, 255, 255]),  # Hearts (Deep Red)
    "c": ([40, 50, 50], [90, 255, 255]),  # Clubs (Green)
    "d": ([100, 50, 50], [140, 255, 255]),  # Diamonds (Blue)
    "s": ([0, 0, 0], [180, 50, 70]),  # Spades (Black)
}

# Card positions (adjust these coordinates based on your poker table layout)
CARD_POSITIONS = {
    "hole_1": (1228, 988, 44, 55),  # Player's first hole card
    "hole_2": (1276, 988, 44, 55),  # Player's second hole card
    "comm_1": (400, 400, 50, 80),  # First community card
    "comm_2": (480, 400, 50, 80),  # Second community card
    "comm_3": (560, 400, 50, 80),  # Third community card
    "comm_4": (640, 400, 50, 80),  # Fourth community card
    "comm_5": (720, 400, 50, 80),  # Fifth community card
}


# Capture screen
def capture_screen():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])  # Capture primary monitor
        return np.array(screenshot)


# Detect suit using HSV color filtering
def detect_suit(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    for suit, (lower, upper) in SUIT_COLORS.items():
        lower_bound = np.array(lower, dtype="uint8")
        upper_bound = np.array(upper, dtype="uint8")
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        if np.any(mask):  # If suit color is detected
            return suit

    return "?"  # Unknown suit


# Match rank template (from "Cards" folder, 2.png to 14.png)
def match_rank(image):
    best_match = None
    highest_confidence = 0

    for number in range(2, 15):  # 2 to 14 (Ace)
        template_path = os.path.join(RANK_TEMPLATE_PATH, f"{number}.png")
        if os.path.exists(template_path):
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            match_result = cv2.matchTemplate(
                cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), template, cv2.TM_CCOEFF_NORMED
            )
            _, max_val, _, _ = cv2.minMaxLoc(match_result)

            if max_val > highest_confidence:  # Update best match
                highest_confidence = max_val
                best_match = str(number)

    return best_match if highest_confidence > 0.7 else None


# Detect cards & save hole card screenshots
def detect_cards(screen):
    detected_cards = {}

    for name, (x, y, w, h) in CARD_POSITIONS.items():
        card_img = screen[y : y + h, x : x + w]  # Crop card area

        # Save screenshots of hole cards for debugging
        if name in ["hole_1", "hole_2"]:
            save_path = os.path.join(DEBUG_FOLDER, f"{name}.png")
            cv2.imwrite(save_path, card_img)
            print(f"Saved {name} screenshot: {save_path}")

        suit = detect_suit(card_img)
        rank = match_rank(card_img)

        if rank and suit:
            detected_cards[name] = f"{rank}{suit}"

    return detected_cards


# Main function
def main():
    screen = capture_screen()
    detected_cards = detect_cards(screen)

    if detected_cards:
        print("Detected Cards:")
        for position, card in detected_cards.items():
            print(f"{position}: {card}")
    else:
        print("No cards detected.")


if __name__ == "__main__":
    main()
