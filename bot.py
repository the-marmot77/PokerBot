import pied_poker as pp
import numpy as np
from screen_analyzer import analyze_region, analyze_first_community_card

# Seed the random number generator for reproducibility
np.random.seed(420)


def get_player_cards():
    """
    Use screen_analyzer to detect the player's cards.
    Returns:
        list: Detected ranks and suits formatted as strings (e.g., 'as', 'qs').
    """
    detected_cards = analyze_region()
    left_card = detected_cards.get("left")
    right_card = detected_cards.get("right")

    if left_card and right_card and all(left_card) and all(right_card):
        # Handle missing suit detection
        left_suit = left_card[1] if left_card[1] else "?"
        right_suit = right_card[1] if right_card[1] else "?"

        return [
            f"{left_card[0]}{left_suit}".lower(),
            f"{right_card[0]}{right_suit}".lower(),
        ]

    raise ValueError(
        "Failed to detect both player cards. Check the screen region and templates."
    )


def simulate_poker_round(player_cards, num_opponents=3, community_cards=[]):
    """
    Simulate a poker round and return the results.
    """
    output = []
    try:
        # Ensure valid player cards
        if not player_cards or any(
            card is None or "?" in card for card in player_cards
        ):
            raise ValueError(
                "Invalid player cards detected. Suit detection may have failed."
            )

        # Convert to pied_poker card objects
        player_cards_objects = pp.card.Card.of(*player_cards)
        community_cards_objects = (
            pp.card.Card.of(*community_cards) if community_cards else []
        )

        output.append(f"Detected Player Cards: {player_cards}")

        # Create players
        players = [pp.player.Player("You", player_cards_objects)]
        for i in range(1, num_opponents + 1):
            players.append(pp.player.Player(f"Opponent {i}"))

        # Simulate the round
        simulator = pp.poker_round.PokerRoundSimulator(
            community_cards=community_cards_objects,
            players=players,
            total_players=len(players),
        )
        simulation_result = simulator.simulate(n=2500, n_jobs=1)

        # Get probabilities
        p1 = players[0]
        win_prob = simulation_result.probability_of(
            pp.probability.events.PlayerWins(p1)
        )
        lose_prob = simulation_result.probability_of(
            pp.probability.events.PlayerLoses(p1)
        )

        output.append(f"Win Probability: {str(win_prob)}")
        output.append(f"Lose Probability: {str(lose_prob)}")

        # Opponent probabilities
        for opponent in players[1:]:
            opp_win_prob = simulation_result.probability_of(
                pp.probability.events.PlayerWins(opponent)
            )
            output.append(f"🤼 {opponent.name} - Win Probability: {str(opp_win_prob)}")

    except Exception as e:
        return f"Error during simulation: {e}"

    return "\n".join(output)


def main():
    try:
        # Detect player's cards
        player_cards = get_player_cards()
        print(f"Detected Player Cards: {player_cards}")

        # Test community card detection
        first_card = analyze_first_community_card(save_debug_image=True)

        if first_card:
            print(f"Detected First Community Card: {first_card}")
        else:
            print(
                "Failed to detect the first community card. Running simulation without it."
            )

        # Simulate the round if detection was successful
        results = simulate_poker_round(
            player_cards,
            num_opponents=3,
            community_cards=[first_card] if first_card else [],
        )
        print(results)

    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Unhandled error: {e}")


if __name__ == "__main__":
    main()
