import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
#import platform
import ImgViewer.imgview as IV #(1)
import FrameViewer.frameView as FV #(2)
import SearchDocs.SearchDocs as SearDoc #(8)
import SearchSceneMark.SearchSceneMark as SearSM #(10)
import SearchVideo.SearchVideo as SearV #(11)

import tkinter.messagebox as tkmsg
from PIL import Image, ImageTk, ImageDraw, ExifTags, ImageColor,ImageFont
#from pdf2image import convert_from_path, convert_from_bytes
#from pdf2image.exceptions import PDFInfoNotInstalledError,PDFPageCountError,PDFSyntaxError
import tempfile
from glob import glob
import glob
#import ffmpeg
import os
from os.path import splitext
import platform
#import subprocess


class TestTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Test Tool Platform:"+str(platform.system()))        
        #self.NICE_wallpaper = tk.PhotoImage(file = "icons/pr6-01.png")
        #self.NICE_logo = tk.PhotoImage(file = "icons/1002nice_logo_full_light.png")
        #self.Allion_logo = tk.PhotoImage(file = "icons/logo_footer.png")
        w = 1180 # width for the Tk root
        h = 860 # height for the  Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #self.geometry("1440x1020")

        #self.init_menubar()
        #if platform.system() == "Windows": self.iconbitmap('icons\\screen_webcam_web_camera_icon_148791.ico')

        '''self.notebook'''
        self.notebook = Notebook(self)
        self.notebook.pack(side = tk.TOP,fill=tk.BOTH, expand=tk.YES)


        self.init_FrameViewer()
        self.init_ImgViewer()
        #self.init_Search_tab()
        self.init_SearchDocs_tab()
        self.init_SearchSceneMark_tab()
        self.init_SearchVideo_tab()
 
    def init_FrameViewer(self):
        self.init_FrameViewer_tab = tk.Frame(self.notebook)
        self.init_FrameViewer_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.notebook.add(self.init_FrameViewer_tab, text="init_FrameViewer")
        self.FrameSwitch = tk.StringVar()

        fvfram1 = tk.Frame(self.init_FrameViewer_tab )
        fvfram1.grid(row =0, column = 0, sticky = tk.E+tk.W)
        self.fv1 = FV.FrameViewer(fvfram1)
        fvfram1_2 = tk.Frame(self.init_FrameViewer_tab )
        fvfram1_2.grid(row =1, column = 0, sticky = tk.E+tk.W)
        switch1 = tk.Radiobutton(fvfram1_2, text = "Frame\n Switch 1",font=('Courier', 9), variable = self.FrameSwitch, value = "Frame Switch 1", command = self.frameswitch)
        switch1.pack(side=tk.RIGHT, expand=tk.NO, fill = tk.X)

        fvfram2 = tk.Frame(self.init_FrameViewer_tab )
        fvfram2.grid(row =2, column = 0, sticky = tk.E+tk.W)
        self.fv2 = FV.FrameViewer(fvfram2)
        fvfram2_2 = tk.Frame(self.init_FrameViewer_tab )
        fvfram2_2.grid(row =3, column = 0, sticky = tk.E+tk.W)
        switch2 = tk.Radiobutton(fvfram2_2, text = "Frame\n Switch 2",font=('Courier', 9), variable = self.FrameSwitch, value = "Frame Switch 2", command = self.frameswitch)
        switch2.pack(side=tk.RIGHT, expand=tk.NO, fill = tk.X)
        
        fvfram3 = tk.Frame(self.init_FrameViewer_tab )
        fvfram3.grid(row =0, column = 1, sticky = tk.E+tk.W)
        self.fv3 = FV.FrameViewer(fvfram3)
        fvfram3_2 = tk.Frame(self.init_FrameViewer_tab )
        fvfram3_2.grid(row =1, column = 1, sticky = tk.E+tk.W)
        switch3 = tk.Radiobutton(fvfram3_2, text = "Frame\n Switch 3",font=('Courier', 9), variable = self.FrameSwitch, value = "Frame Switch 3", command = self.frameswitch)
        switch3.pack(side=tk.RIGHT, expand=tk.NO, fill = tk.X)

  
        fvfram4 = tk.Frame(self.init_FrameViewer_tab )
        fvfram4.grid(row =2, column = 1, sticky = tk.E+tk.W)
        self.fv4 = FV.FrameViewer(fvfram4)
        fvfram4_2 = tk.Frame(self.init_FrameViewer_tab )
        fvfram4_2.grid(row =3, column = 1, sticky = tk.E+tk.W)
        switch4 = tk.Radiobutton(fvfram4_2, text = "Frame\n Switch 4",font=('Courier', 9), variable = self.FrameSwitch, value = "Frame Switch 4", command = self.frameswitch)
        switch4.pack(side=tk.RIGHT, expand=tk.NO, fill = tk.X)
        
    
    def frameswitch(self):
        if self.FrameSwitch.get() =="Frame Switch 1": StreamFile = self.fv1.cap#self.iv1.image_paths[self.iv1.image_idx]
        elif self.FrameSwitch.get() =="Frame Switch 2": StreamFile = self.fv2.cap#self.iv2.image_paths[self.iv2.image_idx]
        elif self.FrameSwitch.get() =="Frame Switch 3": StreamFile = self.fv3.cap#self.iv3.image_paths[self.iv3.image_idx]
        elif self.FrameSwitch.get() =="Frame Switch 4": StreamFile = self.fv4.cap#self.iv4.image_paths[self.iv4.image_idx]
        #print(StreamFile)
        """
        self.dlib_frame.cap = StreamFile
        self.frameopencv.cap = StreamFile
        """
    def init_ImgViewer(self):
        self.init_ImgViewer_tab = tk.Frame(self.notebook)
        self.init_ImgViewer_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.notebook.add(self.init_ImgViewer_tab, text="init_ImgViewer")
        self.ImgSwitch = tk.StringVar()
        ivfram1 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1.grid(row =0, column = 0, sticky = tk.E+tk.W)
        self.iv1 = IV.ImageViewer(ivfram1)
        ivfram1_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1_2.grid(row =0, column = 1, sticky = tk.E+tk.W)        
        opendir1 = tk.Button(ivfram1_2, text = "Open\n dir 1",font=('Courier', 9), command = self.iv1.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch1 = tk.Radiobutton(ivfram1_2, text = "Img\n Switch 1",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 1", command = self.imgswitch)
        switch1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

        ivfram3 = tk.Frame(self.init_ImgViewer_tab )
        ivfram3.grid(row =0, column = 2, sticky = tk.E+tk.W)
        self.iv3 = IV.ImageViewer(ivfram3)
        ivfram3_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram3_2.grid(row =0, column = 3, sticky = tk.E+tk.W)        

        opendir3 = tk.Button(ivfram3_2, text = "Open\n dir 3",font=('Courier', 9), command = self.iv3.open_dir)
        opendir3.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        switch3 = tk.Radiobutton(ivfram3_2, text = "Img\n Switch 3",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 3", command = self.imgswitch)
        switch3.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

        ivfram2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2.grid(row =1, column = 0, sticky = tk.E+tk.W)
        self.iv2 = IV.ImageViewer(ivfram2)
        ivfram2_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2_2.grid(row =1, column = 1, sticky = tk.E+tk.W)        
        
        opendir2 = tk.Button(ivfram2_2, text = "Open\n dir 2",font=('Courier', 9), command = self.iv2.open_dir)
        opendir2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch2 = tk.Radiobutton(ivfram2_2, text = "Img\n Switch 2",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 2", command = self.imgswitch)
        switch2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
  
        ivfram4 = tk.Frame(self.init_ImgViewer_tab )
        ivfram4.grid(row =1, column = 2, sticky = tk.E+tk.W)
        self.iv4 = IV.ImageViewer(ivfram4)
        ivfram4_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram4_2.grid(row =1, column = 3, sticky = tk.E+tk.W)        

        opendir1 = tk.Button(ivfram4_2, text = "Open\n dir 4",font=('Courier', 9), command = self.iv4.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch4 = tk.Radiobutton(ivfram4_2, text = "Img\n Switch 4",font=('Courier', 9), variable = self.ImgSwitch, value = "Img switch 4", command = self.imgswitch)
        switch4.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

    def imgswitch(self):
        if self.ImgSwitch.get() =="Img Switch 1": imageFile = self.iv1.image_paths[self.iv1.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 2": imageFile = self.iv2.image_paths[self.iv2.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 3": imageFile = self.iv3.image_paths[self.iv3.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 4": imageFile = self.iv4.image_paths[self.iv4.image_idx]
        """
        self.awsrk.imageFile = imageFile
        self.alpr.imageFile = imageFile
        self.iss.imageFile = imageFile
        self.haar.imageFile = imageFile
        self.DlibImg.imageFile = imageFile
        self.ocrtess.imageFile = imageFile
        self.clrP.imageFile = imageFile
        """ 
    def init_Search_tab(self):
        self.Search_tab = tk.Frame(self.notebook)
        self.Search_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.notebook.add(self.Search_tab, text = "Search")

        """
        self.Searchnotebook = Notebook(self.Search_tab)
        self.Searchnotebook.pack(side = tk.TOP,fill=tk.BOTH, expand=tk.YES)
        """
        self.init_SearchDocs_tab()
        #self.init_SearchJson_tab()
        self.init_SearchSceneMark_tab()
        self.init_SearchVideo_tab()

    def init_SearchDocs_tab(self):
        self.SearchDocs_tab = tk.Frame(self.notebook)
        #self.SearchDocs_tab.grid(row =0, column = 0,rowspan = 2, sticky = tk.E+tk.W)
        self.notebook.add(self.SearchDocs_tab, text = "Search Docs")
        self.SD = SearDoc.SearchDocs(self.SearchDocs_tab)

    def init_SearchSceneMark_tab(self):
        self.SearchSceneMark_tab = tk.Frame(self.notebook)
        #self.SearchSceneMark_tab.grid(row =0, column = 1, sticky = tk.E+tk.W)
        self.notebook.add(self.SearchSceneMark_tab, text = "Search SceneMark")
        self.SSM = SearSM.SearchSceneMark(self.SearchSceneMark_tab)

    def init_SearchVideo_tab(self):
        self.SearchVideo_tab = tk.Frame(self.notebook)
        #self.SearchVideo_tab.grid(row =1, column = 1, sticky = tk.E+tk.W)
        self.notebook.add(self.SearchVideo_tab, text = "Search Video")
        self.SV = SearV.SearchVideo(self.SearchVideo_tab)

if __name__ == "__main__":
       
    TT = TestTool()
    TT.mainloop()

