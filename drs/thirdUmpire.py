import tkinter
import PIL.Image, PIL.ImageTk
import cv2
from functools import partial
import threading
import time
import imutils

stream = cv2.VideoCapture("clip.mp4")
flag = True


def play(speed):
    global flag

    print(f"You clicked on play. Speed is {speed}")
    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag


def pending(decision):

    # 1. Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)

    # 2. Wait for 1 second
    time.sleep(1)

    # 3. Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)
    
    # 4. Wait for 3 second
    time.sleep(3)

    # 5. Display out/not out image
    if decision == "not out":
        decision_image = "not_out.png"

    else :
        decision_image = "out.png"   

    frame = cv2.cvtColor(cv2.imread(decision_image), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image=frame, anchor=tkinter.NW)


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")    


# Width and height for the screen
SET_WIDTH = 650
SET_HEIGHT = 368

# Tkinter GUI starts here
window = tkinter.Tk()
window.title("Princy Jain Third Umpire Review System")
cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image= photo)
canvas.pack()

# buttons to control the playback
btn = tkinter.Button(window, text="<< Previous (Fast)", width= 60, command=partial(play, -20))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow)", width= 60, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (Fast) >>", width= 60, command=partial(play, 20))
btn.pack()

btn = tkinter.Button(window, text="Next (Slow) >>", width= 60, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width= 60, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give not Out", width= 60, command=not_out)
btn.pack()

window.mainloop()