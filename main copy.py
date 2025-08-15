import tkinter as tk
import random 
import time 
from database import store_data, get_last10
from tkinter import messagebox

easy_level = ["cats drink milk",
    "hello world",
    "the sky is blue",
    "practice makes progress",
    "I like ice cream",
    "the sun is bright",
    "dogs wag their tails",
    "birds can fly",
    "read every day",
    "time to sleep",
    "wash your hands",
    "water is cold",
    "my shoes are red",
    "keep your hands relaxed",
    "home row helps accuracy",
    "stay safe and happy",
    "a smile is kind",
    "fish swim in water",
    "rain falls from clouds",
    "type fast and smile"]

medium_level = ["Measure what matters: time, errors, and accuracy.",
    "Random prompts reduce memorization bias.",
    "Typing speed improves with consistent practice.",
    "Good posture prevents fatigue during typing.",
    "Design your app to start timing on first keypress.",
    "SQLite stores sessions so progress is visible.",
    "Accuracy comes from both focus and patience.",
    "Reading more will improve your vocabulary.",
    "A healthy lifestyle helps concentration.",
    "Practice every day for better results.",
    "Stay calm when making small mistakes.",
    "Challenge yourself with longer sentences.",
    "Consistency is better than intensity for learning.",
    "Clear goals help track your improvement.",
    "Discipline builds long-term skills."]

hard_level = [ "Concurrency complicates correctness; careful testing is critical.",
    "Human-computer interaction values clarity over cleverness.",
    "A robust metric pipeline logs raw data before rounding.",
    "Edge cases appear precisely when you ignore them.",
    "Accessibility is a design constraint, not a feature.",
    "Typing proficiency results from mindful repetition over time.",
    "The quick brown fox jumps over the lazy dog repeatedly.",
    "Algorithmic efficiency becomes critical at scale.",
    "Design patterns help structure large-scale applications.",
    "Error handling must account for both expected and unexpected input.",
    "Multithreaded code requires careful synchronization.",
    "User experience depends on clarity, speed, and reliability.",
    "Premature optimization is the root of many software issues.",
    "Accurate logging is essential for debugging complex systems.",
    "System design should prioritize maintainability."]


started = False
start_time = 0
chosen_sentence = ''
entry_field = None
output_label = None
submit_button = None
prompt_label = None
results_wpm_value = None
results_acc_value = None
history_listbox = None

def timer_start(event):
    global started, start_time
    if started == False:
        start_time = time.time()
        started = True
        
def calculate_results():
    global chosen_sentence, entry_field, output_label, submit_button, start_time, started


    text_entered = entry_field.get("1.0", tk.END).strip()
    if not text_entered:
        output_label.config(text="Type something first")
        return

    end_time = time.time()

    if not started:
        started = True
        start_time = end_time - 0.001 

    typing_time = max(0.001, end_time - start_time)
    typing_minutes = typing_time / 60.0

    typed_words = text_entered.split()
    word_count = len(typed_words)
    wpm = word_count / typing_minutes


    correct_chars = 0
    actual_characters = len(chosen_sentence)

    upto = min(len(text_entered), actual_characters)
    for i in range(upto):
        if text_entered[i] == chosen_sentence[i]:
            correct_chars += 1

    denom = max(actual_characters, len(text_entered), 1)  
    accuracy = (correct_chars / denom) * 100.0

    store_data(wpm, accuracy)

    output_label.config(text=f"WPM: {int(round(wpm))} | Accuracy: {int(round(accuracy))}%")
    submit_button.config(state="disabled")



def getting_diff_level_sentences():
    level = level_choice.get()
    if level == "easy":
        return random.choice(easy_level)
    elif level == "medium":
        return random.choice(medium_level)
    else:
        return random.choice(hard_level) 


def set_new_sentence():
    global chosen_sentence, started, start_time

    chosen_sentence = getting_diff_level_sentences()

    prompt_label.config(text=chosen_sentence)

    started = False

    start_time = 0

    entry_field.delete("1.0", tk.END)

    submit_button.config(state="normal")

    output_label.config(text="WPM: - | Accuracy: -")

    entry_field.focus_set()


def submit_and_next(event=None):
    global started, start_time

    text_entered = entry_field.get("1.0", tk.END).strip()
    if not text_entered:
        output_label.config(text="Type something first")
        return "break"

    now = time.time()
    if not started:
        started = True
        start_time = now - 0.001

    minutes = max(0.001, now - start_time) / 60.0
    wpm = len(text_entered.split()) / minutes

    correct = 0
    upto = min(len(text_entered), len(chosen_sentence))
    for i in range(upto):
        if text_entered[i] == chosen_sentence[i]:
            correct += 1
    denom = max(len(chosen_sentence), len(text_entered), 1)
    acc = (correct / denom) * 100.0

    store_data(wpm, acc)

    wpm_int = int(round(wpm))
    acc_int = int(round(acc))
    output_label.config(text=f"WPM: {wpm_int} | Accuracy: {acc_int}%")

    
    results_wpm_value.config(text=str(wpm_int))
    results_acc_value.config(text=f"{acc_int}%")

    set_new_sentence()          
    show_page(results_page)     
    return "break"



def on_submit():
    try:
        calculate_results()
        set_new_sentence()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        

def show_history():
    win = tk.Toplevel()

    win.title("Last 10 Sessions")

    win.geometry("340x280")

    lb = tk.Listbox(win, width=44)
    lb.pack(fill="both", expand=True, padx=10, pady=10)
    rows = get_last10()

    if not rows:
        lb.insert("end", "No history yet.")
    else:
        for ts, w, a in rows:
            lb.insert("end", f"{ts} — WPM {w}, Acc {a}%")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Typing IA")
    root.geometry("820x520")


    container = tk.Frame(root)
    container.pack(fill="both", expand=True)
    container.rowconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)

    typing_page  = tk.Frame(container)
    results_page = tk.Frame(container)
    history_page = tk.Frame(container)

    for f in (typing_page, results_page, history_page):
        f.grid(row=0, column=0, sticky="nsew")

    def show_page(frame):
        frame.tkraise()

    level_choice = tk.StringVar(value="easy")

    top = tk.Frame(typing_page)
    top.pack(fill="x", padx=12, pady=8)

    tk.Label(top, text="Level:").pack(side="left")
    level_menu = tk.OptionMenu(top, level_choice, "easy", "medium", "hard", command=lambda _: set_new_sentence())
    level_menu.pack(side="left", padx=6)

    next_btn = tk.Button(top, text="Next", command=set_new_sentence)
    next_btn.pack(side="left", padx=6)

    hist_btn = tk.Button(top, text="History", command=lambda: (populate_history(), show_page(history_page)))
    hist_btn.pack(side="left", padx=6)

    prompt_box = tk.LabelFrame(typing_page, text="Prompt")
    prompt_box.pack(fill="x", padx=12, pady=6)
    prompt_label = tk.Label(prompt_box, text="", wraplength=760, anchor="w", justify="left")
    prompt_label.pack(fill="x", padx=10, pady=8)

    type_box = tk.LabelFrame(typing_page, text="Type here (press Enter to submit)")
    type_box.pack(fill="x", padx=12, pady=6)
    entry_field = tk.Text(type_box, height=4, wrap="word")
    entry_field.pack(fill="x", padx=10, pady=8)
    entry_field.bind("<KeyPress>", timer_start)
    entry_field.bind("<Return>", submit_and_next)

    output_label = tk.Label(typing_page, text="WPM: - | Accuracy: -")
    output_label.pack(anchor="w", padx=18, pady=4)

    submit_button = tk.Button(typing_page, text="Submit", command=submit_and_next)

    submit_button.pack(anchor="e", padx=12, pady=6)


    tk.Label(results_page, text="Results / Feedback", font=("Arial", 16, "bold")).pack(pady=14)

    res_box = tk.Frame(results_page); res_box.pack(pady=8)
    tk.Label(res_box, text="WPM:", font=("Arial", 13)).grid(row=0, column=0, sticky="e", padx=6, pady=6)
    results_wpm_value = tk.Label(res_box, text="-", font=("Arial", 13, "bold"))
    results_wpm_value.grid(row=0, column=1, sticky="w", padx=6, pady=6)

    tk.Label(res_box, text="Accuracy:", font=("Arial", 13)).grid(row=1, column=0, sticky="e", padx=6, pady=6)
    results_acc_value = tk.Label(res_box, text="-", font=("Arial", 13, "bold"))
    results_acc_value.grid(row=1, column=1, sticky="w", padx=6, pady=6)

    res_btns = tk.Frame(results_page); res_btns.pack(pady=10)
    tk.Button(res_btns, text="Next Sentence", command=lambda: (show_page(typing_page))).grid(row=0, column=0, padx=8)
    tk.Button(res_btns, text="View History", command=lambda: (populate_history(), show_page(history_page))).grid(row=0, column=1, padx=8)

    
    tk.Label(history_page, text="Last 10 Sessions", font=("Arial", 16, "bold")).pack(pady=14)
    history_listbox = tk.Listbox(history_page, width=60, height=12)
    history_listbox.pack(padx=12, pady=10, fill="both", expand=True)

    hist_btns = tk.Frame(history_page); hist_btns.pack(pady=8)
    tk.Button(hist_btns, text="Back to Typing", command=lambda: show_page(typing_page)).grid(row=0, column=0, padx=8)

    def populate_history():
        history_listbox.delete(0, "end")
        rows = get_last10()
        if not rows:
            history_listbox.insert("end", "No history yet.")
        else:
            for ts, w, a in rows:
                history_listbox.insert("end", f"{ts} — WPM {w}, Acc {a}%")



    set_new_sentence()
    show_page(typing_page)
    root.mainloop()

