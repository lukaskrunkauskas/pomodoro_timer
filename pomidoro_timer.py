from tkinter import *
from enum import Enum
from time import sleep
from loguru import logger
import threading


class State(Enum):
    WORK = 'work'
    BREAK = 'break'


break_time = 5
work_time = 10
is_working = True
loop_state = State.WORK

root = Tk()
root.title("Pomodoro")
root.geometry("300x300")
root.resizable(0, 0)
root.config(bg='blanched almond')
sec = StringVar()
working_state_label_variable = StringVar()
s = Entry(root, textvariable=sec, width=2, font='arial 12')
sec.set('00')
mins = StringVar()
m = Entry(root, textvariable=mins, width=2, font='arial 12')
mins.set('00')
hrs = StringVar()
h = Entry(root, textvariable=hrs, width=2, font='arial 12')
hrs.set('00')

breakTime = Entry(root, width=3, borderwidth=5)
breakTime.grid(row=1, column=1)
sessionTime = Entry(root, width=3, borderwidth=5)
sessionTime.grid(row=1, column=4)
clock = Entry(root, width=10, borderwidth=5)
clock.grid(row=5, column=2)
working_state_label = Label(root, bg='antique white', font='arial 10 bold', textvariable=working_state_label_variable)


def update_timer_ui(t, state):
    clock.delete(0, END)
    clock.insert(0, t)
    working_state_label_variable.set(state)


def break_counter(sign):
    global break_time
    breakTime.delete(0, END)
    if break_time == 0 and sign == -1:
        break_time = 0
    else:
        break_time = break_time + sign
    breakTime.insert(0, break_time)


def session_counter(sign):
    global work_time
    sessionTime.delete(0, END)
    if work_time == 0 and sign == -1:
        work_time = 0
    else:
        work_time = work_time + sign
    sessionTime.insert(0, work_time)


def time_loop(time):
    global is_working
    global loop_state
    while time > 0 and is_working:
        sleep(1)
        time -= 1
        update_timer_ui(time, loop_state)


def play():
    def start():
        global is_working
        global loop_state
        while is_working:
            if loop_state == State.WORK:
                logger.debug("looping working timer")
                time_loop(work_time)
                loop_state = State.BREAK
            else:
                logger.debug("looping break timer")
                time_loop(break_time)
                loop_state = State.WORK
            if not is_working:
                break

    thread = threading.Thread(target=start)
    thread.start()


def start_button():
    global is_working
    is_working = True
    play()


def cancel_button():
    global is_working
    is_working = False
    play()


# creating a label widget

myLabel1 = Label(root, text="Break length(min)", bg='antique white', font='arial 10 bold')
myLabel2 = Label(root, text="Session length(min)", bg='antique white', font='arial 10 bold')
# myLabel3 = Label(root, font='arial 15 bold', text='set the time', bg='papaya whip')
myLabel4 = Label(root, text="Time for work !")
minusBreakButton = Button(root, text="-", command=lambda: break_counter(-1))
plusBreakButton = Button(root, text="+", command=lambda: break_counter(1))
minusSessionButton = Button(root, text="-", command=lambda: session_counter(-1))
plusSessionButton = Button(root, text="+", command=lambda: session_counter(1))
startButton = Button(root, text='START', bd='5', command=start_button, bg='antique white', font='arial 10 bold')
cancelButton = Button(root, text="CANCEL", bd='5', command=cancel_button, bg='antique white', font='arial 10 bold')

# printing on screen
myLabel1.grid(row=0, column=0, columnspan=2)
myLabel2.grid(row=0, column=3, columnspan=3)
# myLabel3.grid(row = 2, columnspan = 6)
minusBreakButton.grid(row=1, column=0)
plusBreakButton.grid(row=1, column=2)
minusSessionButton.grid(row=1, column=3)
plusSessionButton.grid(row=1, column=5)
working_state_label.grid(row=5, column=0)
# h.grid(row = 3, column=1)
# m.grid(row = 3, column=2)
# s.grid(row = 3, column=4)
startButton.grid(row=4, column=1)
cancelButton.grid(row=4, column=2)

root.mainloop()
