from tkinter import *
from tkinter import messagebox
import random
import json
import pandas


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
BACKGROUND_COLOR = "#B1DDC6"
to_learn={}
    
# ---------------------------- CHECK CSV  ------------------------------- #
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    # print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# # Use to_learn for the flashcards
french_words = to_learn

# ---------------------------- RANDOM WORD  ------------------------------- #

def new_card():
    global current_word, is_front, flip_timer
    window.after_cancel(flip_timer)  # Cancel the previous timer

    if french_words:
        current_word = random.choice(french_words)
        canvas.itemconfig(card_image, image=front_img)
        canvas.itemconfig(card_title, text="French")
        canvas.itemconfig(card_word, text=current_word["French"])
        is_front = True

        flip_timer = window.after(5000, flip_card)  # Reset the timer
    else:
        canvas.itemconfig(card_word, text="Well done!")
        canvas.itemconfig(card_title, text="")
    is_front=True
# ---------------------------- Flip Card  ------------------------------- #
def flip_card():
    global is_front
    if is_front:
        canvas.itemconfig(card_image, image=back_img)
        canvas.itemconfig(card_title, text="English")
        canvas.itemconfig(card_word, text=current_word["English"])
    else:
        canvas.itemconfig(card_image, image=front_img)
        canvas.itemconfig(card_title, text="French")
        canvas.itemconfig(card_word, text=current_word["French"])
    is_front = not is_front


# ---------------------------- REMOVE WORD FROM CSV  ------------------------------- #

def is_known():
    to_learn.remove(current_word)
    data=pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False) 
    #index is false removes index number which removes bug which causes index to be created every time you run program
    # print(len(to_learn))
    new_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("FlashCards-French")
window.config(padx=50, pady = 50, bg=BACKGROUND_COLOR)
flip_timer= window.after(5000,flip_card)

canvas = Canvas(width=800, height = 526, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
card_image=canvas.create_image(400,263, image=front_img)
card_title=canvas.create_text(400,150, text="French", font=("Arial", 40, "italic"), fill="black")
card_word=canvas.create_text(400,263, text="word", font=("Arial", 60, "bold"), fill="blue")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0 , columnspan=2)

# ---------------------------- NEXT CARD-click  ------------------------------- #

canvas.bind("<Button-1>", lambda event: flip_card())#binds left click to flip card function



# Buttons
check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command = is_known)
check_button.grid(row=1, column=0)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,command=new_card)
wrong_button.grid(row=1, column=1)

is_front = True  # Variable to track which side of the card is showing
new_card()  # Display the first word

window.mainloop()