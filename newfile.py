from guizero import App, Text, PushButton
from gpiozero import Motor
import cv2
from tkinter import *

motor = Motor(17,18)
motor2 = Motor(22,23)
cam = cv2.VideoCapture(0)
cam.set(3,1024)
cam.set(4,768)

print ("I was printing here")
def move_forward(event, motor_name):
    print("Hey, we are moving forward")
    motor_name.forward(speed=1)

def move_backward(event, motor_name):
    print("Moving backward")
    motor_name.backward(speed=1)
    
def release(event, motor_name):
    print("Stopped")
    motor_name.stop()

button1 = PushButton(app, text = "move forward")
button2 = PushButton(app, text = "move backward")
button3 = PushButton(app, text = "Dummy extender-1")
button4 = PushButton(app, text = "Dummy retractor-2")

# Motor 1
button1.tk.bind("<ButtonPress>", lambda event, arg = motor: move_forward(event, arg))
button2.tk.bind("<ButtonPress>", lambda event, arg = motor: move_backward(event, arg))

button1.tk.bind("<ButtonRelease>", lambda event, arg = motor: release(event, arg))
button2.tk.bind("<ButtonRelease>", lambda event, arg = motor: release(event, arg))

# Motor 2:

button3.tk.bind("<ButtonPress>", lambda event, arg = motor2: move_forward(event, arg))
button4.tk.bind("<ButtonPress>", lambda event, arg = motor2: move_backward(event, arg))

button3.tk.bind("<ButtonRelease>", lambda event, arg = motor2: release(event, arg))
button4.tk.bind("<ButtonRelease>", lambda event, arg = motor2: release(event, arg))

while True:
    ret, frame = cam.read()
    cv2.imshow('Video Test', frame)
    #wait for Escape Key
    if cv2.waitKey(1) & 0xFF == 27 :
        break
cam.release()
cv2.destroyAllWindows()

app.display()


if ok:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config (image = imgtk)
        self.root.after(0, self.video_loop)
