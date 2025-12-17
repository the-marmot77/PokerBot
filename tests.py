from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import cv2
import mss
import numpy as np

from pokerbot.vision import analyze_card

DEBUG_FOLDER = Path("debug_screenshots")
DEBUG_FOLDER.mkdir(exist_ok=True)

CARD_POSITIONS: Dict[str, Tuple[int, int, int, int]] = {
    "hole_1": (1228, 988, 44, 55),
    "hole_2": (1276, 988, 44, 55),
    "comm_1": (400, 400, 50, 80),
    "comm_2": (480, 400, 50, 80),
    "comm_3": (560, 400, 50, 80),
    "comm_4": (640, 400, 50, 80),
    "comm_5": (720, 400, 50, 80),
}


def capture_box(box: Tuple[int, int, int, int]) -> np.ndarray:
    x, y, w, h = box
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": w, "height": h}
        screenshot = np.array(sct.grab(monitor))
    return cv2.cvtColor(screenshot[:, :, :3], cv2.COLOR_BGRA2BGR)


def detect_cards() -> Dict[str, str]:
    detected = {}
    for name, box in CARD_POSITIONS.items():
        card_img = capture_box(box)
        if name.startswith("hole"):
            cv2.imwrite(str(DEBUG_FOLDER / f"{name}.png"), card_img)
        rank, suit = analyze_card(card_img, save_debug=False)
        if rank and suit:
            detected[name] = f"{rank}{suit}"
    return detected


def main() -> None:
    cards = detect_cards()
    if not cards:
        print("No cards detected.")
        return
    print("Detected Cards:")
    for label, value in cards.items():
        print(f"{label}: {value}")


if __name__ == "__main__":
    main()
