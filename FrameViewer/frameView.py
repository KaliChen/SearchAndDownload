import os
import shutil
import glob
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd
from tkinter import filedialog
import cv2
import numpy as np
import time



class FrameViewer():
    LABEL_WIDTH = 480
    LABEL_HEIGHT = 256
    def __init__(self, master):
        self.parent = master
        image = Image.open("icons/f00dbe87124fe8da600c02a42380b77a.png")
        image = image.resize((self.LABEL_WIDTH, self.LABEL_HEIGHT), Image.ANTIALIAS) ## The (250, 250) is (height, width)
        #self.logo = tk.PhotoImage(file = "icons/f00dbe87124fe8da600c02a42380b77a.png")
        self.logo = ImageTk.PhotoImage(image)

        self.init_frameviewer()
    def init_frameviewer(self):       
        self.LOCAL_VIDEO_NAME = tk.StringVar()
        self.DEV_VIDEO_NAME= tk.StringVar()
        self.DEV_VIDEO_NAME.set("http://192.168.43.1:8080/video/mjpeg")
        self.StreamCtrlPanel = tk.LabelFrame(self.parent , text="Stream Control Panel",font=('Courier', 8))
        self.StreamCtrlPanel.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
              
        self.selStr = tk.StringVar()
        #self.selStr.set("From Local Camera")		
        fromlocalCam = tk.Radiobutton(self.StreamCtrlPanel, text = "Local Camera",font=('Courier', 8), variable = self.selStr, value = "From Local Camera", command = self.init_VideoCapture)
        fromlocalCam.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)

        fromdevCam = tk.Radiobutton(self.StreamCtrlPanel, text = "Device Camera",font=('Courier', 8), variable = self.selStr, value = "From Device Camera", command = self.init_VideoCapture)
        fromdevCam.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)
        self.DeviceVideoPath= tk.Entry(self.StreamCtrlPanel , textvariable=self.DEV_VIDEO_NAME, width = 10)
        self.DeviceVideoPath.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)        
        
        fromlocalVideofile = tk.Radiobutton(self.StreamCtrlPanel, text = "Local File",font=('Courier', 8), variable = self.selStr, value = "From Local File", command = self.load_video)
        fromlocalVideofile.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)

        self.LocalVideoPath= tk.Entry(self.StreamCtrlPanel , textvariable=self.LOCAL_VIDEO_NAME, width = 10)
        self.LocalVideoPath.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)
        

        self.VideoCtrlPanel = tk.LabelFrame(self.parent  , text="VideoControl Panel",font=('Courier', 8))
        self.VideoCtrlPanel.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
		       
        showframebutton = tk.Button(self.VideoCtrlPanel, text = "PLAY",font=('Courier', 8), command = self.show_frame)
        showframebutton.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)
        
        capreleabutton = tk.Button(self.VideoCtrlPanel, text ="STOP",font=('Courier', 8), command = self.cap_release)
        capreleabutton.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)

        split_framebutton = tk.Button(self.VideoCtrlPanel, text ="Split",font=('Courier', 8), command = self.split_frame)
        split_framebutton.pack(side=tk.LEFT, expand=tk.NO, fill = tk.X)

        self.streamplay_tab = tk.Frame(self.parent)
        self.streamplay_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.stream = tk.Label(self.streamplay_tab, image=self.logo,
                                width=self.LABEL_WIDTH, height=self.LABEL_HEIGHT)
        self.stream.pack(side=tk.LEFT, expand=tk.NO, fill = tk.BOTH)
       
    def show_frame(self, event = None):
        _, frame = self.cap.read()
        #frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame = cv2.resize(frame,(self.LABEL_WIDTH,self.LABEL_HEIGHT))
        # timestamp
        Time = time.time()
        # datetime 物件
        local_time = time.ctime(Time)
        """
        cv2.putText(frame, str(local_time), (10, 50), 
                    self.fontcv2Var.get(), #int(self.fontcv2spinbox.get()),
                    int(self.fontsizespinbox.get()), 
                    self.HTMLColorToRGB(self.color1[1]), 
                    int(self.linesizespinbox.get()),
                    self.fontlinetypecv2Var.get())#int(self.fontlinetypecv2spinbox.get()))
        """
        cv2.putText(frame, str(local_time), (10, 10), 
                    1, #int(self.fontcv2spinbox.get()),
                    1, 
                    (255,255,255), 
                    1,
                    0)#int(self.fontlinetypecv2spinbox.get()))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.stream.imgtk = imgtk
        self.stream.configure(image=imgtk)
        self.stream.after(15, self.show_frame)

        
    def cap_release(self, event = None):
        self.cap.release()
        self.stream.configure(image=self.NICE_logo)
        #self.stream.after(0, None)
        #self.Destroy_All_Windows()
    def Destroy_All_Windows(self, event = None):
        cv2.destroyAllWindows()

    def split_frame(self, event = None):
        if self.selStr.get() =="From Local Camera": self.cap = cv2.VideoCapture(0)
        elif self.selStr.get() =="From Local File": self.cap = cv2.VideoCapture(self.localvideoname)
        #調整預設影像大小，預設值很大，很吃效能 
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.LABEL_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.LABEL_HEIGHT)

        if not os.path.exists(os.getcwd()+"/split_frame"): os.mkdir("split_frame")
        while(self.cap.isOpened()): #當攝影機打開時，對每個frame進行偵測    
            T = int(100*time.time())
            #讀出frame資訊
            ret, frame = self.cap.read()
            #輸出到畫面
            cv2.imshow("Split frame", frame)
            cv2.imwrite('split_frame/'+str(T)+'.jpg', frame) #write the frames into facerecognition
            #如果按下ESC键，就退出
            if cv2.waitKey(1) == 27: break
        #釋放記憶體
        self.cap.release()
        #關閉所有視窗
        cv2.destroyAllWindows() 
        
    def init_VideoCapture(self, event = None):
        
        if self.selStr.get() =="From Local Camera": self.cap = cv2.VideoCapture(0)

        elif self.selStr.get() =="From Local File": self.cap = cv2.VideoCapture(self.localvideoname)
       
        elif self.selStr.get() =="From Device Camera": self.cap = cv2.VideoCapture(self.DEV_VIDEO_NAME.get())
        """     
        elif self.selStr.get() =="From Device Video File":
            print(self.selStr.get())
        """

        #self.show_frame()
    def load_video(self, event = None):
        self.localvideoname =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp4 files","*.mp4*"),("all files","*.*")))
        self.LOCAL_VIDEO_NAME.set(self.localvideoname)
        #print(self.localvideoname)
        self.init_VideoCapture()


if __name__ == '__main__':
    root = tk.Tk()
    FrameViewer(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()

