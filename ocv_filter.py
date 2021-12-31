from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import ctypes
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter import ttk
import cv2
import numpy as np
ctypes.windll.shcore.SetProcessDpiAwareness(1)


class ocvf:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x900")
        self.root.title("OCV Filter GUI")
        self.root.iconbitmap('icon.ico')

        # Image Preview Label
         
        

        # Browse File Function

        def browseFiles():
            global filename
            filename = filedialog.askopenfilename(initialdir=r"/",
                                                  title="Select Image",
                                                  filetypes=(("PNG",
                                                              "*.png*"),
                                                             ("JPG",
                                                              "*.jpg*")
                                                             ))
            self.img = Image.open(filename)
            self.img = self.img.resize((850, 450), Image.ANTIALIAS)
            self.ph_img = ImageTk.PhotoImage(self.img)
            global label_prev
            label_prev = Label(self.root, image=self.ph_img)
            label_prev.place(x=50, y=20, width=850, height=450)

        # Save Files Function
        def save():
            files = [
                ('PNG', '*.png'),
                ('JPG', '*.jpg')]
            file = asksaveasfile(filetypes=files, defaultextension=files)


        # Water Color Art Function
        def water():
            try:
                self.img = cv2.imread(filename)

                self.image_resized = cv2.resize(self.img, (850,430))
                # Phase 2
                self.image_cleared = cv2.medianBlur(self.image_resized, 3)
                self.image_cleared = cv2.medianBlur(self.image_cleared, 3)
                self.image_cleared = cv2.medianBlur(self.image_cleared, 3)

                self.image_cleared = cv2.edgePreservingFilter(self.image_cleared, sigma_s=5)

                # phase 3
                self.image_filtered = cv2.bilateralFilter(self.image_resized, 3, 20, 5)

                for i in range(2):
                    self.image_filtered = cv2.bilateralFilter(self.image_filtered, 5, 40, 10)

                for i in range(3):
                    self.image_filtered = cv2.bilateralFilter(self.image_filtered, 5, 30, 10)

                # phase 4
                gaussian_mask = cv2.GaussianBlur(self.image_filtered, (7, 7), 2)
                self.image_sharp = cv2.addWeighted(
                    self.image_filtered, 1.5, gaussian_mask, -0.5, 0)
                self.image_sharp = cv2.addWeighted(
                    self.image_filtered, 1.4, gaussian_mask, -0.2, 10)

                # Rearranging color channels
                b,g,r = cv2.split(self.image_sharp)
                self.image_sharp = cv2.merge((r,g,b))
                
                self.water_img = ImageTk.PhotoImage(image = Image.fromarray(self.image_sharp))
                # label_prev.config(image = self.water_img)                
                label_prev = Label(self.root, image=self.water_img)
                label_prev.place(x=50, y=20, width=850, height=450)
                
            except:
                 messagebox.showinfo(
                "Welcome", "Error!,\nNo Image selected")   

            # __________________________________________________________________

        # Grascale Image 
        def grayscale():
            try:
                image = cv2.imread(filename)
                self.image_grascale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
                
                self.image_grascale = cv2.resize(self.image_grascale,(850,430))
                self.ph_grascale = ImageTk.PhotoImage(image = Image.fromarray(self.image_grascale))
                # label_prev.config(image = self.water_img)                
                label_prev = Label(self.root, image=self.ph_grascale)
                label_prev.place(x=50, y=20, width=850, height=450) 
            except:
                 messagebox.showinfo(
                "Welcome", "Error!,\nNo Image selected")   
        
        #Motion Blur Image
        def mblur():
            try:
                self.image = cv2.imread(filename)
                self.image = cv2.resize(self.image,(850,430))
                self.size = 15
                self.kernel = np.zeros((self.size, self.size))
                self.kernel[int((self.size-1)/2),:] = np.ones(self.size)
                self.kernel= self.kernel/self.size
                self.output = cv2.filter2D(self.image,-1,self.kernel,self.kernel)
                b,g,r = cv2.split(self.output)
                self.output = cv2.merge((r,g,b))
                self.output = ImageTk.PhotoImage(image = Image.fromarray(self.output))              
                label_prev = Label(self.root, image=self.output)
                label_prev.place(x=50, y=20, width=850, height=450) 
            except:
                 messagebox.showinfo(
                "Welcome", "Error!,\nNo Image selected") 

        # Median Blurring (Smoothing) 
        def smooth():
            try:
                image = cv2.imread(filename) 
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                image = cv2.resize(image,(850,430))
                self.output_median = cv2.medianBlur(image,5)
                self.smooth = ImageTk.PhotoImage(image = Image.fromarray(self.output_median))
                # label_prev.config(image = self.water_img) 
                               
                label_prev = Label(self.root, image=self.smooth)
                label_prev.place(x=50, y=20, width=850, height=450) 
            except:
                 messagebox.showinfo(
                "Welcome", "Error!,\nNo Image selected") 

        # Gaussian Blur
        def gblur():
            try:
                image = cv2.imread(filename) 
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                image = cv2.resize(image,(850,430))
                self.output_gaussian = cv2.GaussianBlur(image,(5,5),0)
                self.gblur = ImageTk.PhotoImage(image = Image.fromarray(self.output_gaussian))                
                label_prev = Label(self.root, image=self.gblur)
                label_prev.place(x=50, y=20, width=850, height=450) 
            except:
                 messagebox.showinfo(
                "Welcome", "Error!,\nNo Image selected") 

        # background
        background = Image.open(r'D:\Prog\OpenCV\Project OCV Filter\bg.png')
        background = background.resize((1000, 900), Image.ANTIALIAS)
        self.ph_bg = ImageTk.PhotoImage(background)
        label_bg = Label(self.root, image=self.ph_bg)
        label_bg.place(x=0, y=0, width=1000, height=900)

        # Image Preview window
        bg_preview = Image.open('prev.png')
        bg_preview = bg_preview.resize((850, 420), Image.ANTIALIAS)
        self.bg_preview = ImageTk.PhotoImage(bg_preview)
        label_preview = Label(self.root, image=self.bg_preview)
        label_preview.place(x=50, y=20, width=850, height=420)

        # Browse button
        browse_img = Image.open('browse.png')
        browse_img = browse_img.resize((50, 50), Image.ANTIALIAS)
        self.browse_img = ImageTk.PhotoImage(browse_img)
        browse_img = Button(root, image=self.browse_img, bd=0,
                            cursor="hand2", command=browseFiles, borderwidth=2)
        browse_img.place(x=50, y=800, width=50, height=50)

        # Save Button
        save_img = Image.open('save.png')
        save_img = save_img.resize((50, 50), Image.ANTIALIAS)
        self.save_img = ImageTk.PhotoImage(save_img)
        save_img = Button(root, image=self.save_img, bd=0,
                          cursor="hand2", command=save, borderwidth=2)
        save_img.place(x=150, y=800, width=50, height=50)


        # # button label
        # btn_label = Label(self.root, bg='#0B0D34')
        # btn_label.place(x=50, y=560, width=900, height=250)
    
        # Watercolor art Button
        water_img = Image.open('water.png')
        water_img = water_img.resize((210, 60), Image.ANTIALIAS)
        self.water_img = ImageTk.PhotoImage(water_img)
        water_img = Button(self.root, image=self.water_img, bd=0,
                           cursor="hand2", command=water, borderwidth=2)
        water_img.place(x=50, y=500, width=210, height=60)

        # Grayscal Image Button
        gray_img = Image.open('gray.png')
        gray_img = gray_img.resize((210, 60), Image.ANTIALIAS)
        self.gray_img = ImageTk.PhotoImage(gray_img)
        gray_img = Button(self.root, image=self.gray_img, bd=0,
                           cursor="hand2", command=grayscale, borderwidth=2)
        gray_img.place(x=50, y=600, width=210, height=60)

        # Smoothen Image Button
        smooth_img = Image.open('smooth.png')
        smooth_img = smooth_img.resize((210, 60), Image.ANTIALIAS)
        self.smooth_img = ImageTk.PhotoImage(smooth_img)
        smooth_img = Button(self.root, image=self.smooth_img, bd=0,
                           cursor="hand2", command=smooth, borderwidth=2)
        smooth_img.place(x=50, y=700, width=210, height=60)

        # Motion Blur Image Button
        mblur_img = Image.open('mblur.png')
        mblur_img = mblur_img.resize((210, 60), Image.ANTIALIAS)
        self.mblur_img = ImageTk.PhotoImage(mblur_img)
        mblur_img = Button(self.root, image=self.mblur_img, bd=0,
                           cursor="hand2", command=mblur, borderwidth=2)
        mblur_img.place(x=290, y=500, width=210, height=60)

        # Gaussian Blur Image Button
        gblur_img = Image.open('gblur.png')
        gblur_img = gblur_img.resize((210, 60), Image.ANTIALIAS)
        self.gblur_img = ImageTk.PhotoImage(gblur_img)
        gblur_img = Button(self.root, image=self.gblur_img, bd=0,
                           cursor="hand2", command=gblur, borderwidth=2)
        gblur_img.place(x=290, y=600, width=210, height=60)
        

        # _____________________________________________


if __name__ == '__main__':
    root = Tk()
    obj = ocvf(root)
    # messagebox.showinfo(
    #     "Welcome", "Hi,\nThis OCV Filter GUI is developed by hksoriginal")
    root.resizable(False, False)
    root.mainloop()
