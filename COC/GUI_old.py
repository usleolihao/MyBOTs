#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time
import threading
import logging
import tkinter.scrolledtext as ScrolledText

from subprocess import call
from tkinter import *
from tkinter import messagebox
from util import *

from COC.GUI.GUI_util import *
from COC.GUI.GUI_logs import *

from COC.Bot import COC_BOT

global Win
if not Win:
	import appscript

class GUI(tk.Frame):

	def __init__(self):
		self.window = None

		#------------------Loading config------------------------------
		try:
			self.config = load_configure("COC/config/config.json")
		except Exception as e:
			self.config = {}

		#select a language	
		if 'lang' not in self.config.keys() or self.config['lang'] == '':
			self.select_language()	

		#-------------------Loading Language----------------------------------
		#print(self.config)
		try:
			self.lang = load_configure("COC/config/lang/" + self.config['lang'] + ".json")
		except Exception as e:
			messagebox.showinfo("Error", "Did not find the language profile")
			self.config['lang'] = ''
			self.save_config()
			exit()

		#-------------------Selecting Emulator---------------------------------
		
		self.em = None
		self.d = None

		self.SelectDevices()

		#check the version of Uiautomator2
		try:
			call('pip install -U uiautomator2')
			call('pip3 install -U uiautomator2')
		except Exception as e:
			pass
		

		#----------------------Connect-----------------------------------------
			
		#self.d is the Devices that we want to connect
		print("device:",self.d)
		if self.d != None:
			bot = COC_BOT(device = self.d)

		if not Win and self.em != None: #Mac OS activate emulator
			appscript.app(pid=pid).activate()
			
		#-------------------Basic Windows--------------------------------------
		self.window = tk.Tk()
		self.window.title("My CoC Bots")
		self.window.resizable(width = False, height = False)
		self.window.geometry("600x600")
		self.window.option_add('*tearOff', 'FALSE')
		#-------------------Set widgets up----------------------------------
		self.SetUpMenu()
		self.func_button()
		self.logs_area()
		self.test_area()
		self.information_show()
		
	def donothing(self):
		filewin = Toplevel(self.window)
		button = Button(filewin, text="Do nothing button")
		button.pack()

	def SetUpMenu(self):
		menubar = Menu(self.window)

		filemenu = Menu(menubar, tearoff = 0)
		filemenu.add_command(label="New", command = self.donothing)
		filemenu.add_command(label = "Open", command = self.donothing)
		filemenu.add_command(label = "Save", command = self.donothing)
		filemenu.add_command(label = "Save as...", command = self.donothing)
		filemenu.add_command(label = "Close", command = self.donothing)
		filemenu.add_separator()
		filemenu.add_command(label = "Exit", command = self.window.quit)
		menubar.add_cascade(label = "File", menu = filemenu)

		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label = "Undo", command = self.donothing)
		editmenu.add_separator()
		editmenu.add_command(label = "Cut", command = self.donothing)
		editmenu.add_command(label = "Copy", command = self.donothing)
		editmenu.add_command(label = "Paste", command = self.donothing)
		editmenu.add_command(label = "Delete", command = self.donothing)
		editmenu.add_command(label = "Select All", command = self.donothing)
		menubar.add_cascade(label = "Edit", menu = editmenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label = "Help Index", command = self.donothing)
		helpmenu.add_command(label = "About...", command = self.donothing)
		menubar.add_cascade(label = "Help", menu = helpmenu)

		self.window.config(menu = menubar)
				
	def func_button(self):
				CheckVar1 = IntVar()
				CheckVar2 = IntVar()
				CheckVar3 = IntVar()
				CheckVar4 = IntVar()
				CheckVar5 = IntVar()
				CheckVar6 = IntVar()
				donate = Checkbutton(self.window, text = "自动捐兵",variable = CheckVar1, onvalue = 1,
									 offvalue = 0, height = 2, width = 10)
				donate.place(x = 325,y = 0)
				auto_lose = Checkbutton(self.window, text = "自动掉杯",variable = CheckVar2, onvalue = 1,
									 offvalue = 0, height = 2, width = 10)
				auto_lose.place(x = 325,y = 30)
				auto_attack = Checkbutton(self.window, text = "自动打鱼",variable = CheckVar3, onvalue = 1,
									 offvalue = 0, height = 2, width = 10)
				auto_attack.place(x = 325,y = 60)
				extra_func1 = Checkbutton(self.window, text = "更多功能1",variable = CheckVar4, onvalue = 1,
									 offvalue = 0, height = 2, width = 10)
				extra_func1.place(x = 325,y = 90)
				extra_func2 = Checkbutton(self.window, text = "更多功能2",variable = CheckVar5, onvalue = 1,
									 offvalue = 0, height = 2, width = 10)
				extra_func2.place(x = 325,y = 120)
				extra_func3 = Checkbutton(self.window, text = "更多功能3",variable = CheckVar6, onvalue = 1,
									 offvalue = 0, height = 2, width = 10)
				extra_func3.place(x = 325,y = 150)

	def logs_area(self):
			   w = Label(self.window, height = 50, width =33,fg = "white", bg = "black",
				anchor = "nw",text = self.lang['log']+":" )
			   w.place(x = 0,y = 0)

			   self.grid(column=0, row=0, sticky='ew')
			   self.grid_columnconfigure(0, weight=1, uniform='a')
			   self.grid_columnconfigure(1, weight=1, uniform='a')
			   self.grid_columnconfigure(2, weight=1, uniform='a')
			   self.grid_columnconfigure(3, weight=1, uniform='a')
			   # Add text widget to display logging info
			   st = ScrolledText.ScrolledText(self, state='disabled')
			   st.configure(font='TkFixedFont')
			   st.grid(column=0, row=1, sticky='w', columnspan=4)

			   # Create textLogger
			   text_handler = TextHandler(st)

			   # Logging configuration
			   logging.basicConfig(filename='test.log',
					level=logging.INFO, 
					format='%(asctime)s - %(levelname)s - %(message)s')        

			   # Add the handler to logger
			   logger = logging.getLogger()        
			   logger.addHandler(text_handler)
			   
			   

	def test_area(self):
			   canva = Canvas(self.window,width=150,height=300,bg = "gray")
			   canva.place(x = 450,y = 0)
			   canva.create_text(75,30,text = "测试区")
			   button1 = Button(self.window, text = "缩放", command = self.donothing,
								anchor = W)
			   button1.configure(width = 5, activebackground = "#33B5E5", relief = FLAT)
			   button1_window = canva.create_window(35, 60, anchor=NW, window=button1)
			   
			   button2 = Button(self.window, text = "收集资源", command = self.donothing,
								anchor = W)
			   button2.configure(width = 8, activebackground = "#33B5E5", relief = FLAT)
			   button2_window = canva.create_window(35, 100, anchor=NW, window=button2)

			   button3 = Button(self.window, text = "捐兵测试", command = self.donothing,
								anchor = W)
			   button3.configure(width = 8, activebackground = "#33B5E5", relief = FLAT)
			   button3_window = canva.create_window(35, 140, anchor=NW, window=button3)

	def information_show(self):
		canva = Canvas(self.window,width=300,height=300,bg = "yellow")
		canva.place(x = 300,y = 300)
		canva.create_text(150,15,text = "游戏状态")
		canva.create_text(50,50,text = "金钱：")
		canva.create_text(50,70,text = "红水：")
		canva.create_text(50,90,text = "黑水：")
		canva.create_text(73,140,text = "累计掠夺金币：")
		canva.create_text(73,160,text = "累计掠夺红水：")
		canva.create_text(73,180,text = "累计掠夺黑水：")


	def save_config(self):
		with open('COC/config/config.json', 'w',encoding='utf-8') as outfile:
				json.dump(self.config, outfile, ensure_ascii=False, indent=4, sort_keys=True)

	def start(self):
		t1 = threading.Thread(target=worker, args=[])
		t1.start()
		self.window.mainloop()
		t1.join()


	def select_language(self): 
		langs = {
				"中文":'chn',
				"English":'eng'
			}

		def Set_lang(lang):
			self.window.destroy()
			self.config['lang'] = lang
			self.save_config()

		self.window = Selection_Windows("Languages",langs)
		for lang in langs.keys():
			btn = Button(self.window, text = lang,anchor = W,width = 90,
				command = lambda lang=lang:Set_lang(langs[lang])).pack()
		
		self.window.mainloop()

	def SelectDevices(self):

		def Sel_device(d):
				if self.window != None:
					self.window.destroy()

				if type(d) is list:
					self.d = d[2]
					self.em = d[1]
				else:
					self.d = d

		devices = self.util.find_emulator()

		print(devices)

		#found a real Android device
		if len(devices) > 0 and type(devices[0]) is str:
			self.window = Selection_Windows(self.lang['s_dev'],devices)
			for d in devices: 
				btn = Button(self.window, text = d,anchor = W,width = 90,
					command = lambda d=d:Sel_device(d)).pack()
			self.window.mainloop()

		#only one emulator
		elif len(devices) == 1:
			Sel_device(devices[0])

			
		elif len(devices) > 1:
			self.window = Selection_Windows(self.lang['s_dev'],devices)
			count = 1
			for d in devices: 
				c = "{} {} pid/handle:{}".format(d[0] + str(count),d[1],d[2])
				d.append("emulator-" + str(5554 + (count-1)*2))
				btn = Button(self.window, text = c,anchor = W,width = 90,
					command = lambda d=d:Sel_device(d)).pack()
				count += 1
			self.window.mainloop()

		else:
			messagebox.showinfo("Error", "Did not find the devices")
			exit()