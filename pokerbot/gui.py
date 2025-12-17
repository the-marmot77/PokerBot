from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import List

from .simulator import detect_player_cards, simulate_poker_round
from .vision import analyze_first_community_card


class PokerBotGUI:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Poker Odds")
        self.window.geometry("360x420")
        self.window.configure(bg="#121212")

        self.opponent_input = tk.Entry(
            self.window,
            font=("Helvetica", 11),
            width=6,
            bg="#1E1E1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
        )
        self.community_entry = tk.Entry(
            self.window,
            font=("Helvetica", 11),
            width=22,
            bg="#1E1E1E",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
        )
        self.auto_detect_var = tk.BooleanVar(value=True)
        self.output_label = tk.Label(
            self.window,
            text="",
            font=("Helvetica", 10),
            justify="left",
            fg="#FFFFFF",
            bg="#121212",
        )
        self._build_layout()

    def _build_layout(self) -> None:
        tk.Label(
            self.window,
            text="Poker Odds Generator",
            font=("Helvetica", 14),
            fg="#FFFFFF",
            bg="#121212",
        ).pack(pady=6)

        tk.Label(
            self.window,
            text="Opponents:",
            font=("Helvetica", 11),
            fg="#FFFFFF",
            bg="#121212",
        ).pack(pady=(10, 0))
        self.opponent_input.pack()
        self.opponent_input.insert(0, "3")

        tk.Label(
            self.window,
            text="Community Cards (comma separated):",
            font=("Helvetica", 11),
            fg="#FFFFFF",
            bg="#121212",
        ).pack(pady=(12, 0))
        self.community_entry.pack()

        tk.Checkbutton(
            self.window,
            text="Auto-detect first community card",
            variable=self.auto_detect_var,
            font=("Helvetica", 10),
            bg="#121212",
            fg="#FFFFFF",
            selectcolor="#333333",
        ).pack(pady=8)

        tk.Button(
            self.window,
            text="Generate Odds",
            font=("Helvetica", 11),
            bg="#1E1E1E",
            fg="#FFFFFF",
            command=self._on_generate,
        ).pack(pady=10)

        self.output_label.pack(pady=10, padx=16, fill="both")

        self.window.after(100, lambda: self.opponent_input.focus())

    def _parse_opponents(self) -> int:
        try:
            opponents = int(self.opponent_input.get())
            if opponents < 1:
                raise ValueError
            return opponents
        except ValueError:
            raise ValueError("Number of opponents must be a positive integer.")

    def _parse_community_cards(self) -> List[str]:
        text = self.community_entry.get().strip().lower()
        return [card.strip() for card in text.split(",") if card.strip()]

    def _detect_community_cards(self) -> List[str]:
        community_cards = self._parse_community_cards()
        if self.auto_detect_var.get():
            detected = analyze_first_community_card(save_debug_image=True)
            if detected:
                community_cards.insert(0, detected)
        return community_cards

    def _on_generate(self) -> None:
        try:
            opponents = self._parse_opponents()
            player_cards = detect_player_cards()
            community_cards = self._detect_community_cards()
            result = simulate_poker_round(
                player_cards, num_opponents=opponents, community_cards=community_cards
            )
            self.output_label.config(text=result.formatted_output())
        except ValueError as exc:
            messagebox.showwarning("Poker Odds", str(exc))
        except Exception as exc:
            messagebox.showerror("Poker Odds", f"Unexpected error: {exc}")

    def run(self) -> None:
        self.window.mainloop()


def launch() -> None:
    PokerBotGUI().run()


if __name__ == "__main__":
    launch()
