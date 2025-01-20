import tkinter as tk
from tkinter import scrolledtext
from io import StringIO
import sys
from bot import main as run_bot  # Import the main function from bot.py

def capture_output(func):
    """
    Redirect standard output (stdout) to capture the output of a function.
    Args:
        func (callable): The function to execute and capture its output.
    Returns:
        str: The captured output.
    """
    old_stdout = sys.stdout  # Backup original stdout
    sys.stdout = StringIO()  # Redirect stdout to a StringIO object
    try:
        func()
        output = sys.stdout.getvalue()  # Get the captured output
    finally:
        sys.stdout = old_stdout  # Restore original stdout
    return output

def generate_odds():
    """
    Trigger the poker odds calculation and display the results in the GUI.
    """
    output_box.delete(1.0, tk.END)  # Clear the output box
    try:
        # Capture the output of run_bot() and display it in the GUI
        output = capture_output(run_bot)
        output_box.insert(tk.END, output)
    except Exception as e:
        output_box.insert(tk.END, f"Error: {e}\n")

# Initialize the main GUI window
window = tk.Tk()
window.title("Poker Odds Generator")
window.geometry("800x500")

# Add a label
label = tk.Label(window, text="Poker Odds Generator", font=("Helvetica", 16))
label.pack(pady=10)

# Add a button to trigger odds generation
generate_button = tk.Button(window, text="Generate Odds", command=generate_odds, font=("Helvetica", 14))
generate_button.pack(pady=20)

# Add a scrolled text box to display output
output_box = scrolledtext.ScrolledText(window, width=60, height=20, wrap=tk.WORD, font=("Helvetica", 10))
output_box.pack(pady=10)

# Start the GUI event loop
window.mainloop()
