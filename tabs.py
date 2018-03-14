#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from gpiozero import Motor, CPUTemperature
import time
import cv2
from PIL import Image, ImageTk
import numpy as np

class App:
    def __init__(self, root):

        self.setup_grid(root)

        # creating Notebook that holds tabs   
        nb = ttk.Notebook(root)
        nb.grid(row =0, column = 0, columnspan=50, rowspan=50, sticky="NESW")

        # The first tab 
        control_tab = ttk.Frame(nb) 
        nb.add(control_tab, text = 'Control')
        self.createButtons(control_tab)

        # Label for updating the angle 
        self.angle = Label(control_tab)
        self.angle.grid(row = 39, column = 40)
        self.update_angle()

        # The secons tab
        percepts_tab = ttk.Frame(nb)
        nb.add(percepts_tab, text = 'Percepts')
        self.set_camera_image(percepts_tab)

        # Label for updating the temperature 
        # what I trying to sat is the 52 row of the percepts tab. I do not get my mssage across.
        self.temp = Label(percepts_tab, width = 50, height = 10, bg = "blue")
        self.temp.grid(row = 52, column = 0)
        self.temp.grid_propagate(0)
        self.cpu = CPUTemperature()
        self.update_temp()

        info_tab = ttk.Frame(nb)
        nb.add(info_tab, text = 'Info')
        
        self.tree = ttk.Treeview(info_tab)
        self.tree["columns"] = ("one")
        self.tree.column("one", width = 100)
        self.tree.heading("one", text = "Value")
        
        self.id =  self.tree.insert('', 0, text = "Voltage")
      
        self.update_voltage()
        self.tree.pack()

    def update_voltage(self):
        self.tree.set(self.id, column = "one", value=self.cpu.temperature)
        self.tree.after(100, self.update_voltage)
        
    # Replace this method by the formula of angle calculation 
    def update_angle(self):
        new_time = time.strftime('%H:%M:%S')
        self.angle.configure(text = "Angle: "+ new_time)
        self.angle.after(100, self.update_angle)

    def update_temp(self):
        self.temp.configure(text = "Temperature: "+ str(self.cpu.temperature))
        self.temp.after(100, self.update_temp)

    def set_camera_image(self, tab):
        self.setup_grid(tab)
        
        imageFrame = Frame(tab, width = 350, height = 350, bg = "blue")
        imageFrame.grid_propagate(0)
        imageFrame.grid(row = 0, column = 25)

        self.lmain = Label(imageFrame)
        self.lmain.grid(row = 0, column = 25)
        self.cap = cv2.VideoCapture(0)
        self.video_loop()

    def video_loop(self):
        
        ok, fr = self.cap.read()
        fr  = cv2.flip(fr, 1) 
        cv2image = cv2.cvtColor(fr, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image = img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image = imgtk)
        self.lmain.after(10, self.video_loop)     
        
    def move_forward(self, event, motor_name):
        print("Moving forward")
        motor_name.forward(speed=1)

    def move_backward(self, event, motor_name):
        print("Moving backward")
        motor_name.backward(speed=1)

    def release(self, event, motor_name):
        print("Stopped")
        motor_name.stop()

    def createButtons(self, tab):
       
        self.setup_grid(tab); 
        
        self.button1 = Button(tab, text = "North")
        self.button2 = Button(tab, text = "South")
        self.button3 = Button(tab, text = "West")
        self.button4 = Button(tab, text = "East")

        self.button1.grid(row = 10, column = 25)
        self.button2.grid(row = 30, column = 25)
        self.button3.grid(row = 20, column = 15)
        self.button4.grid(row = 20, column = 35)

        # Motor 1
        self.button1.bind("<ButtonPress>", lambda event, arg = motor: self.move_forward(event, arg))
        self.button2.bind("<ButtonPress>", lambda event, arg = motor: self.move_backward(event, arg))

        self.button1.bind("<ButtonRelease>", lambda event, arg = motor: self.release(event, arg))
        self.button2.bind("<ButtonRelease>", lambda event, arg = motor: self.release(event, arg))
      
        # Motor 2
        self.button3.bind("<ButtonPress>", lambda event, arg = motor2: self.move_forward(event, arg))
        self.button4.bind("<ButtonPress>", lambda event, arg = motor2: self.move_backward(event, arg))

        self.button3.bind("<ButtonRelease>", lambda event, arg = motor2: self.release(event, arg))
        self.button4.bind("<ButtonRelease>", lambda event, arg = motor2: self.release(event, arg))


    #assigning weight to the cells in a grid => make sure that the positioning is as expected 
    def setup_grid(self, grid_name):
        row=0
        while row<50:
            grid_name.rowconfigure(row, weight=1)
            grid_name.columnconfigure(row, weight=1)
            row +=1
            
        
main = Tk()
main.title("Python GUI")
main.geometry('500x500')

motor = Motor(17,18)
motor2 = Motor(22,23)

app = App (main)
main.bind()
main.mainloop()



    

