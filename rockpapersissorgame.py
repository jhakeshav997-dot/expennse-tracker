import tkinter as tk
import random
from tkinter import messagebox

# स्कोर ट्रैक करने के लिए वेरिएबल्स
user_score = 0
comp_score = 0

# गेम का मुख्य लॉजिक (फंक्शन)
def play(user_choice):
    global user_score, comp_score
    
    # कंप्यूटर का रैंडम चुनाव
    choices = ["Rock 🪨", "Paper 📄", "Scissors ✂️"]
    comp_choice = random.choice(choices)
    
    # विजेता तय करने के नियम
    if user_choice == comp_choice:
        result = "मैच टाई (बराबर) रहा! 🤝"
    elif (user_choice == "Rock 🪨" and comp_choice == "Scissors ✂️") or \
         (user_choice == "Paper 📄" and comp_choice == "Rock 🪨") or \
         (user_choice == "Scissors ✂️" and comp_choice == "Paper 📄"):
        result = "बधाई हो! आप जीत गए! 🎉"
        user_score += 1
    else:
        result = "कंप्यूटर जीत गया! 🤖"
        comp_score += 1
        
    # स्क्रीन पर रिजल्ट और स्कोर अपडेट करना
    lbl_result.config(text=f"आपका चुनाव: {user_choice}\nकंप्यूटर का चुनाव: {comp_choice}\n\n{result}")
    lbl_score.config(text=f"स्कोर 🏆 -> आप: {user_score} | कंप्यूटर: {comp_score}")

# स्कोर रीसेट करने का फंक्शन
def reset_game():
    global user_score, comp_score
    user_score = 0
    comp_score = 0
    lbl_result.config(text="अपना दांव चुनें और खेल शुरू करें! 👇")
    lbl_score.config(text="स्कोर 🏆 -> आप: 0 | कंप्यूटर: 0")

# --- UI सेटअप (डार्क थीम) ---
root = tk.Tk()
root.title("🎮 Rock, Paper, Scissors Game")
root.geometry("450x500")
root.resizable(False, False)
root.config(bg="#1E1E2E")  # वही पुराना सुंदर डार्क बैकग्राउंड

# फोंट्स
FONT_MAIN = ("Segoe UI", 12, "bold")
FONT_SCORE = ("Segoe UI", 14, "bold")

# टाइटल
lbl_title = tk.Label(root, text="Rock, Paper, Scissors 🕹️", font=("Segoe UI", 18, "bold"), bg="#1E1E2E", fg="#FF79C6")
lbl_title.pack(pady=20)

# रिजल्ट दिखाने की जगह
lbl_result = tk.Label(root, text="अपना दांव चुनें और खेल शुरू करें! 👇", font=("Segoe UI", 12), bg="#2D2D3F", fg="#FFFFFF", width=38, height=6, bd=0, relief="solid")
lbl_result.pack(pady=15)

# लाइव स्कोरबोर्ड
lbl_score = tk.Label(root, text="स्कोर 🏆 -> आप: 0 | कंप्यूटर: 0", font=FONT_SCORE, bg="#1E1E2E", fg="#BD93F9")
lbl_score.pack(pady=10)

# बटनों के लिए एक फ्रेम (ताकि तीनों बटन एक लाइन में दिखें)
frame_buttons = tk.Frame(root, bg="#1E1E2E")
frame_buttons.pack(pady=20)

# बटन 1: Rock
btn_rock = tk.Button(frame_buttons, text="🪨 Rock", font=FONT_MAIN, bg="#8BE9FD", fg="#1E1E2E", width=10, command=lambda: play("Rock 🪨"), cursor="hand2")
btn_rock.grid(row=0, column=0, padx=5, ipady=5)

# बटन 2: Paper
btn_paper = tk.Button(frame_buttons, text="📄 Paper", font=FONT_MAIN, bg="#FFB86C", fg="#1E1E2E", width=10, command=lambda: play("Paper 📄"), cursor="hand2")
btn_paper.grid(row=0, column=1, padx=5, ipady=5)

# बटन 3: Scissors
btn_scissors = tk.Button(frame_buttons, text="✂️ Scissors", font=FONT_MAIN, bg="#FF5555", fg="#FFFFFF", width=10, command=lambda: play("Scissors ✂️"), cursor="hand2")
btn_scissors.grid(row=0, column=2, padx=5, ipady=5)

# रीसेट बटन
btn_reset = tk.Button(root, text="🔄 Reset Game", font=("Segoe UI", 10, "bold"), bg="#50FA7B", fg="#1E1E2E", command=reset_game, cursor="hand2")
btn_reset.pack(pady=15, ipady=3)

root.mainloop()
