import pied_poker as pp
import numpy as np

np.random.seed(420)

# Prompt for your cards
cards_input = input("Enter your cards (e.g., 'as, qs' for Ace of Spades, Queen of Spades): ")
player_cards = pp.card.Card.of(*[card.strip() for card in cards_input.split(',')]) if cards_input.strip() else []

# Prompt for the number of opponents
num_opponents = int(input("Enter the number of opponents: "))

# Optional: Prompt for community cards
community_input = input("Enter community cards (e.g., '4s, 4h, 10s' or leave blank): ")
community_cards = pp.card.Card.of(*[card.strip() for card in community_input.split(',')]) if community_input.strip() else []

# Create your player
players = [pp.player.Player('You', player_cards)]

# Dynamically create opponents
for i in range(1, num_opponents + 1):
    players.append(pp.player.Player(f'Opponent {i}'))

# Display the players and community cards
print(f"Players: {players}")
print(f"Community cards: {community_cards}")

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
print(f"Win Probability: {str(win_prob)}")
print(f"Lose Probability: {str(lose_prob)}")

# Optional: Display probabilities for opponents (if needed)
for opponent in players[1:]:
    opp_win_prob = simulation_result.probability_of(pp.probability.events.PlayerWins(opponent))
    print(f"{opponent.name} - Win Probability: {str(opp_win_prob)}")

# Visualize your hand distribution
simulation_result.visualize_player_hand_distribution(p1)
