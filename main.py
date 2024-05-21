# jen 21/5/2024

import json
import math
import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import defaultdict

class Repository():

    def __init__(self):
        self.rolls = None
        self.face = None
        self.font = ('Arial', 14)
        self.face_count = 20
        self.load()

    def load(self, filename="0"):
        with open(f"saves/{filename}.json") as file:
            loaded_file = json.load(file)
            self.rolls = loaded_file["rolls"]
            self.face = defaultdict(int,loaded_file["face"])


    def save(self, filename="1"):
        with open(f"saves/{filename}.json", "w", encoding="utf-8") as file:
            json.dump({"rolls": self.rolls, "face": self.face}, file, ensure_ascii=False, indent=4)

class Window():

    def __init__(self):
        self.repo = Repository()

        # Set up basics for window.
        self.root = tk.Tk()
        self.root.title("Dice Counter")
        self.root.iconphoto(False, tk.PhotoImage(file="icon.png"))

        # Create a list for frames and a dictionary to hold string variables for the output.
        self.frame_list = []
        self.var_dict = {}

        # Create two frames, one for a total rolls label, another for the buttons.
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, expand=True, side=tk.TOP)
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, expand=True, side=tk.TOP)
        
        # Create the frames and buttons for the display and update the output to the values saved from memory.
        self.makeDisplay()
        self.updateOutput()

        # Set up an exit menu and enter mainloop.
        self.root.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.root.mainloop()
    
    def makeDisplay(self):
        # Empty and forget all frames and reset list.
        for frame in self.frame_list: 
            for widget in frame.winfo_children(): widget.destroy()
            frame.pack_forget()
            frame.destroy()
        self.frame_list = []

        # Set variables based on the number of faces on the die.
        cols = math.floor(self.repo.face_count**0.5)
        buttons_per_col = math.ceil(self.repo.face_count/cols)

        # Create and pack a label for the total number of rolls.
        self.var_dict["rolls"] = tk.StringVar()
        self.rolls_text = tk.Label(self.top_frame,
                                   textvariable=self.var_dict["rolls"],
                                   font=self.repo.font)
        self.rolls_text.pack(padx=10, pady=5)

        # Create frames to hold the buttons.
        for _ in range(cols):
            frame = tk.Frame(self.bottom_frame)
            self.frame_list.append(frame)
            self.frame_list[-1].pack(fill=tk.X, expand=True, side=tk.LEFT)

        # Create the buttons.
        for i in range(self.repo.face_count):
            self.var_dict[str(i+1)] = tk.StringVar()
            button = tk.Button(self.frame_list[i//buttons_per_col],
                               textvariable=self.var_dict[str(i+1)],
                               bg="green",
                               fg="white",
                               font=self.repo.font,
                               width=10,
                               command=lambda i=i: self.incrementCount(str(i+1)))
            button.pack(padx=10, pady=10)

    def incrementCount(self, count="rolls"):
        # Add one to the roll counter and a specific counter then update the output.
        self.repo.rolls += 1
        self.repo.face[count] += 1
        self.updateOutput()
    
    def updateOutput(self):
        # Set the StringVars equal to the values stored in the dictionary.
        self.var_dict["rolls"].set(f"Rolls: {self.repo.rolls}")
        for i in range(self.repo.face_count):
            self.var_dict[str(i+1)].set(f"{i+1}\nCount: {self.repo.face[str(i+1)]}")
    
    def onClosing(self):
        # Check if the user wants to close the window.
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"): 
            self.root.destroy()

Window()