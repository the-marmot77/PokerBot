from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import numpy as np
import pied_poker as pp

from .vision import analyze_first_community_card, analyze_region

np.random.seed(420)


@dataclass
class SimulationResult:
    player_cards: List[str]
    community_cards: List[str]
    win_probability: str
    lose_probability: str
    opponent_probabilities: List[str]

    def formatted_output(self) -> str:
        lines = [
            f"Detected Player Cards: {', '.join(self.player_cards).upper()}",
            f"Community Cards: {', '.join(self.community_cards).upper() if self.community_cards else 'None'}",
            f"Win Probability: {self.win_probability}",
            f"Lose Probability: {self.lose_probability}",
        ]
        lines.extend(self.opponent_probabilities)
        return "\n".join(lines)


def detect_player_cards() -> List[str]:
    cards = analyze_region()
    left_card = cards.get("left")
    right_card = cards.get("right")

    if not left_card or not right_card:
        raise ValueError("Failed to detect both hole cards.")

    def normalize(card: Sequence[str | None]) -> str:
        rank, suit = card
        if not rank:
            raise ValueError("Rank detection failed – re-align the capture region.")
        return f"{rank}{suit or '?'}".lower()

    normalized = [normalize(left_card), normalize(right_card)]
    if any("?" in card for card in normalized):
        raise ValueError("Suit detection failed for at least one card.")
    return normalized


def _as_card_objects(cards: Iterable[str]) -> Sequence[pp.card.Card]:
    if not cards:
        return []
    return pp.card.Card.of(*cards)


def simulate_poker_round(
    player_cards: Sequence[str],
    *,
    num_opponents: int = 3,
    community_cards: Sequence[str] | None = None,
) -> SimulationResult:
    if not player_cards or any("?" in card for card in player_cards):
        raise ValueError("Player cards must include detected rank and suit.")

    if num_opponents < 1:
        raise ValueError("Number of opponents must be at least one.")

    player_card_objs = _as_card_objects(player_cards)
    community_objs = _as_card_objects(community_cards or [])

    players = [pp.player.Player("You", player_card_objs)]
    for idx in range(1, num_opponents + 1):
        players.append(pp.player.Player(f"Opponent {idx}"))

    simulator = pp.poker_round.PokerRoundSimulator(
        community_cards=community_objs,
        players=players,
        total_players=len(players),
    )
    result = simulator.simulate(n=2500, n_jobs=1)

    hero = players[0]
    win_prob = result.probability_of(pp.probability.events.PlayerWins(hero))
    lose_prob = result.probability_of(pp.probability.events.PlayerLoses(hero))

    opponent_lines = []
    for opponent in players[1:]:
        opp_prob = result.probability_of(pp.probability.events.PlayerWins(opponent))
        opponent_lines.append(f"{opponent.name} Win Probability: {opp_prob}")

    return SimulationResult(
        player_cards=list(player_cards),
        community_cards=list(community_cards or []),
        win_probability=str(win_prob),
        lose_probability=str(lose_prob),
        opponent_probabilities=opponent_lines,
    )


def cli_main() -> None:
    try:
        player_cards = detect_player_cards()
        first_card = analyze_first_community_card(save_debug_image=True)
        community_cards = [first_card] if first_card else []
        result = simulate_poker_round(player_cards, community_cards=community_cards)
        print(result.formatted_output())
    except Exception as exc:
        print(f"PokerBot failed: {exc}")


if __name__ == "__main__":
    cli_main()
