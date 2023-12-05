import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random


def configure_grid(row_col, element):
    for i in range(row_col):
        element.grid_rowconfigure(i, weight=1)
        element.grid_columnconfigure(i, weight=1, uniform='column')
    return element


def switch_to_main_view(key):
    welcome_view.grid_remove()
    main_view.grid(row=0, column=0, sticky='nsew')


def open_picture(number):
    global image_references
    new_width, new_height = 300, 400
    converted_image = ''

    if number in image_references:
        return image_references[number]

    if number == 0:
        image = Image.open("hangman/0.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    elif number == 1:
        image = Image.open("hangman/1.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    elif number == 2:
        image = Image.open("hangman/2.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    elif number == 3:
        image = Image.open("hangman/3.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    elif number == 4:
        image = Image.open("hangman/4.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    elif number == 5:
        image = Image.open("hangman/5.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    elif number == 6:
        image = Image.open("hangman/6.png")
        image = image.resize((new_width, new_height))
        converted_image = ImageTk.PhotoImage(image)
    if number not in image_references:
        image_references[number] = converted_image

    return converted_image


def guess(key, but):
    global word, guessed_letters, errors, current_image, main_image_label, remaining_attempts_label, guessed_words
    but.config(state='disabled')

    if key in word:
        guessed_letters.add(key)
        updated_word_repr = display_word(word, guessed_letters)
        word_label.config(text=updated_word_repr)

    elif errors < 6:
        errors += 1
        current_image = open_picture(errors)
        main_image_label.config(image=current_image)
        new_remaining_attempts = f"You have {6 - errors} remaining attempts.\nPress a button to guess a letter."
        remaining_attempts_label.config(text=new_remaining_attempts)

    if len(set(word)) == len(guessed_letters):
        guessed_words += 1
        message = 'Congratulations! You have won!\nWould you like to play again?'
        end_game(message)

    if errors == 6:
        guessed_words = 0
        message = f'You lost! The word was "{word}".\nWould you like to play again?'
        end_game(message)


def reset_game():
    global word, errors, guessed_letters, current_image, main_image_label, remaining_attempts_label, word_label, streak_label

    errors = 0
    guessed_letters = set()

    word = choose_word()
    guessed_letters.add(word[0])
    guessed_letters.add(word[-1])

    current_image = open_picture(0)
    main_image_label.config(image=current_image)
    new_remaining_attempts = f"You have {6 - errors} remaining attempts.\nPress a button to guess a letter."
    remaining_attempts_label.config(text=new_remaining_attempts)

    new_word_repr = display_word(word, guessed_letters)
    word_label.config(text=new_word_repr)
    streak_text = f"Streak: {guessed_words}"
    streak_label.config(text=streak_text)

    for b in keyboard_buttons:
        button_text = b.cget("text")
        if button_text in guessed_letters:
            b.config(state='disabled')
        else:
            b.config(state='normal')


def end_game(message):
    response = messagebox.askyesno("Game Over", message)
    if response:
        reset_game()
    else:
        root.destroy()


def display_word(word_to_process, letters):
    word_representation = ''.join([l if l in letters else "_ " for l in word_to_process])
    return word_representation


def choose_word():
    with open('words.txt', "r") as words_from_file:
        words = [w.strip().upper() for w in words_from_file.readlines()]

    return random.choice(words)


guessed_words = 0
errors = 0
guessed_letters = set()
image_references = {}

root = tk.Tk()
root.title('Hangman Game')
root.geometry('900x600')
root.resizable(True, True)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

welcome_view = tk.Frame(root, bg='black')
welcome_view.grid(row=0, column=0, sticky='nsew')

welcome_view = configure_grid(5, welcome_view)

welcome_message = ttk.Label(welcome_view, text='HANGMAN\n   GAME', font=('tahoma', 40, 'bold'), foreground='white',
                            background='black')
welcome_message.grid(row=1, column=1, columnspan=4, sticky='news')

current_image = open_picture(6)
image_label = tk.Label(welcome_view, image=current_image, borderwidth=0)
image_label.grid(row=1, column=3, columnspan=2)

press_enter_label = ttk.Label(welcome_view, text='Press "Enter" to continue.', font=('tahoma', 15, 'italic'),
                              foreground='white', background='black')
press_enter_label.grid(row=4, column=0, columnspan=5)

welcome_view.bind('<Return>', switch_to_main_view)
welcome_view.focus_set()
welcome_view['takefocus'] = True

word = choose_word()
main_view = tk.Frame(root, bg='black')
main_view = configure_grid(12, main_view)

keyboard_buttons = []
keyboard_layout = [
    'QWERTYUIO',
    'ASDFGHJKL',
    'ZXCVBNMP'
]

button_style = ttk.Style(root)
button_style.configure('TButton', font=('calibri', 10, 'bold'), borderwidth='1', background='#7393B3')
button_style.map('TButton',
                 foreground=[('!disabled', 'black'), ('active', 'black'), ('disabled', 'light grey')],
                 background=[('active', 'grey'), ('disabled', 'dark grey')],
                 relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

for row_index, row in enumerate(keyboard_layout):
    for col_index, letter in enumerate(row):
        button = ttk.Button(main_view, text=letter)
        button.config(command=lambda b=button, l=letter: guess(l, b))
        if letter == word[0] or letter == word[-1]:
            button.config(state='disabled')
        if row_index == 2:
            col_index += 1
        button.grid(row=row_index + 6, column=col_index + 1, padx=1, pady=1, sticky='snwe')
        keyboard_buttons.append(button)

current_image = open_picture(0)

main_image_label = tk.Label(main_view, image=current_image, borderwidth=0)
main_image_label.grid(row=0, column=7, columnspan=6)

guessed_letters.add(word[0])
guessed_letters.add(word[-1])
word_repr = display_word(word, guessed_letters)

word_label = ttk.Label(main_view, background='black', text=word_repr, font=('calibri', 36, 'bold'), foreground='white')
word_label.grid(row=0, column=0, columnspan=8)

remaining_attempts = f"You have {6 - errors} remaining attempts.\nPress a button to guess a letter."
remaining_attempts_label = ttk.Label(main_view, background='black', text=remaining_attempts,
                                     font=('calibri', 12, 'italic'), foreground='white')
remaining_attempts_label.grid(row=1, column=1, columnspan=6)

streak_label_message = f"Streak: {guessed_words}"
streak_label = ttk.Label(main_view, text=streak_label_message, background='black', foreground='white',
                         font=('calibri', 12, 'bold'))
streak_label.grid(row=1, column=7, columnspan=4)

root.mainloop()
