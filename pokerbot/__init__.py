"""
pokerbot
========

High level helpers for detecting cards on screen and simulating holdem odds.
"""

from .simulator import (
    detect_player_cards,
    simulate_poker_round,
    SimulationResult,
)
from .vision import analyze_first_community_card

__all__ = [
    "detect_player_cards",
    "simulate_poker_round",
    "SimulationResult",
    "analyze_first_community_card",
]
