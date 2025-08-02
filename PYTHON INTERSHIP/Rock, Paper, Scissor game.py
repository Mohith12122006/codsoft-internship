import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rock Paper Scissors")
        self.window.geometry("400x400")
        self.window.resizable(False, False)
        
        # Choices
        self.choices = ["Rock", "Paper", "Scissors"]
        
        # Score tracking
        self.player_score = 0
        self.computer_score = 0
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.window, text="Rock Paper Scissors", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)
        
        # Score display
        self.score_label = tk.Label(self.window, text=f"Player: {self.player_score}  Computer: {self.computer_score}", 
                                  font=("Arial", 12))
        self.score_label.pack(pady=10)
        
        # Result display
        self.result_label = tk.Label(self.window, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        # Buttons frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=20)
        
        # Choice buttons
        tk.Button(self.button_frame, text="Rock", width=10, command=lambda: self.play("Rock")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Paper", width=10, command=lambda: self.play("Paper")).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Scissors", width=10, command=lambda: self.play("Scissors")).pack(side=tk.LEFT, padx=5)
        
        # Reset button
        tk.Button(self.window, text="Reset Score", command=self.reset_score).pack(pady=20)
        
    def play(self, player_choice):
        computer_choice = random.choice(self.choices)
        
        # Determine winner
        result = self.determine_winner(player_choice, computer_choice)
        
        # Update result label
        self.result_label.config(text=f"You chose: {player_choice}\nComputer chose: {computer_choice}\n{result}")
        
        # Update score display
        self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")
        
    def determine_winner(self, player, computer):
        if player == computer:
            return "It's a tie!"
        elif (player == "Rock" and computer == "Scissors") or \
             (player == "Paper" and computer == "Rock") or \
             (player == "Scissors" and computer == "Paper"):
            self.player_score += 1
            return "You win!"
        else:
            self.computer_score += 1
            return "Computer wins!"
            
    def reset_score(self):
        self.player_score = 0
        self.computer_score = 0
        self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")
        self.result_label.config(text="")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = RockPaperScissors()
    game.run()