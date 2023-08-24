import tkinter as tk
from tkinter import *
import customtkinter as ct
from PIL import *
#Functions definitions
def slider_event_RT(value):
    valRT=tk.StringVar(value=int(value))
    labelRT = ct.CTkLabel(master=root,
                               textvariable=valRT,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelRT.place(relx=0.12, rely=0.63)
    labelRTM.place_forget()
def slider_event_CB(value):
    valCB=tk.StringVar(value=int(value))
    labelCB = ct.CTkLabel(master=root,
                               textvariable=valCB,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelCB.place(relx=0.4, rely=0.63)
    labelCBM.place_forget()

    
def stopRT():
    valRTM=tk.StringVar(value=0)
    labelRTM = ct.CTkLabel(master=root,
                               textvariable=valRTM,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelRTM.place(relx=0.12, rely=0.63)
    sliderRT.set(0)
    print("Stop RT")
def stopCB():
    valCBM=tk.StringVar(value=0)
    labelCBM = ct.CTkLabel(master=root,
                               textvariable=valCBM,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
    labelCBM.place(relx=0.4, rely=0.63)
    sliderCB.set(0)
    print("Stop CB")
def GoFront():
    print("CB Front")
def GoBack():
    print("CB Back")    
def GoLeft():
    print("RT Left")
def GoRight():
    print("RT Right")   



#GUI configuration
ct.set_appearance_mode('white')

ct.set_default_color_theme("green")
root= ct.CTk()
root.title("Dobot Didactech")
root.geometry("1200x600")
text_var = tk.StringVar(value="Welcome! You will then be able to select the conveyor belt or the rotary table,\n in order to test the speed and performance of both. ")

label = ct.CTkLabel(master=root,
                               textvariable=text_var,
                               width=80,
                               height=40,
                               font=('Comic Sans MS', 15),
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
label.place(relx=0.28, rely=0.05, anchor=tk.CENTER)

text_var2 = tk.StringVar(value="In this part, you can test the Dobot Magician's movements\n and observe the value of its entries.")

label2 = ct.CTkLabel(master=root,
                               textvariable=text_var2,
                               width=80,
                               height=40,
                               font=('Comic Sans MS', 15),
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
label2.place(relx=0.8, rely=0.05, anchor=tk.CENTER)





#Rotary table configuration

imgRT= tk.PhotoImage(file="images/RT.png")
lbl_imgRT= tk.Label(root, image=imgRT)
lbl_imgRT.place(relx=0.08,rely=0.15)

buttonRTL = ct.CTkButton(master=root, text="Clockwise", fg_color="green", command=GoLeft)
buttonRTL.place(relx=0.08, rely=0.55, anchor=CENTER)
buttonRTR = ct.CTkButton(master=root, text="Counterclockwise", fg_color="green", command=GoRight)
buttonRTR.place(relx=0.22, rely=0.55, anchor=CENTER)
buttonRT = ct.CTkButton(master=root, text="Stop", fg_color="red", command=stopRT)
buttonRT.place(relx=0.15, rely=0.8, anchor=CENTER)
sliderRT = ct.CTkSlider(master=root, from_=0, to=40, command=slider_event_RT)
sliderRT.place(relx=0.15, rely=0.7, anchor=tk.CENTER)
sliderRT.set(0)
valRTM=tk.StringVar(value=0)
labelRTM = ct.CTkLabel(master=root,
                               textvariable=valRTM,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
labelRTM.place(relx=0.12, rely=0.63)
VarURT = tk.StringVar(value="rpm")

labelURT = ct.CTkLabel(master=root,
                               textvariable=VarURT,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
labelURT.place(relx=0.14, rely=0.63)
valPWM = tk.StringVar(value=0)
labelPWM = ct.CTkLabel(master=root,
                               textvariable=valPWM,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "black"),
                               corner_radius=8)
labelPWM.place(relx=0.14, rely=0.9)



#Conveyor Belt configuration
imgCB= tk.PhotoImage(file="images/CB.png")
lbl_imgCB= tk.Label(root, image=imgCB)
lbl_imgCB.place(relx=0.36,rely=0.15)

buttonCBDF = ct.CTkButton(master=root, text="Go fordward", fg_color="green", command=GoFront)
buttonCBDF.place(relx=0.5, rely=0.55, anchor=CENTER)
buttonCBDB = ct.CTkButton(master=root, text="Go backward", fg_color="green", command=GoBack)
buttonCBDB.place(relx=0.36, rely=0.55, anchor=CENTER)
buttonCB = ct.CTkButton(master=root, text="Stop", fg_color="red", command=stopCB)
buttonCB.place(relx=0.43, rely=0.8, anchor=CENTER)

sliderCB = ct.CTkSlider(master=root, from_=0, to=75, command=slider_event_CB)
sliderCB.set(0)
sliderCB.place(relx=0.43, rely=0.7, anchor=tk.CENTER)
valCBM=tk.StringVar(value=0)

labelCBM = ct.CTkLabel(master=root,
                               textvariable=valCBM,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
labelCBM.place(relx=0.4, rely=0.63)
VarUCB = tk.StringVar(value="mm/s")

labelUCB = ct.CTkLabel(master=root,
                               textvariable=VarUCB,
                               width=20,
                               height=25,
                               fg_color=("#ececec", "#ececec"),
                               corner_radius=8)
labelUCB.place(relx=0.42, rely=0.63)



root.iconbitmap('images/logo.ico')
root.mainloop()
