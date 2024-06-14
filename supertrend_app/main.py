from tkinter import Tk, Label, Frame, StringVar, Scrollbar, Frame, Canvas
from supertrend_app.functions import *
from symbolList import symbol_list

status_label = ""
symbol_list = {
    "Aarti Industries Limited": "AARTIIND.NS",
    "ABB Limited": "ABB.NS",
    "Abbott India Limited": "ABBOTINDIA.NS",
    "Aditya Birla Capital Limited": "ABCAPITAL.NS",
    "Aditya Birla Fashion and Retail Limited": "ABFRL.NS",
    "ACC Limited": "ACC.NS",
    "Adani Enterprises Limited": "ADANIENT.NS",
    "Adani Ports and Special Economic Zone Limited": "ADANIPORTS.NS",
    "Alkem Laboratories Limited": "ALKEM.NS",
    "Ambuja Cements Limited": "AMBUJACEM.NS",
    "Apollo Hospitals Enterprise Limited": "APOLLOHOSP.NS",
    "Apollo Tyres Limited": "APOLLOTYRE.NS",
    "Ashok Leyland Limited": "ASHOKLEY.NS",
    "Asian Paints Limited": "ASIANPAINT.NS",
    "Astral Limited": "ASTRAL.NS",
    "Atul Limited": "ATUL.NS",
    "AU Small Finance Bank Limited": "AUBANK.NS",
    "Aurobindo Pharma Limited": "AUROPHARMA.NS",
    "Axis Bank Limited": "AXISBANK.NS",
}
prize_range_touch = []
count = 1


def onCountdownFunctionCall():
    global status_label, prize_range_touch, symbol_list, count, frame

    count += 1
    prize_range_touch = []

    for name, sbl in symbol_list.items():
        data = fetch_realtime_data(sbl)
        merged_data = calculate_supertrend(data)
        check_range = check_supertrend_range(merged_data)

        if check_range:
            prize_range_touch.append(name)

    if len(prize_range_touch) > 0:
        stock_frame = Frame(frame, bg="#333333")
        stock_frame.pack(pady=50)

        scrollbar_y = Scrollbar(stock_frame)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = Scrollbar(stock_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        stock_canvas = Canvas(
            stock_frame,
            bg="#333333",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            height=400,
            width=900,
        )
        stock_canvas.pack(side="top", fill="both", expand=True)  # Change side to "top"

        scrollbar_y.config(command=stock_canvas.yview)
        scrollbar_x.config(command=stock_canvas.xview)

        stock_inner_frame = Frame(
            stock_canvas, bg="#333333"
        )  # Move stock_inner_frame inside stock_canvas

        stock_inner_frame.bind(
            "<Configure>",
            lambda e: stock_canvas.configure(scrollregion=stock_canvas.bbox("all"))
        )

        stock_canvas.create_window((0, 0), window=stock_inner_frame, anchor="nw")

        def center_window(canvas, window):
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            window_width = window.winfo_reqwidth()
            window_height = window.winfo_reqheight()
            x = (canvas_width - window_width) // 2
            y = (canvas_height - window_height) // 2
            canvas.create_window(x, y, window=window)

        center_window(stock_canvas, stock_inner_frame)

        for name in prize_range_touch:
            label = Label(
                stock_inner_frame,
                text=name,
                font=("Helvetica", 16),
                fg="white",
                bg="#333333",
            )
            label.pack(pady=5)



def countdown():
    global timer, status_label, count
    if timer > 0:
        mins, secs = divmod(timer, 60)
        time_str.set(f"{mins:02d}:{secs:02d}")
        timer -= 1
        root.after(1000, countdown)
    else:
        status_label.config(text=f"re-fetched data, iteration: {count}")
        timer = 60
        onCountdownFunctionCall()
        countdown()


def start_countdown():
    global timer, status_label, count
    status_label.config(text=f"Countdown started, iteration: {count}")
    timer = 60
    onCountdownFunctionCall()
    countdown()


root = Tk()
root.title("Super-trend calculator for stocks")

width = int(root.winfo_screenwidth() * 0.75)
height = int(root.winfo_screenheight() * 0.7)
root.geometry(f"{width}x{height}")

time_str = StringVar()
frame = Frame(root, bg="#333333")
frame.pack(fill="both", expand=True)

countdown_label = Label(
    frame, textvariable=time_str, font=("Helvetica", 48), fg="white", bg="#333333"
)
countdown_label.pack(pady=50)

status_label = "fetching data..."
status_label = Label(
    frame,
    text=f"status: {status_label}",
    font=("Helvetica", 16),
    fg="white",
    bg="#333333",
)
status_label.pack(pady=0)

root.after(100, start_countdown)
root.mainloop()
