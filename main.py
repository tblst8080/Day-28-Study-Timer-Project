import tkinter as tk
import time
from timer import Timer
import winsound
import os

# Minutes for each activity
my_sessions = (25, 5, 25, 5, 25, 5, 25, 20)

activity = {
    0: "Keep Working!",
    1: "Take a Break!",
}

# Set up timer object
my_timer = Timer()

frame1 = 0
frame2 = 0


def reset():
    # reset clock
    my_timer.reset_clock()

    # reset visuals
    b_start.config(text="Start")

    my_canvas.tag_raise(reading_img)
    my_canvas.tag_raise(timer_text)
    my_canvas.itemconfig(timer_text, text="00:00", fill="white")
    my_canvas.tag_raise(activity_text)
    my_canvas.itemconfig(activity_text, text="Ready to Start?", fill="white")


def check_time():
    # Keep window on top
    root.wm_attributes("-topmost", True)

    if my_timer.is_timing:

        # animation background
        global frame1, frame2

        # while working
        if my_timer.progress % 2 == 0:
            my_canvas.itemconfig(activity_text, fill="white")
            my_canvas.itemconfig(timer_text, fill="white")
            my_canvas.tag_raise(lofi_obj[int(frame1)])
            frame1 += 0.5
            if frame1 == len(lofi_obj):
                frame1 = 0

        # while taking a break
        elif my_timer.progress % 2 == 1:

            my_canvas.itemconfig(activity_text, fill="#00667d")
            my_canvas.itemconfig(timer_text, fill="#00667d")
            my_canvas.tag_raise(sagiri_obj[frame2])
            frame2 += 1

            # loop frames
            if frame2 == len(sagiri_obj):
                frame2 = 0

        # keep track of time
        my_timer.keep_time()

        # display time
        in_seconds = my_sessions[my_timer.progress] * 60
        countdown = time.strftime("%M:%S", time.gmtime(in_seconds - my_timer.lapse))
        my_canvas.tag_raise(timer_text)
        if my_timer.lapse < my_sessions[my_timer.progress] * 60:
            my_canvas.itemconfig(timer_text, text=countdown)

        # display activity
        current_activity = activity[my_timer.progress % 2]
        my_canvas.tag_raise(activity_text)
        my_canvas.itemconfig(activity_text, text=current_activity)

        # configure pause button
        b_start.config(text="Pause")

        # proceed to next item in the sequence when time is done
        if my_timer.lapse > my_sessions[my_timer.progress] * 60:
            my_timer.is_timing = False
            my_timer.is_new = True

            winsound.PlaySound("doorbell.wav", flags=winsound.SND_FILENAME | winsound.SND_ASYNC)
            root.deiconify()
            my_canvas.itemconfig(activity_text, text="Session is over!")

            my_timer.reset_time()
            my_timer.progress += 1
            b_start.config(text="Continue")

    # skip code if t_reference has not been set (until start)
    else:
        # during pause
        if my_timer.is_paused:
            my_canvas.tag_raise(pause_img)
            my_canvas.tag_lower(activity_text)
            b_start.config(text="Continue")

    # update timer every second
    root.after(ms=37, func=check_time)


# Setting up window
root = tk.Tk()
root.title("Il Pomodoro")
root.iconbitmap("my_icon.ico")
root.minsize(width=500, height=300)
root.maxsize(width=500, height=300)
root.geometry('-1-50')

# Canvas for images
my_canvas = tk.Canvas(width=500, height=300)

# Lofi girl
lofi_count = sum(len(files) for _, _, files in os.walk('./Lofigirl'))  # count the number of files in the .gif folder

lofi_img = []
lofi_obj = []
for x in range(1, lofi_count + 1):
    lofi_img.append(tk.PhotoImage(file=f'Lofigirl/Layer {x}.png'))
    lofi_obj.append(my_canvas.create_image(250, 150, image=lofi_img[x - 1]))

# Sagiri
sagiri_count = sum(len(files) for _, _, files in os.walk('./Sagiri'))  # count the number of files in the .gif folder

sagiri_img = []
sagiri_obj = []
for x in range(1, sagiri_count + 1):
    sagiri_img.append(tk.PhotoImage(file=f'Sagiri/Layer {x}.png'))
    sagiri_obj.append(my_canvas.create_image(250, 150, image=sagiri_img[x - 1]))

# Pause image
pausing = tk.PhotoImage(file='pause.png')
pause_img = my_canvas.create_image(250, 150, image=pausing)

# Cover Page
books = tk.PhotoImage(file='Study.png')
reading_img = my_canvas.create_image(250, 150, image=books)

# Timer text
timer_text = my_canvas.create_text(250, 50, anchor="center", fill="white")
my_canvas.itemconfig(timer_text, text="00:00", font=("Javanese Text", 40, "normal"))

# Activity text
activity_text = my_canvas.create_text(250, 80, anchor="center", fill="white")
my_canvas.itemconfig(activity_text, text="Ready to Start?", font=("Javanese Text", 15, "normal"))

# Reset Button
b_reset = tk.Button(text="Reset", command=reset, height=1, width=10, bg="white", activebackground="brown",
                    activeforeground="yellow", font=("Monotype Corsiva", 11, "normal"))
b_start = tk.Button(text="Start", command=my_timer.start, height=1, width=10, bg="white", activebackground="brown",
                    activeforeground="yellow", font=("Monotype Corsiva", 11, "normal"))

# Automate time-checking function
root.after(ms=1000, func=check_time)

# Layout
my_canvas.place(anchor='center', relx=.5, rely=.5)
b_reset.place(anchor='center', relx=.85, rely=.7, x=-20)
b_start.place(anchor='center', relx=.15, rely=.7, x=20)

# my_window.after(ms=10, func=keep_time)
root.mainloop()
