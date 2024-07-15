import random
from english_words import get_english_words_set
from tkinter import *
from PIL import ImageTk, Image


all_words = sorted(list(get_english_words_set(['web2'], lower=True)))
random_words = []
correct_words = []
incorrect_words = []
total_words = []
TIMER = False
current_word_index = 0


def start_timer():
    global random_words, TIMER, current_word_index
    random_words = random.sample(all_words, 100)
    TIMER = True
    current_word_index = 0
    countdown(60)
    next_word()
    input_field.focus_set()
    input_field.config(state='normal')


def countdown(count):
    global TIMER
    count_sec = f'{count:02}'
    if count > 0:
        timer.config(text=f"{count_sec}")
        TIMER = window.after(1000, countdown, count - 1)
    else:
        timer.config(text="00")
        pop_up_results()


def reset_timer():
    global TIMER
    if TIMER:
        window.after_cancel(TIMER)
        TIMER = False
    clear_all()
    start_timer()
    

def help_function():

    pop_up = Toplevel(window)
    pop_up.title("Help")
    pop_up.config(bg='grey')

    title = Label(pop_up, text= "Welcome to the Speed Type Test!", font=('Helvetica', 35), bg='grey')
    title.pack(pady=20)

    instructions = Label(pop_up, font=('Tahoma', 15), bg='grey', justify='left',
                         text='This game challenges you to type fast! \n'
                               "Here are the instructions: \n"
                              "\n"
                               "When you click start, a random word will appear. Just type it. \n"
                               "Once you start typing, the timer will start. \n"
                               "When you're done, hit SPACEBAR or ENTER for the next word. \n"
                               "Each time a new word will appear until you run out of time. \n"
                               "\n"
                               "Only correctly spelled words count, but you can delete letters. \n"
                               "The application automatically saves the 10 highest scores. \n"
                               " \n"
                               'Have fun!' )
    instructions.pack(pady=20)

    button_frame = Frame(pop_up, bg='grey')
    button_frame.pack(pady=20)

    high_score_button = Button(button_frame, text= 'High Scores', command=high_scores, font=('Helvetica', 14))
    high_score_button.pack(side=LEFT, padx= 10)

    close_button = Button(button_frame, text='Close', command=pop_up.destroy, font=('Helvetica', 14))
    close_button.pack(side=RIGHT, padx= 10)



def high_scores():
    pop_up = Toplevel(window)
    pop_up.title("High Scores")
    pop_up.config(bg='grey')

    scores_title = Label(pop_up, text='Top 10 Scores', fg='green', font=('Helvetica', 20), bg='grey')
    scores_title.pack(pady=10)

    with open('data.txt', 'r') as data:
        scores = data.readlines()
    scores = [int(score.strip()) for score in scores]

    for score in scores:
        score_label = Label(pop_up, text=f'{score}', font=('Tahoma', 14), bg='grey')
        score_label.pack()

    button_frame = Frame(pop_up, bg='grey')
    button_frame.pack(pady=20)

    back_button = Button(button_frame, text='back', command=help_function, font=('Helvetica', 14))
    back_button.pack(side=LEFT, padx=10)
    close_button = Button(button_frame, text='Close', command=pop_up.destroy, font=('Helvetica', 14))
    close_button.pack(side=RIGHT, padx= 10)

def clear_all():
    global random_words, correct_words, \
        current_word_index, incorrect_words, total_words
    random_words.clear()
    correct_words.clear()
    incorrect_words.clear()
    total_words.clear()
    current_word_index = 0
    input_field.delete('1.0', END)
    input_field.config(state='disabled')
    card_canvas.itemconfig(card_word, text='')

def pop_up_results():
    global TIMER
    TIMER = False
    save_score()
    pop_up = Toplevel(window)
    pop_up.title("Results")
    pop_up.config(bg='grey')

    correct_wpm = len(correct_words)
    incorrect_wpm = len(incorrect_words)
    total_wpm = len(total_words)

    result_title = Label(pop_up, text="Typing Speed Test Results", fg='green',
                        font=('Helvetica', 35, 'bold'), bg='grey' )
    result_title.pack(pady=10)

    result_paragraph = Label(pop_up, text="Here is the summary of your results. How did it go?",
                             font=('Helvetica', 20), bg='grey', justify='left')
    result_paragraph.pack(pady=10)

    total_label = Label(pop_up, text=f'Total Words: {total_wpm} per minute', fg='black',
                          font=('Helvetica', 16), bg='grey')
    total_label.pack(pady=5)
    correct_label = Label(pop_up, text=f'Correct Words: {correct_wpm}', fg='green',
                          font=('Helvetica', 16), bg='grey')
    correct_label.pack(pady=5)
    incorrect_label = Label(pop_up, text=f'Incorrect Words: {incorrect_wpm}', fg='red',
                          font=('Helvetica', 16), bg='grey')
    incorrect_label.pack(pady=5)

    final_label = Label(pop_up, text=f'Final Score: {correct_wpm} per minute', fg='green',
                          font=('Helvetica', 16), bg='grey')
    final_label.pack(pady=10)

    scores_title = Label(pop_up, text='Top 10 Scores', font=('Helvetica', 20), bg='grey')
    scores_title.pack(pady=10)

    with open('data.txt', 'r') as data:
        scores = data.readlines()
    scores = [int(score.strip()) for score in scores]

    for score in scores:
        if score == correct_wpm:
            score_label = Label(pop_up, text=f'{score}', fg='green', font=('Helvetica', 14), bg='grey')
        else:
            score_label = Label(pop_up, text=f'{score}', font=('Helvetica', 14), bg='grey')
        score_label.pack()

    close_button = Button(pop_up, text='Close', command=pop_up.destroy, font=('Helvetica', 14))
    close_button.pack(pady=20)

    clear_all()


def save_score():
    new_score = len(correct_words)
    try:
        with open("data.txt", mode="r") as data:
            scores = data.readlines()
        scores = [int(score.strip()) for score in scores]
    except FileNotFoundError:
        scores = []

    scores.append(new_score)
    scores.sort(reverse=True)
    scores = scores[:10]

    with open("data.txt", 'w') as data:
        for score in scores:
            data.write(f"{score}\n")


def next_word():
    global current_word_index, random_words
    current_word = random_words[current_word_index]
    card_canvas.itemconfig(card_word, text=current_word)
    input_field.delete('1.0', END)
    input_field.update_idletasks()

    
def on_spacebar(event):
    global current_word_index, input_field
    if input_field.get("1.0","end-1c").strip() == "":
        return
    check_word()
    input_field.delete('1.0', END)
    current_word_index += 1
    next_word()


def on_key_press(event):
    global input_field, random_words, current_word_index


    current_input = input_field.get('1.0', 'end-1c').strip()
    current_word = random_words[current_word_index]

    input_field.tag_delete('mistake')
    for i in range(len(current_input)):
        if i < len(current_word) and current_input[i] != current_word[i]:
            show_mistake(i)


def show_mistake(index):
    global input_field

    input_field.tag_add("mistake", f"1.{index}", f"1.{index +1}")
    input_field.tag_config("mistake", foreground="red")


def check_word():
    global current_word_index, random_words, input_field, \
        correct_words,incorrect_words, total_words
    current_input = input_field.get('1.0', 'end-1c').strip()
    current_word = random_words[current_word_index]

    if current_input == current_word:
        correct_words.append(current_word)
    else:
        incorrect_words.append(current_word)
    total_words.append(current_word)




# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Typing Speed Test")
window.config(bg='grey')
window.minsize(width=700, height=500)


#--------Frames-------
timer_frame = Frame(window, bg='grey')
timer_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

card_frame = Frame(window, bg='grey')
card_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

input_frame = Frame(window, bg='grey')
input_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

#----------------------Timer label-----------------------
timer = Label(timer_frame, text="00", fg="white", font=('Helvetica', 55), bg='grey')
timer.pack()

#----------------------CARD-----------------------
#---canvas
card_canvas = Canvas(card_frame,width=650, height=450, bg='grey',highlightthickness=0)
card_canvas.pack()

card_image = Image.open("card.png")
card_image = card_image.resize((card_image.width * 2, card_image.height * 2))
card_img = ImageTk.PhotoImage(card_image)
card_canvas.create_image(325,225, image=card_img)

card_word =card_canvas.create_text(325,225, text='', fill='white', font=('Helvetica', 35))

#----------------------Buttons and input space-----------------------
# ----help----
help_icon = Image.open('question.png')
help_icon = help_icon.resize((55, 55), Image.LANCZOS)
help_icon = ImageTk.PhotoImage(help_icon)

help_button = Button(input_frame, image=help_icon, command=help_function)
help_button.pack(side= LEFT, padx=10)

#----user input field----
input_field = Text(input_frame, font=('Helvetica', 35), height=1, width=20, state='disabled')
input_field.pack(pady=20, side=LEFT)

input_field.bind("<space>", on_spacebar)
input_field.bind('<Return>', on_spacebar)
input_field.bind("<KeyRelease>", on_key_press)



#-----restart----
restart_icon = Image.open('restart.png')
restart_icon = restart_icon.resize((55,55), Image.LANCZOS)
restart_icon = ImageTk.PhotoImage(restart_icon)

restart_button = Button(input_frame, image=restart_icon, command=reset_timer)
restart_button.pack(side=RIGHT, padx=10)


#----start----
start_icon = Image.open('start-button.png')
start_icon = start_icon.resize((55,55), Image.LANCZOS)
start_icon= ImageTk.PhotoImage(start_icon)

start_button = Button(input_frame, image=start_icon, command=start_timer)
start_button.pack(side=RIGHT, padx=10)


window.mainloop()

