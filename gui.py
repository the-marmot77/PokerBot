import tkinter as tk
from bot import simulate_poker_round, get_player_cards
from screen_analyzer import analyze_first_community_card

def generate_odds():
    """
    Generate and display player cards, community cards, and win/lose probabilities.
    """
    output_label.config(text="")  # Clear the output label
    try:
        # Get player cards
        player_cards = get_player_cards()

        # Get the number of opponents
        num_opponents = int(opponent_input.get())
        if num_opponents < 1:
            raise ValueError("Number of opponents must be at least 1.")

        # Detect or manually input community cards
        if auto_detect_var.get():
            first_card = analyze_first_community_card(save_debug_image=True)  # Save debug images
            community_cards = [first_card] if first_card else []
        else:
            community_cards_input = community_cards_entry.get().strip()
            community_cards = [card.strip().lower() for card in community_cards_input.split(",")] if community_cards_input else []

        # Ensure no None values appear
        community_cards = [card for card in community_cards if card]

        # Run the simulation
        output = simulate_poker_round(player_cards, num_opponents=num_opponents, community_cards=community_cards)

        # Extract and clean win/lose probabilities
        lines = output.split("\n")
        win_line = next((line for line in lines if "Win Probability" in line), None)
        lose_line = next((line for line in lines if "Lose Probability" in line), None)

        # Extract numbers even if format varies
        def extract_probability(line):
            if not line:
                return "N/A"
            try:
                return line.split(":")[1].strip()
            except IndexError:
                return "N/A"

        win_prob = extract_probability(win_line)
        lose_prob = extract_probability(lose_line)

        # Display detected player cards, detected community cards, win probability, and lose probability
        output_label.config(
            text=f"🎴 Detected Cards: {', '.join(player_cards).upper()}\n"
                 f"🃏 Community Cards: {', '.join(community_cards).upper() if community_cards else 'None'}\n"
                 f"✅ Win Probability: {win_prob}\n"
                 f"❌ Lose Probability: {lose_prob}"
        )

    except Exception as e:
        output_label.config(text=f"⚠️ Error: {e}")

# Initialize the main GUI window
window = tk.Tk()
window.title("Poker Odds Generator")
window.geometry("350x500")  # Slightly larger to accommodate the checkbox
window.configure(bg="#121212")  # Dark mode background

# Add a title label
label = tk.Label(window, text="Poker Odds Generator", font=("Helvetica", 12), fg="#FFFFFF", bg="#121212")
label.pack(pady=5)

# Add input for the number of opponents
opponent_label = tk.Label(window, text="Opponents:", font=("Helvetica", 10), fg="#FFFFFF", bg="#121212")
opponent_label.pack(pady=2)
opponent_input = tk.Entry(window, font=("Helvetica", 10), width=5, bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF")
opponent_input.pack()
opponent_input.insert(0, "8")  # Default value

# Add input for community cards
community_cards_label = tk.Label(window, text="Community Cards:", font=("Helvetica", 10), fg="#FFFFFF", bg="#121212")
community_cards_label.pack(pady=2)
community_cards_entry = tk.Entry(window, font=("Helvetica", 10), width=20, bg="#1E1E1E", fg="#FFFFFF", insertbackground="#FFFFFF")
community_cards_entry.pack()

# Add checkbox for auto-detecting the first community card
auto_detect_var = tk.BooleanVar()
auto_detect_checkbox = tk.Checkbutton(
    window, text="Auto-Detect First Community Card", variable=auto_detect_var, font=("Helvetica", 10),
    bg="#121212", fg="#FFFFFF", selectcolor="#333333"
)
auto_detect_checkbox.pack(pady=5)

# Add a button to trigger odds generation
generate_button = tk.Button(
    window, text="Generate Odds", command=generate_odds, font=("Helvetica", 10), bg="#1E1E1E",
    fg="#FFFFFF", activebackground="#333333", activeforeground="#FFFFFF"
)
generate_button.pack(pady=10)

# Add a label to display detected player cards and win/lose probabilities
output_label = tk.Label(window, text="", font=("Helvetica", 10), justify="center", fg="#FFFFFF", bg="#121212")
output_label.pack(pady=5)

# Automatically focus on the opponent input field on startup
window.after(100, lambda: opponent_input.focus())

# Start the GUI event loop
window.mainloop()
