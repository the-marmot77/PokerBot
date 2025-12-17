# PokerBot

Computer-vision helper that reads an online poker table, detects hole/community cards, and feeds the results into [pied-poker](https://github.com/CuriousAI/pied-poker) to estimate win probabilities. Everything now lives inside the `pokerbot/` package with a GUI, CLI, and debugging utilities.

## Repository map

| Path | Description |
| --- | --- |
| `pokerbot/vision.py` | Screen capture helpers plus template matching/HSV filtering for rank and suit detection. |
| `pokerbot/simulator.py` | Orchestrates detection + pied-poker simulations and exposes a CLI-friendly API. |
| `pokerbot/gui.py` | Tkinter front-end to run simulations, choose opponent counts, and toggle community-card auto-detect. |
| `tests.py` | Standalone debug script that grabs predefined regions via `mss` and logs the detected cards. |
| `artifacts/` | Collected debug outputs: rank/suit crops, suit masks, palette references (`Colors*.png`). |
| `Cards/`, `Suits/` | Rank templates and suit color references. |
| `debug_screenshots/` | Saved crops from failed detections (safe to delete when not needed). |

## Setup

1. Python 3.11+ on Windows (coordinates assume the default Windows poker layout).
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Align `CARD_REGION`, `CARD_SPLIT_X`, and `COMMUNITY_REGION` inside `pokerbot/vision.py` to match your monitor resolution and table position.

## Usage

- **CLI odds check**
  ```powershell
  python -m pokerbot.simulator
  ```
  Detects hole cards, optionally the first board card, and prints win/lose probabilities.

- **GUI**
  ```powershell
  python -m pokerbot
  ```
  Launches a small Tkinter app that runs the detector, lets you configure opponents/community cards, and displays the results.

- **Debug capture**
  ```powershell
  python tests.py
  ```
  Captures each configured card region, saves hero-card crops under `debug_screenshots/`, and prints out detected values.

## How the pieces fit

1. `pokerbot.vision` captures the configured screen regions, splits them into card crops, and runs template matching for rank + HSV filtering for suit.
2. `pokerbot.simulator.detect_player_cards()` wraps the vision module and returns strings like `["as", "qh"]`. `simulate_poker_round()` converts those strings into pied-poker `Card` objects, seeds opponents, and runs Monte Carlo simulations.
3. `pokerbot.gui` is a lightweight Tkinter interface calling into the simulator so you can trigger odds checks with a single click.
4. `tests.py` remains as a utility script for recalibrating coordinates or validating new card templates with repeatable screenshots.

## Notes

- Coordinates assume a single monitor with cards around `(x=1200, y=980)`; adjust the constants for other layouts.
- Template PNGs should match your poker client's font/size. Replacing them with crisp monochrome digits/letters often improves accuracy.
- All capture paths respect `pyautogui.FAILSAFE` (move the cursor to the top-left corner to abort).

Feel free to extend the package with richer board detection, logging, or automation once you are happy with the baseline card recognition.
