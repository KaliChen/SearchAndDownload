import paramiko 
import scp
from paramiko import SSHClient
from scp import SCPClient
import os

import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import ttk
import tkinter.messagebox as tkmsg


class SearchDocs():
    def __init__(self, master):
        self.parent = master
        self.keyword = tk.StringVar()
        self.Path = tk.StringVar()
        self.Path.set('/')
        self.ADDRESS = tk.StringVar()
        self.ADDRESS.set('')        
        self.USER = tk.StringVar()
        self.USER.set('')
        self.PASSWD = tk.StringVar()
        self.PASSWD.set('')
        self.SearchSceneMarkPanel = tk.LabelFrame(self.parent, text="Search Docs",font=('Courier', 10))
        self.SearchSceneMarkPanel.pack(side=tk.TOP, expand=tk.NO, fill = tk.BOTH) 
        self.init_ctrlPanel()
        self.init_DocSearch_tab()
        

    def init_ctrlPanel(self):
        self.ctrlPanel = tk.LabelFrame(self.SearchSceneMarkPanel, text="Control Panel",font=('Courier', 10), width = 60)
        self.ctrlPanel.pack(side=tk.TOP, expand=tk.YES, fill = tk.BOTH)        
        tk.Label(self.ctrlPanel, text='IP Address', font=('Courier', 10),width=10, height=2).grid(row = 0, column = 0, sticky = tk.E+tk.W)
        self.Address = tk.Entry(self.ctrlPanel, textvariable=self.ADDRESS,font=('Courier', 10), width = 15)
        self.Address.grid(row = 0, column = 1, sticky = tk.E+tk.W)
        tk.Label(self.ctrlPanel, text='User', font=('Courier', 10),width=5, height=2).grid(row = 0, column = 2, sticky = tk.E+tk.W)
        self.User = tk.Entry(self.ctrlPanel, textvariable=self.USER,font=('Courier', 10), width = 10)
        self.User.grid(row = 0, column = 3, sticky = tk.E+tk.W)
        tk.Label(self.ctrlPanel, text='Password', font=('Courier', 10),width=8, height=2).grid(row = 0, column = 4, sticky = tk.E+tk.W)
        self.Passwd = tk.Entry(self.ctrlPanel, textvariable=self.PASSWD, show = "*",font=('Courier', 10), width = 10)
        self.Passwd.grid(row = 0, column = 5, sticky = tk.E+tk.W)
        self.ConfButton = tk.Button(self.ctrlPanel, text = "Config",font=('Courier', 10), command= self.Config)
        self.ConfButton.grid(row = 1, column = 2, sticky = tk.E+tk.W)    
        #43)
        self.ssh_loginButton =tk.Button(self.ctrlPanel, text = "ssh_login",font=('Courier', 10), width = 10, command = self.ssh_login)
        self.ssh_loginButton.grid(row = 1, column = 3, sticky = tk.E+tk.W)
        #44)
        self.ssh_closeButton =tk.Button(self.ctrlPanel, text = "ssh_close",font=('Courier', 10), command = self.ssh_close)
        self.ssh_closeButton.grid(row = 1, column = 4, sticky = tk.E+tk.W)

        #self.DevVerType = ttk.Combobox(self.ctrlPanel,font=('Courier', 10), values = ["0.2.0", "0.2.1"], width = 10,state = "readonly") 
        #self.DevVerType.grid(row = 1, column = 5, sticky = tk.E+tk.W)
        #self.DevVerType.current(0)

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
    def Doc_Search(self, event = None):
        #print(self.keyword.get())
        #print(self.Path.get())
        rawcommand = 'find {path} -name {pattern}'
        #rawcommand2 = 'grep –r –I “{key1}” {path}'
                
        command = rawcommand.format(path=self.Path.get(), pattern=self.keyword.get())
        #command2 = rawcommand2.format(path=self.Path.get(), key1=self.keyword.get())
        #print(command2)
        
        stdin, stdout, stderr = self.ssh.exec_command(command)
        #stdin, stdout, stderr = self.ssh.exec_command(command2)
        
        #filelist = stdout.read()#.splitlines()
        filelist = stdout.readlines()
        for afile in filelist:
            (head, filename) = os.path.split(afile)
            #print(filename)
            #print(afile)
            self.Table_of_Docs.insert("", index = 'end', text = filename,  values = (afile))

    def Select_Docs(self, event = None):
        for item in self.Table_of_Docs.selection():
            self.item_text = self.Table_of_Docs.item(item, "values")
            #print(self.item_text[0])
        #tkmsg.showinfo("Information",self.item_text[0])
        stdin, stdout, stderr = self.ssh.exec_command("cat "+self.item_text[0].rstrip('\n'))
        echo = stdout.read().decode()
        self.DocText.insert(tk.END,echo)
                
    def Doc_Download(self, event = None):
        #print("Doc_Download")
        if not os.path.exists(os.getcwd()+"/Docs"):
            os.mkdir("Docs")
        (head, filename) = os.path.split(self.item_text[0])
        self.scp.get(self.item_text[0].rstrip('\n'), "Docs/"+filename)        
        tkmsg.showinfo("Information",self.item_text[0]+"Download Finished")
        
    def Doc_Clear(self, event = None):
        #print("Doc_Clear")
        self.DocText.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR")
        
    def Doc_item_DEL(self, event = None):
        selected_item = self.Table_of_Docs.selection()[0] ## get selected item
        self.Table_of_Docs.delete(selected_item)
        
    def init_DocSearch_tab(self):
        self.DocSearch_tab = tk.Frame(self.SearchSceneMarkPanel)
        self.DocSearch_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        #self.notebook.add(self.DocSearch_tab, text="Doc Search")        

        self.Docs = tk.LabelFrame(self.DocSearch_tab, text="Documents",font=('Courier', 10), height = 10)
        self.Docs.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)         
        
        self.searDButton = tk.Button(self.Docs, text = "Search",font=('Courier', 10), command = self.Doc_Search)
        self.searDButton.grid(row = 0, column = 0, sticky = tk.E+tk.W)
        
        self.DLJButton = tk.Button(self.Docs, text = "Download",font=('Courier', 10), command = self.Doc_Download)
        self.DLJButton.grid(row = 0, column = 1, sticky = tk.E+tk.W)        

        self.Doc_item_del =tk.Button(self.Docs, text = "Item Delete",font=('Courier', 10), command=self.Doc_item_DEL)
        self.Doc_item_del.grid(row = 0, column = 2, sticky = tk.E+tk.W)
        
        self.DocPreviewCLEAR =tk.Button(self.Docs, text = "Preview Clear",font=('Courier', 10), command = self.Doc_Clear)
        self.DocPreviewCLEAR.grid(row = 0, column = 3, sticky = tk.E+tk.W)
        
        tk.Label(self.Docs, text='Path', font=('Courier', 10),width=8, height=2).grid(row = 1, column = 0, sticky = tk.E+tk.W)
        self.UpPath = tk.Entry(self.Docs, textvariable=self.Path,font=('Courier', 10))
        self.UpPath.grid(row = 1, column = 1, sticky = tk.E+tk.W)
        
        tk.Label(self.Docs, text='filename key\n (ex:*.log)', font=('Courier', 10),width=15, height=2).grid(row = 1, column = 2, sticky = tk.E+tk.W)
        self.Key = tk.Entry(self.Docs, textvariable=self.keyword,font=('Courier', 10))
        self.Key.grid(row = 1, column = 3, sticky = tk.E+tk.W)
        
        #tk.Label(self.Docs, text='key of content', font=('Courier', 7),width=15, height=2).pack(side=tk.LEFT, expand=tk.NO)
        #self.Keywd1 = tk.Entry(self.Docs, textvariable=self.keyword,font=('Courier', 8))
        #self.Keywd1.pack(side=tk.LEFT, expand=tk.NO)
        
        self.Table_of_Docs = ttk.Treeview(self.DocSearch_tab,columns = ["#1"],height = 10)
        self.Table_of_Docs.heading("#0", text = "Search of Documents")#icon column
        self.Table_of_Docs.heading("#1", text = "Path")
        self.Table_of_Docs.column("#0", width = 320)#icon column
        self.Table_of_Docs.column("#1", width = 820)
        self.Table_of_Docs.tag_configure('T', font = 'Courier,4')
        self.Table_of_Docs.bind("<Double-1>",self.Select_Docs)
        self.Table_of_Docs.pack(side=tk.TOP, expand=tk.NO)

        self.DocTextFrame = tk.LabelFrame(self.DocSearch_tab, text="Doc Preview", font=('Courier', 10))
        self.DocTextFrame.pack(side=tk.TOP, expand=tk.YES, fill = tk.BOTH)
        self.DocText = tk.Text(self.DocTextFrame, height = 20) 
        DocText_sbarV = Scrollbar(self.DocTextFrame, orient=tk.VERTICAL)
        DocText_sbarH = Scrollbar(self.DocTextFrame, orient=tk.HORIZONTAL)
        DocText_sbarV.config(command=self.DocText.yview)
        DocText_sbarH.config(command=self.DocText.xview)
        self.DocText.config(yscrollcommand=DocText_sbarV.set)
        self.DocText.config(xscrollcommand=DocText_sbarH.set)
        DocText_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        DocText_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.DocText.pack(side=tk.TOP, expand=tk.YES, fill = tk.BOTH)
              

if __name__ == '__main__':
    root = tk.Tk()
    SearchDocs(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()
