#!/usr/bin/python3
import tkinter as tk # note that module name has changed from Tkinter in Python 2 to tkinter in Python 3
import json,os,time,threading,logging

from PIL import ImageTk
import PIL.Image

from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as ScrolledText
import tkinter.font

from util import *

from GUI.GUI_logs import *

from COC.COC_Bot import COC_BOT


if not sys.platform == 'win32':
	import appscript


class COC_BOT_GUI(tk.Frame):
	# This class defines the graphical user interface 
	def __init__(self,config, *args, **kwargs):
		#------------------Loading config------------------------------
		self.config = config
		self.loading_config()	
		self.loading_languages()
		#-------------------Basic Windows--------------------------------------
		self.window = tk.Tk()
		tk.Frame.__init__(self, self.window, *args, **kwargs)
		self.build_basic_window()
		self.build_left_part()
		self.build_right_part()

	def start(self):
		#t1 = threading.Thread(target=worker, args=[])
		#t1.daemon = True
		#t1.start()
		self.window.mainloop()

	def build_right_part(self):
		self.right_part = Canvas(self.window,bg = "white",width=400,height=800)
		self.right_part.grid(row = 0, column = 1 ,rowspan = 2, sticky=N+S+E+W)
		self.set_information()
		self.set_function()
		self.test_area()

		self.place_image(self.right_part,"COC/res/dragon.png",150,300)


	def place_image(self,frame,image,x,y):
		img =PIL.Image.open(image)
		self.img = ImageTk.PhotoImage(img)
		frame.create_image(x,y,image=self.img,anchor = NW)


	def test_area(self):
		self.right_part.create_text(75,530,text = self.lang['Test_Area'], fill="darkblue",font="Times 20 italic bold")
		#------------------------background-----------------------------------------------
		#self.logo = tk.PhotoImage(file = "COC/res/COC_logo.png")
		self.logo = PIL.Image.open(self.config['coc_logo'])
		#image = image.resize((20, 20))
		self.logo = ImageTk.PhotoImage(self.logo)
		self.right_part.create_image(230,720,image=self.logo,anchor = NW)
		
		#------------------------test button saved in text_button-------------------------
		self.test_button = list()

		for i in range(len(self.lang['test_name'])):
			btn = Button(self.right_part, text = self.lang['test_name'][i],
						anchor = "center" , highlightcolor = "red")
			btn.configure(width = 14, activebackground = "red", relief = FLAT)
			self.right_part.create_window(30, 560 + i*40, anchor= NW , window=btn)
			self.test_button.append(btn)
		

	def set_function(self):
		self.func = list()
		for i in range(len(self.lang['func_name'])):
			self.func.append(BooleanVar())
			donate = Checkbutton(self.right_part, text = self.lang['func_name'][i],
				variable = self.func[i],bg="white", offvalue = 0, height = 1, width = 10)
			donate.place(x = 20, y = 330 + i*30)

	def set_information(self):
		#------------------------background-----------------------------------------------
		# self.img2 = tk.PhotoImage(file= "COC/res/elixir.png")
		# canva.create_image(20,20,image=self.img2,anchor =NW)
		#------------------------Information Board-------------------------
		self.right_part.create_text(75,15,text = "游戏状态", fill="darkblue",font="Times 20 italic bold")
		fill_color = [
					  "brown",
					  "red",
					  "black"
					 ]
		self.list_pic = list()
		for i in range(len(self.lang['info_name'])):
			self.right_part.create_text(110,50 + 40*i,text = self.lang['info_name'][i],fill = fill_color[i%len(fill_color)])
			image = PIL.Image.open(self.config['source_image'][i])
			#image = image.resize((20, 20))
			image = ImageTk.PhotoImage(image)
			self.list_pic.append(image)
			self.right_part.create_image(20,30 + 40 * i, image = self.list_pic[i], anchor = NW)
		

	def build_left_part(self):                    
		# Build Left Part log
		text = tk.Text(self.frame, height = 0.2, fg = "white", bg = "black", font="Times 20 italic bold")
		text.insert(INSERT,self.lang['log'])
		text.grid(row = 0,column = 0, sticky=N+S+E+W)

		# Add text widget to display logging info
		st = ScrolledText.ScrolledText(self.frame, state='disabled',
					bg = "black", fg = "white", height = 48)
		st.configure(font='TkFixedFont')
		st.grid(row = 1, column = 0, sticky=N+S+E+W)
		#st.place(x = 0, y = 35)

		# Create textLogger
		text_handler = TextHandler(st)

		# Logging configuration
		logging.basicConfig(filename='test.log',
			level=logging.INFO, 
			format='%(asctime)s - %(levelname)s - %(message)s')        

		# Add the handler to logger
		logger = logging.getLogger()        
		logger.addHandler(text_handler)
		

	def build_basic_window(self):
		#------------------------set up windows and title-------------------------
		self.window.title("My CoC Bots")
		self.window.geometry("800x800") #wxh
		self.window.maxsize(1000, 800)
		self.window.minsize(800, 800)
		#self.window.resizable(width = False, height = False)
		self.window.option_add('*tearOff', 'FALSE')
		
		Grid.rowconfigure(self.window,0, weight=1)
		Grid.columnconfigure(self.window, 0, weight=1)

		self.frame = Frame(self.window)
		self.frame.grid(row=0, column=0, sticky=N+S+E+W)
		Grid.columnconfigure(self.frame, 0, weight=1)
		Grid.columnconfigure(self.frame, 1, weight=1)
		Grid.rowconfigure(self.frame, 0, weight=1)
		Grid.rowconfigure(self.frame, 1, weight=1)
	
	# selecting a language
	def select_language(self):
		langs = {
				"中文":'chn',
				"English":'eng'
			}

		new_window = tk.Tk()
		btn = G.selection(new_window,"Languages",langs)
		
		def Set_lang(lang):
			new_window.destroy()
			self.config['lang'] = lang
			self.save_config()

		for b in btn:
			b['command']=lambda lang=b['text']:Set_lang(langs[lang])

		new_window.mainloop()		

	#loading config of languages
	def loading_languages(self):
		#if it is empty config or language is not set yet, 
		if 'lang' not in self.config.keys() or self.config['lang'] == '':
			self.select_language() #select a language
		
		#if there is a profile of language, loading the config
		try:
			self.lang = load_configure("COC/config/lang/" + self.config['lang'] + ".json")	
		except Exception as e: #exit if error
			#messagebox.showinfo("Error", "Did not find the language profile")
			self.config['lang'] = ''
			self.save_config()
			exit()

	#loading config by json file
	def loading_config(self):
		try: 
			self.config.update(load_configure("COC/config/config.json"))
		except Exception as e:
			raise e
			messagebox.showinfo("Error", "configure error")
			exit()

	#Saving the config into the file config.json
	def save_config(self):
		with open('COC/config/config.json', 'w',encoding='utf-8') as outfile:
				json.dump(self.config, outfile, ensure_ascii=False, indent=4, sort_keys=True)
