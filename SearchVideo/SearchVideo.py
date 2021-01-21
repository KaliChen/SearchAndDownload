import paramiko 
import scp
from paramiko import SSHClient
from scp import SCPClient
import os
from os.path import splitext
import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
from tkinter.colorchooser import *

import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd

class SearchVideo():
    def __init__(self, master):
        self.parent = master

        self.ADDRESS = tk.StringVar()
        self.ADDRESS.set('')        
        self.USER = tk.StringVar()
        self.USER.set('')
        self.PASSWD = tk.StringVar()
        self.PASSWD.set('')
        self.Path = tk.StringVar()
        self.Path.set('/') 

        self.SearchVideoPanel = tk.LabelFrame(self.parent, text="Search Video",font=('Courier', 10))
        self.SearchVideoPanel.pack(side=tk.LEFT, expand=tk.YES, fill = tk.BOTH) 

        self.init_ctrlPanel()
        self.init_Stream_tab()

    def init_ctrlPanel(self):
        self.ctrlPanel = tk.LabelFrame(self.SearchVideoPanel, text="Control Panel",font=('Courier', 10))
        self.ctrlPanel.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)        

        tk.Label(self.ctrlPanel, text='IP Address', font=('Courier', 10),width=10, height=2).grid(row = 0, column = 0, sticky = tk.E+tk.W)
        self.Address = tk.Entry(self.ctrlPanel, textvariable=self.ADDRESS,font=('Courier', 10))
        self.Address.grid(row = 0, column = 1, sticky = tk.E+tk.W)
        tk.Label(self.ctrlPanel, text='User', font=('Courier', 10),width=6, height=2).grid(row = 0, column = 2, sticky = tk.E+tk.W)
        self.User = tk.Entry(self.ctrlPanel, textvariable=self.USER,font=('Courier', 10))
        self.User.grid(row = 0, column = 3, sticky = tk.E+tk.W)
        tk.Label(self.ctrlPanel, text='Password', font=('Courier', 10),width=8, height=2).grid(row = 0, column = 4, sticky = tk.E+tk.W)
        self.Passwd = tk.Entry(self.ctrlPanel, textvariable=self.PASSWD, show = "*", width = 12,font=('Courier', 10))
        self.Passwd.grid(row = 0, column = 5, sticky = tk.E+tk.W)
        self.ConfButton = tk.Button(self.ctrlPanel, text = "Config",font=('Courier', 10), command= self.Config)
        self.ConfButton.grid(row = 1, column = 2, sticky = tk.E+tk.W)    
        #43)
        self.ssh_loginButton =tk.Button(self.ctrlPanel, text = "ssh_login",font=('Courier', 10), command = self.ssh_login)
        self.ssh_loginButton.grid(row = 1, column = 3, sticky = tk.E+tk.W)
        #44)
        self.ssh_closeButton =tk.Button(self.ctrlPanel, text = "ssh_close",font=('Courier', 10), command = self.ssh_close)
        self.ssh_closeButton.grid(row = 1, column = 4, sticky = tk.E+tk.W)

    def ssh_login(self, event = None):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        self.ssh.load_system_host_keys()
        echo = self.ssh.connect(hostname=self.ADDRESS, username=self.USER, password=self.PASSWD)
        #print(echo)
        # SCPCLient takes a paramiko transport as an argument
        self.scp = SCPClient(self.ssh.get_transport())
        tkmsg.showinfo("Information","ssh "+self.USER+"@"+self.ADDRESS+" Connection is setup")

    def ssh_close(self, event = None):
        echo = self.ssh.close()
        print(echo)
        tkmsg.showinfo("Information","ssh "+self.USER+"@"+self.ADDRESS+" Connection is closed")


    def Config(self, event = None):
        self.ADDRESS = self.Address.get()
        self.USER = self.User.get()
        self.PASSWD = self.Passwd.get()
        tkmsg.showinfo("Information","IP Address:"+self.ADDRESS+" User:"+self.USER+" Pass Word:"+self.PASSWD)

    
    def DisplayVideoInfo_Clear(self, event = None):
        #print("Doc_Clear")
        self.DisplaySceneMarkInfo.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR") 
       
    def Search_DeviceVideo(self, event = None):
        rawcommand = 'find {path} -name {pattern}'

        command = rawcommand.format(path=self.Path.get(), pattern='*.mp4')

        stdin, stdout, stderr = self.ssh.exec_command(command)
        #filelist = stdout.read()#.splitlines()
        filelist = stdout.readlines()
        
        #if not os.path.exists(os.getcwd()+"/DeviceVideo"):
        #    os.mkdir("DeviceVideo")
        for afile in filelist:
            (head, filename) = os.path.split(afile)
            #print(filename)
            #print(afile)
            self.Table_of_DiscoverVideo.insert("", index = 'end', text = filename,  values = (afile))
            #####self.scp.get(afile.rstrip('\n'), "DeviceVideo/"+filename)
            #print("DeviceVideo/"+filename)

    def SelectDevVideo(self, event = None):
        for item in self.Table_of_DiscoverVideo.selection(): self.item_text = self.Table_of_DiscoverVideo.item(item, "values")
        tkmsg.showinfo("Information",self.item_text[0])
                
    def Download_DeviceVideo(self, event = None):
        #print("Download_DeviceVideo")
        if not os.path.exists(os.getcwd()+"/DeviceVideo"): os.mkdir("DeviceVideo")
        (head, filename) = os.path.split(self.item_text[0])
        self.scp.get(self.item_text[0].rstrip('\n'), "DeviceVideo/"+filename)
        tkmsg.showinfo("Information",self.item_text[0]+"Download Finished")
 
        
    def init_Stream_tab(self):       
        self.Stream_tab = tk.Frame(self.SearchVideoPanel)
        #self.notebook.add(self.Stream_tab, text="Stream")
        self.Stream_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

        self.StreamCtrlPanel = tk.LabelFrame(self.Stream_tab  , text="Stream Control Panel",font=('Courier', 10))
        self.StreamCtrlPanel.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
 
        tk.Label(self.StreamCtrlPanel, text='Path', font=('Courier', 10),width=8).pack(side=tk.LEFT, expand=tk.NO, fill = tk.BOTH)
        self.UpPath = tk.Entry(self.StreamCtrlPanel, textvariable=self.Path,font=('Courier', 10))
        self.UpPath.pack(side=tk.LEFT, expand=tk.NO, fill = tk.BOTH)
        
        SearDevVideobutton = tk.Button(self.StreamCtrlPanel,font=('Courier', 10), text = "Search Video", command = self.Search_DeviceVideo)
        SearDevVideobutton.pack(side=tk.LEFT, expand=tk.NO, fill = tk.BOTH)

        DowlDevVideobutton = tk.Button(self.StreamCtrlPanel,font=('Courier', 10), text = "Download", command = self.Download_DeviceVideo)
        DowlDevVideobutton.pack(side=tk.LEFT, expand=tk.NO, fill = tk.BOTH)
       
        self.Table_of_DiscoverVideo = ttk.Treeview(self.Stream_tab ,columns = ["#1"],height = 30)
        self.Table_of_DiscoverVideo.heading("#0", text = "Search of Videos", )#icon column
        self.Table_of_DiscoverVideo.heading("#1", text = "Path")
        self.Table_of_DiscoverVideo.column("#0", width = 320)#icon column
        self.Table_of_DiscoverVideo.column("#1", width = 820)
        self.Table_of_DiscoverVideo.tag_configure('T', font = 'Courier,4')
        self.Table_of_DiscoverVideo.bind("<Double-1>",self.SelectDevVideo)
        self.Table_of_DiscoverVideo.pack(side=tk.TOP, expand=tk.NO, fill = tk.Y)

if __name__ == '__main__':
    root = tk.Tk()
    SearchVideo(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()
