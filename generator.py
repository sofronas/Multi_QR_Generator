import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PIL import Image
from PIL import ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime as d
import os
import sys
import sv_ttk
import time
import glob
import pyqrcode

class Application(tk.Frame):
    
    def __init__(self,master):
        super().__init__(master)
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        
        sv_ttk.set_theme("dark")
        root.title("QR Generator") #set window title
        root.geometry("520x800") #set window size
        try:
            root.iconbitmap("assets/qr-code.ico")
        except:
            pass
        # root.resizable(0,0) #remove maximize option
        root.update()
        # Center window
        root.minsize(root.winfo_width(), root.winfo_height())
        x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
        y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
        root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
        # root.config(bg="#015a2a")

        # Label Informing User
        labelEnterText = ttk.Label(root, text="Enter text:", font=("Courier", 48))
        labelEnterText.pack()
        
        # Entry
        global user_input
        user_input = tk.StringVar()
        global entryText
        entryText = ttk.Entry(root, textvariable=user_input,width=80, font=("Ariel", 15))
        entryText.pack(padx=50, pady=30)
        entryText.bind('<Button-3>',self.popup) # Bind a func to right click
        entryText.bind('<Return>', self.enterHitted)

        global menu
        menu = tk.Menu(root,tearoff=0) # Create a menu
        menu.add_command(label='Copy',command=self.copy) # Create labels and commands
        menu.add_command(label='Paste',command=self.paste)

        # Button user to Order a new QR
        global buttonQRgener
        buttonQRgener = ttk.Button(root, text="Generate QR Code", style="Accent.TButton", width=20, command=self.generateQR)
        buttonQRgener.pack(padx=10, pady=10)

        # Label to show img
        global labelImg 
        labelImg = tk.Label(root, bg="#e6e6e6")
        labelImg.pack()
        labelImg.pack_forget()

        global buttonSaveImgQR
        buttonSaveImgQR = ttk.Button(root,text="Save QR",style="Accent.TButton", width=20, command=self.saveQR)
        buttonSaveImgQR.pack()
        buttonSaveImgQR.pack_forget()


    def popup(self, event):
        try:
            menu.tk_popup(event.x_root,event.y_root)
        finally:
            menu.grab_release()

    def enterHitted(self, event):
        root.update_idletasks()
        buttonQRgener.invoke()
        time.sleep(0.1)

    def paste(self):
        try:
            clipboard = root.clipboard_get()
            user_input = clipboard
            entryText.delete(0,"end")
            entryText.insert('end',clipboard)
        except:
            pass

    def copy(self):
        inp = entryText.get()
        root.clipboard_clear()
        root.clipboard_append(inp)
                
    def generateQR(self):
        user = user_input.get()
        qrLots = user.split(",")

        qrQuantity = len(qrLots)
        # print(qrQuantity)
        qrListSize = len(user)
        if qrListSize != 0: # not empty answer from user
            if qrQuantity == 1:
                global qr, img
                qr = pyqrcode.create(user_input.get())
                labelImg.pack(padx=10, pady=30)
                img = tk.BitmapImage(data=qr.xbm(scale=10))
                bitmap = BitmapImage(data=qr.xbm(scale=10))
                # print(qr.terminal())
                try:
                    self.showQR()
                    buttonSaveImgQR.pack()
                except:
                    pass
            elif qrQuantity > 1:
                # create pdf with qr codes
                date = d.now()
                reportName = "report_" + date.strftime("%d_%m_%Y_%H_%M_")
                pathPDF = os.getcwd()
                pathPDF = pathPDF + "\\reports\\" + reportName + ".pdf"
                my_canvas = canvas.Canvas(pathPDF)
                data = [
                            ["N/N","QR Code Text", "QR Code Image"],
                        ]
                flowables = []
                for i in range(0,qrQuantity):
                    qr = pyqrcode.create(qrLots[i])
                    path = os.getcwd()
                    path = path + "\\images\\" + "image_" + str(i) + ".png"
                    # print(path)
                    qr.png(path,scale=10)
                    
                    doc = SimpleDocTemplate(
                            pathPDF,
                            pagesize=letter,
                            )
                    
                    a = Image(path)
                    a.drawHeight = 0.75*inch
                    a.drawWidth = 0.75*inch
                    data.append(
                            [i+1, qrLots[i], a],
                    )
                    
                tbl = Table(data)
                tbl.setStyle(TableStyle([
                        ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                        ('ALIGN', (1,1), (-1,-1), 'CENTER')
                        ]))
                tbl.wrapOn(my_canvas, 50, 200)
                tbl.drawOn(my_canvas,20,50)
                flowables.append(tbl)
                doc.build(flowables)
                os.startfile(pathPDF)

                # remove images created
                imagesPath = os.getcwd() + "\\images\\"
                # print(imagesPath)
                self.removeImages(imagesPath)
        else:
            messagebox.showwarning("Warning", "No data")
            

    def showQR(self):
        labelImg.config(image=img)
        pass

    def saveQR(self):
        root.filename = filedialog.asksaveasfilename(initialdir = "/",title = "Select file", defaultextension=".png", filetypes = (("Png files","*.png"),("all files","*.*")))
        # print(root.filename)
        qr.png(root.filename,scale=10)
        pass

    def removeImages(self, path):
        try:
            dir_list = os.listdir(path)
            for filename in dir_list:
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print("Files not removed")
            print(e)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()