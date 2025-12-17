from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np
import pyautogui

BASE_DIR = Path(__file__).resolve().parent.parent
CARD_REGION = (1200, 980, 200, 120)
CARD_SPLIT_X = 1275
COMMUNITY_REGION = (950, 670, 700, 125)

SUIT_HSV_RANGES = {
    "h": ([0, 100, 50], [10, 255, 255]),
    "c": ([40, 50, 50], [90, 255, 255]),
    "d": ([100, 50, 50], [140, 255, 255]),
    "s": ([0, 0, 0], [180, 50, 70]),
}

RANK_TEMPLATES = {
    "a": BASE_DIR / "Cards" / "14.png",
    "k": BASE_DIR / "Cards" / "13.png",
    "q": BASE_DIR / "Cards" / "12.png",
    "j": BASE_DIR / "Cards" / "11.png",
    "10": BASE_DIR / "Cards" / "10.png",
    "9": BASE_DIR / "Cards" / "9.png",
    "8": BASE_DIR / "Cards" / "8.png",
    "7": BASE_DIR / "Cards" / "7.png",
    "6": BASE_DIR / "Cards" / "6.png",
    "5": BASE_DIR / "Cards" / "5.png",
    "4": BASE_DIR / "Cards" / "4.png",
    "3": BASE_DIR / "Cards" / "3.png",
    "2": BASE_DIR / "Cards" / "2.png",
}


def capture_region(region: Tuple[int, int, int, int]) -> np.ndarray:
    screenshot = pyautogui.screenshot(region=region)
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def detect_suit_by_color(card_image: np.ndarray, *, save_debug: bool = False) -> str | None:
    height, width, _ = card_image.shape
    suit_region = card_image[int(height * 0.55) :, int(width * 0.30) : int(width * 0.70)]

    hsv = cv2.cvtColor(suit_region, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    detected_suit = None
    max_color_match = 0
    mask = None

    for suit, (lower, upper) in SUIT_HSV_RANGES.items():
        lower_np = np.array(lower, dtype="uint8")
        upper_np = np.array(upper, dtype="uint8")
        candidate_mask = cv2.inRange(hsv, lower_np, upper_np)
        color_match = np.sum(candidate_mask)

        if color_match > max_color_match:
            max_color_match = color_match
            detected_suit = suit
            mask = candidate_mask

    if save_debug and detected_suit:
        cv2.imwrite(f"suit_region_debug_{detected_suit}.png", suit_region)
        if mask is not None:
            cv2.imwrite(f"suit_mask_debug_{detected_suit}.png", mask)

    return detected_suit


def match_template(image: np.ndarray, template_path: Path) -> float:
    template = cv2.imread(str(template_path), 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val


def analyze_card(card_image: np.ndarray, *, save_debug: bool = False) -> Tuple[str | None, str | None]:
    detected_rank, detected_suit = None, None
    highest_rank_confidence = 0.0

    for label, template_path in RANK_TEMPLATES.items():
        confidence = match_template(card_image, template_path)
        if confidence > highest_rank_confidence:
            detected_rank = label
            highest_rank_confidence = confidence

    detected_suit = detect_suit_by_color(card_image, save_debug=save_debug)

    if save_debug and detected_rank:
        cv2.imwrite(f"card_debug_rank_{detected_rank}.png", card_image)

    return detected_rank, detected_suit


def analyze_region() -> Dict[str, Tuple[str | None, str | None]]:
    image = capture_region(CARD_REGION)
    offset = CARD_SPLIT_X - CARD_REGION[0]
    left_card = image[:, :offset]
    right_card = image[:, offset:]

    left_rank, left_suit = analyze_card(left_card, save_debug=True)
    right_rank, right_suit = analyze_card(right_card, save_debug=True)

    return {"left": (left_rank, left_suit), "right": (right_rank, right_suit)}


def analyze_first_community_card(*, save_debug_image: bool = False) -> str | None:
    image = capture_region(COMMUNITY_REGION)
    card_width = COMMUNITY_REGION[2] // 5
    first_card_region = image[:, :card_width]
    rank, suit = analyze_card(first_card_region, save_debug=save_debug_image)
    if rank and suit:
        return f"{rank}{suit}"
    return None
