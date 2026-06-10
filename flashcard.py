import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILE_NAME = "flashcards.json"

# Load flashcards
def load_flashcards():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    else:
        return [
            {"question": "What is the capital of India?", "answer": "New Delhi"},
            {"question": "Who developed Python?", "answer": "Guido van Rossum"},
            {"question": "What is 2 + 2?", "answer": "4"}
        ]

# Save flashcards
def save_flashcards():
    with open(FILE_NAME, "w") as file:
        json.dump(flashcards, file, indent=4)

flashcards = load_flashcards()
current_index = 0
showing_answer = False

# Display current card
def display_card():
    global showing_answer

    if not flashcards:
        card_text.config(text="No Flashcards Available")
        return

    showing_answer = False
    card_text.config(text=flashcards[current_index]["question"])

# Show answer
def show_answer():
    global showing_answer

    if flashcards:
        card_text.config(text=flashcards[current_index]["answer"])
        showing_answer = True

# Next card
def next_card():
    global current_index

    if flashcards:
        current_index = (current_index + 1) % len(flashcards)
        display_card()

# Previous card
def previous_card():
    global current_index

    if flashcards:
        current_index = (current_index - 1) % len(flashcards)
        display_card()

# Add flashcard
def add_flashcard():
    question = simpledialog.askstring("Add Flashcard", "Enter Question:")
    if not question:
        return

    answer = simpledialog.askstring("Add Flashcard", "Enter Answer:")
    if not answer:
        return

    flashcards.append({
        "question": question,
        "answer": answer
    })

    save_flashcards()
    messagebox.showinfo("Success", "Flashcard Added Successfully!")

# Edit flashcard
def edit_flashcard():
    global current_index

    if not flashcards:
        return

    question = simpledialog.askstring(
        "Edit Question",
        "Edit Question:",
        initialvalue=flashcards[current_index]["question"]
    )

    if not question:
        return

    answer = simpledialog.askstring(
        "Edit Answer",
        "Edit Answer:",
        initialvalue=flashcards[current_index]["answer"]
    )

    if not answer:
        return

    flashcards[current_index] = {
        "question": question,
        "answer": answer
    }

    save_flashcards()
    display_card()
    messagebox.showinfo("Success", "Flashcard Updated!")

# Delete flashcard
def delete_flashcard():
    global current_index

    if not flashcards:
        return

    confirm = messagebox.askyesno(
        "Delete",
        "Are you sure you want to delete this flashcard?"
    )

    if confirm:
        flashcards.pop(current_index)

        if flashcards:
            current_index = min(current_index, len(flashcards) - 1)
        else:
            current_index = 0

        save_flashcards()
        display_card()

# GUI Window
root = tk.Tk()
root.title("Flashcard Quiz App")
root.geometry("700x500")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Flashcard Quiz App",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)

card_frame = tk.Frame(
    root,
    bd=2,
    relief="solid",
    padx=20,
    pady=20
)
card_frame.pack(pady=20)

card_text = tk.Label(
    card_frame,
    text="",
    font=("Arial", 16),
    wraplength=500,
    width=40,
    height=6
)
card_text.pack()

show_btn = tk.Button(
    root,
    text="Show Answer",
    font=("Arial", 12),
    command=show_answer
)
show_btn.pack(pady=10)

nav_frame = tk.Frame(root)
nav_frame.pack(pady=10)

prev_btn = tk.Button(
    nav_frame,
    text="Previous",
    width=12,
    command=previous_card
)
prev_btn.grid(row=0, column=0, padx=10)

next_btn = tk.Button(
    nav_frame,
    text="Next",
    width=12,
    command=next_card
)
next_btn.grid(row=0, column=1, padx=10)

manage_frame = tk.Frame(root)
manage_frame.pack(pady=20)
add_btn = tk.Button(
    manage_frame,
    text="Add",
    width=12,
    command=add_flashcard
)
add_btn.grid(row=0, column=0, padx=10)

edit_btn = tk.Button(
    manage_frame,
    text="Edit",
    width=12,
    command=edit_flashcard
)
edit_btn.grid(row=0, column=1, padx=10)

delete_btn = tk.Button(
    manage_frame,
    text="Delete",
    width=12,
    command=delete_flashcard
)
delete_btn.grid(row=0, column=2, padx=10)

display_card()

root.mainloop()