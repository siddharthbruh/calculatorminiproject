import tkinter as tk

def safe_set(value):
    entry_var.set(str(value))

def click(event):
    global expression
    btn_text = event.widget.cget("text")
    if btn_text == "C":
        clear_all()
    elif btn_text == "=":
        calculate()
    else:
        expression += btn_text
        safe_set(expression)

def calculate():
    global expression
    if not expression.strip():
        return
    try:
        result = eval(expression)
        if isinstance(result, float) and result.is_integer():
            result = int(result)  
        safe_set(result)
        add_history(expression, result)
        expression = str(result)
    except ZeroDivisionError:
        safe_set("Cannot divide by 0")
        add_history(expression, "Error: Divide by 0")
        expression = ""
    except Exception:
        safe_set("Error")
        add_history(expression, "Error")
        expression = ""

def add_history(expr, res):
    if not history_list or history_list[-1] != f"{expr} = {res}":
        history_list.append(f"{expr} = {res}")

def show_history():
    hist_win = tk.Toplevel(root)
    hist_win.title("Calculation History")
    hist_win.geometry("350x600")
    hist_win.resizable(True, True)
    hist_win.config(bg="#f4f4f4")
    
    tk.Label(hist_win, text="History", font=("Arial", 14), bg="#f4f4f4").pack(pady=10)

    text_frame = tk.Frame(hist_win, bg="#f4f4f4")
    text_frame.pack(expand=True, fill="both", padx=10)

    hist_text = tk.Text(text_frame, font=("Arial", 12), bg="#fafafa", fg="#444",
                        wrap="word", state="normal")
    hist_text.pack(expand=True, fill="both")

    def refresh_history():
        hist_text.configure(state="normal")
        hist_text.delete(1.0, tk.END)
        for item in history_list:
            hist_text.insert(tk.END, item + "\n")
        hist_text.configure(state="disabled")

    refresh_history()

    btn_frame = tk.Frame(hist_win, bg="#f4f4f4")
    btn_frame.pack(fill="x", pady=5)

    tk.Button(btn_frame, text="Clear History", font=("Arial", 12),
              bg="#ffdad6", fg="#a33",
              command=lambda: [history_list.clear(), refresh_history()]).pack(pady=5)

    
def clear_history(hist_text_widget=None):
    history_list.clear()
    if hist_text_widget:
        hist_text_widget.configure(state="normal")
        hist_text_widget.delete(1.0, tk.END)
        hist_text_widget.configure(state="enabled")

def clear_all():
    global expression
    expression = ""
    safe_set("")

def backspace():
    global expression
    if expression:
        expression = expression[:-1]
        safe_set(expression)

def extra_function(func):
    global expression
    try:
        if not expression.strip():
            return
        value = float(expression)
        if func == "square":
            result = value ** 2
        elif func == "recip":
            if value == 0:
                raise ZeroDivisionError
            result = 1 / value
        elif func == "sqrt":
            if value < 0:
                raise ValueError
            result = value ** 0.5
        elif func == "%":
            result = value / 100
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        safe_set(result)
        add_history(f"{func}({expression})", result)
        expression = str(result)
    except ZeroDivisionError:
        safe_set("Cannot divide by 0")
        add_history(expression, "Error: Divide by 0")
        expression = ""
    except Exception:
        safe_set("Error")
        add_history(expression, "Error")
        expression = ""


expression = ""
history_list = []

root = tk.Tk()
root.title("Simple Calculator")
root.geometry("350x520")

root.iconbitmap(r"mini project/Calculator_512.ico")

root.resizable(False, False)
root.config(bg="#f4f4f4")

entry_var = tk.StringVar()
entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 22),
                 bd=0, relief="ridge", bg="#fafafa", fg="#333",
                 justify="right")
entry.place(x=15, y=20, width=320, height=50)

btn_cfg = {
    "font": ("Arial", 16),
    "bd": 0,
    "bg": "#e0e0e0",
    "fg": "#333",
    "activebackground": "#d1d1d1",
    "activeforeground": "#111",
    "width": 5,
    "height": 2
}

buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', 'C', '+'],
    ['=', '√', 'x²', '1/x'],
    ['%']
]

y = 85
for row in buttons:
    x = 15
    for btn_text in row:
        if btn_text == '√':
            cmd = lambda f="sqrt": extra_function(f)
        elif btn_text == 'x²':
            cmd = lambda f="square": extra_function(f)
        elif btn_text == '1/x':
            cmd = lambda f="recip": extra_function(f)
        elif btn_text == '%':
            cmd = lambda f="%": extra_function(f)
        elif btn_text == '=':
            cmd = calculate
        elif btn_text == 'C':
            cmd = clear_all
        else:
            cmd = None
        
        btn = tk.Button(root, text=btn_text, **btn_cfg)
        btn.place(x=x, y=y)
        if cmd:
            btn.config(command=cmd)
        else:
            btn.bind("<Button-1>", click)
        x += 80
    y += 60

show_hist_btn = tk.Button(root, text="Show History", font=("Arial", 12),
                          bg="#cce5ff", fg="#004085",
                          command=show_history)
show_hist_btn.place(x=15, y=460, width=320, height=40)

# ---------- Keyboard bindings ----------
root.bind("<Return>", lambda e: calculate())
root.bind("<BackSpace>", lambda e: backspace())
root.bind("<Escape>", lambda e: clear_all())

root.mainloop()
