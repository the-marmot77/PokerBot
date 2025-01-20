import pied_poker as pp
import numpy as np
from screen_analyzer import analyze_region

# Seed the random number generator for reproducibility
np.random.seed(420)

def get_player_cards():
    """
    Use screen_analyzer to detect the player's cards.
    Returns:
        list: Detected ranks and suits formatted as strings (e.g., 'as', 'qs').
    """

    detected_cards = analyze_region()

    # Extract left and right cards
    left_card = detected_cards.get("left")
    right_card = detected_cards.get("right")

    if left_card and right_card:
        # Format as strings for pied_poker (e.g., 'as', 'qs')
        return [
            f"{left_card[0]}{left_card[1]}".lower(),
            f"{right_card[0]}{right_card[1]}".lower()
        ]
    else:
        raise ValueError("Failed to detect both cards. Check the screen region and templates.")

def simulate_poker_round(player_cards, num_opponents=3, community_cards=[]):
    """
    Simulate a poker round and return the results.
    Args:
        player_cards (list): List of player cards (e.g., ['as', 'qs']).
        num_opponents (int): Number of opponents.
        community_cards (list): List of community cards (default empty).
    Returns:
        str: Formatted string with simulation results.
    """
    output = []
    try:
        # Create your player
        players = [pp.player.Player('You', player_cards)]

        # Dynamically create opponents
        for i in range(1, num_opponents + 1):
            players.append(pp.player.Player(f'Opponent {i}'))

        # Display the players and community cards
        output.append(f"Players: {players}")
        output.append(f"Community cards: {community_cards}")

        # Simulate a round
        simulator = pp.poker_round.PokerRoundSimulator(
            community_cards=community_cards,
            players=players,
            total_players=len(players)
        )

        # Run the simulation
        num_simulations = 1000
        simulation_result = simulator.simulate(n=num_simulations, n_jobs=1)

        # Calculate probabilities for your player
        p1 = players[0]  # Reference your player
        win_prob = simulation_result.probability_of(pp.probability.events.PlayerWins(p1))
        lose_prob = simulation_result.probability_of(pp.probability.events.PlayerLoses(p1))

        # Display probabilities
        output.append(f"Win Probability: {str(win_prob)}")
        output.append(f"Lose Probability: {str(lose_prob)}")

        # Optional: Display probabilities for opponents
        for opponent in players[1:]:
            opp_win_prob = simulation_result.probability_of(pp.probability.events.PlayerWins(opponent))
            output.append(f"{opponent.name} - Win Probability: {str(opp_win_prob)}")

    except Exception as e:
        output.append(f"Error during simulation: {e}")

    return "\n".join(output)

def main():
    """
    Main function to execute the poker odds simulation.
    """
    try:
        player_cards_input = get_player_cards()
        player_cards = pp.card.Card.of(*player_cards_input)
    except ValueError as e:
        print(e)
        return

    # Run simulation and display results
    results = simulate_poker_round(player_cards)
    print(results)

if __name__ == "__main__":
    main()
