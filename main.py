import tkinter as tk
from tkinter import messagebox
import subprocess

LARGE_FONT = ("Verdana", 18)

# App
class Application(tk.Tk):
	changesMade = False # Boolean for saving config file
	count=0 #Number of Config Key, Valued Pairs
	d={} # Dictionary of Config Items, read-in from log
	DetailsPage_labels = []; Edit_fieldEntries = []; # All labels, editable config settings
	errorLog = [] # Errors encountered by GUI
	firstEdit = True # Edited check, to load changed data
	labelsGone = False # Labels Deleted from DetailsPage
	numEdits = 0; # Number of times config settings were changed (store-for-later)
	orderKeys = [] # Order of Dictionary Key Elements
	Read_fieldEntries = [] # All Read-only config settings
	sortedData = {} # Dictionary of Config Items, saved by user
	StatusPage_checks = {} # Checks to make, labels for Status Check page
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		tk.Tk.wm_title(self,"Harness Interface")
		self.container = tk.Frame(self)
		self.container.pack(side="top", fill="both", expand=True)
		self.container.grid_rowconfigure(0,weight=1)
		self.container.grid_columnconfigure(0,weight=1)
		self.frames = {}
		self.gather_StatusPage_checks() # Fill Status Page dictionary
		for F in (StartPage, DetailsPage, EditConfigsPage, StatusCheckPage):
			frame = F(self.container,self) # Create frame
			self.frames[F] = frame # Store frame
			frame.grid(row=0, column=0, sticky="nsew") 
		self.show_frame(StartPage) # Show Home
	def gather_StatusPage_checks(self):
		for I in ["Configuration Settings Loaded","Configuration Settings Set","Harness Script Run"]:
			Application.StatusPage_checks[I] = "PASS"
	def show_frame(self, cont):
		for frame in self.frames.values():
			frame.grid_remove()
		frame = self.frames[cont]
		if cont.__name__ == "DetailsPage" and Application.labelsGone:
			del frame
			frame = DetailsPage(self.container,self)
			self.frames[DetailsPage] = frame
		elif cont.__name__ == "StatusCheckPage":
			del frame
			frame = StatusCheckPage(self.container,self)
			self.frames[StatusCheckPage] = frame
		frame.grid(row=0, column=0, sticky="nsew")

# Global Functions
def close_app():
	print("Closing window...Closed.")
	app.quit()

def initialize_class(self,parent,controller):
	tk.Frame.__init__(self,parent)
	self.controller = controller;self.set_page(controller);

def pad_children(self):
	for child in self.winfo_children():
		child.grid_configure(padx=5, pady=5)

def runscript_callback(controller):
	noerror = False;
	try:
		subprocess.check_output('Scripts/Bash/runFile.sh',stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
		noerror = True
	except subprocess.CalledProcessError as e:
		noerror = False
		Application.errorLog.append(e.output)
		Application.StatusPage_checks["Harness Script Run"] = "FAIL"
	if (noerror):
		subprocess.call('Scripts/Bash/runFile.sh', shell=True) # Script accomplishes both Harness build &run 
		Application.StatusPage_checks["Harness Script Run"] = "PASS"
	controller.show_frame(StatusCheckPage)

def window_asktocancel(pageName,controller):
	if messagebox.askokcancel("Quit", "Harness is running. Are you sure you want to quit?"):
		if pageName == "Home":
			controller.show_frame(StartPage)
		elif pageName == "Quit":
			close_app()

def window_popup(title,message):
   tk.messagebox.showinfo(title, message)

def window_callwait(message,self):
    win = window_loadwait(message,self)
    self.after(2000, win.destroy)

def window_loadwait(message,self):
	win = tk.Toplevel(self)
	win.transient()
	win.title("")
	label = tk.Label(win, bg = "green", fg = "white", font = "Helvetica 12", text=message)
	label.grid(row=0, column=0,columnspan=3)
	label.grid_configure(padx=10, pady=10)
	return win

# Config Data Functions
def load_configdata():
	inputdata = {}
	if (Application.firstEdit or not Application.changesMade):
		with open('Logs/harness_log.txt') as f:
			data = f.readlines()
			for item in data:
				splice = item.split(":")
				no_newline = splice[1].split("\n")
				no_space = no_newline[0].split(" ")
				Application.d[splice[0]] = no_space[1]
				Application.count = Application.count+1
				inputdata = Application.d
				Application.orderKeys.append(splice[0])
		write_configdata("Backup")
	else: # If changes have been made, load output file
		with open('Logs/out.txt') as f:
			data = f.readlines()
			for item in data:
				splice = item.split(":")
				no_newline = splice[1].split("\n")
				no_space = no_newline[0].split(" ")
				inputdata[splice[0]] = no_space[1]
	return inputdata

def remove_configitems():
	if (not Application.labelsGone):
		for label in Application.DetailsPage_labels:
			label.grid_remove()
			label.destroy()
		for entry in Application.Read_fieldEntries:
			entry.grid_remove()
			entry.destroy()
		Application.labelsGone = True

def save_configdata(self,controller): # Gather Entry Data, if changed then Output new values
	num=0 # Incrementer
	for key in Application.orderKeys:
		Application.sortedData[key] = Application.Edit_fieldEntries[num].get() # Each key changed, gets its new value
		num = num+1
		if Application.d[key] != Application.sortedData[key]:
			Application.numEdits = Application.numEdits + 1
			Application.changesMade = True
	if (Application.changesMade):
		write_configdata("Save")
		remove_configitems()
		window_callwait("Changes saved",self)
	controller.show_frame(DetailsPage) # Returns to read-only config settings page

def write_configdata(method):
	num = 1 # printing incrementally
	if method == "Backup":
		config = open('Logs/harness_log_backup.txt', 'w')
		check_dict = Application.d
	else:
		config = open('Logs/out.txt', 'w')
		check_dict = Application.sortedData

	for key in Application.orderKeys:
		if num != Application.count:
			config.write(key + ": " + check_dict[key] + "\n") 
		else:
			config.write(key + ": " + check_dict[key]) 
		num = num+1
	config.close()

# Individual Pages
class StartPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self,controller):
		label = tk.Label(self, font = LARGE_FONT, text = "Harness Interface\n").grid(row=0, column=1,columnspan=3)
		runbutton = tk.Button(self, bd = "2", fg = "white", bg = "green", font = "Helvetica 12", text = "Run Harness",command=lambda: runscript_callback(controller)).grid(row=5,column=0,rowspan=1)
		newpagebutton = tk.Button(self, bd = "2", fg = "white", bg = "gray", font = "Helvetica 12", text="View Configs",command=lambda: controller.show_frame(DetailsPage)).grid(row=4,column=0,rowspan=1)
		exitButton = tk.Button(self, bd = "2", fg = "white", bg = "red", font = "Helvetica 12", text ="Close", command = close_app).grid(row=5,column=4,rowspan=1)
		pad_children(self) # Assign padding to child widgets

class DetailsPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self,controller):
		label = tk.Label(self, font = LARGE_FONT, text = "Configuration Settings\n").grid(row=0, column=1,columnspan=3)
		inputdata = load_configdata()
		gobackbutton = tk.Button(self, bd = "2", fg = "white", bg = "blue", font = "Helvetica 12", text="Home",command=lambda: controller.show_frame(StartPage)).grid(row=6,column=7,rowspan=1)
		editbutton = tk.Button(self, bd = "2", fg = "white", bg = "gray", font = "Helvetica 12", text="Edit",command=lambda: controller.show_frame(EditConfigsPage)).grid(row=6,column=6,rowspan=1)
		self.display_configs(inputdata)
	def display_configs(self,inputdata): # Display Configuration Settings (Harness Log), 2 per row
		i=1;j=2; # Column and row incrementers
		for key in Application.orderKeys:
			if i>4:
				i = 1 # column limit exceeded, begin new line
				j = j+1 # new row
			labelName = tk.Label(self,font = "Helvetica 12",text=key + ":")
			Application.DetailsPage_labels.append(labelName) # Store Label widgets in a list, see remove_configitems() function
			labelName.grid(column=i, row=j)
			fieldName = tk.Entry(self)
			fieldName.insert(5,inputdata[key])
			fieldName.grid(column=i+2, row=j) # Placed next to Config setting label
			fieldName.configure(state="readonly") # Readonly for viewing purposes
			Application.Read_fieldEntries.append(fieldName) # Store Label widgets in a list
			i = i+3
		pad_children(self) # Assign padding to child widgets

class EditConfigsPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self,controller):
		label = tk.Label(self, font = LARGE_FONT, text = "Configuration Settings\n").grid(row=0, column=1,columnspan=3)
		savebutton = tk.Button(self, bd = "2", fg = "white", bg = "green", font = "Helvetica 12", text="Save",command=lambda: save_configdata(self,controller)).grid(row=6,column=6,rowspan=1)
		cancelbutton = tk.Button(self, bd = "2", fg = "white", bg = "red", font = "Helvetica 12", text="Cancel",command=lambda: controller.show_frame(DetailsPage)).grid(row=6,column=7,rowspan=1)
		self.display_configs()
	def display_configs(self):
		i=1;j=2; # Column and row incrementers
		for key in Application.orderKeys:
			if i>4:
				i = 1 # column limit exceeded, begin new line
				j = j+1 # new row
			labelName = tk.Label(self,font = "Helvetica 12",text=key + ":").grid(column=i, row=j)
			fieldName = tk.Entry(self)
			fieldName.insert(5,Application.d[key])
			fieldName.grid(column=i+2, row=j)
			i = i+3 # Increment (chosen spacing)
			Application.Edit_fieldEntries.append(fieldName) # Store Entry widgets in a list
		Application.firstEdit = False # Config settings have been edited
		pad_children(self) # Assign padding to child widgets

class StatusCheckPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self, controller):
		label = tk.Label(self, font = LARGE_FONT, text = "Status Check\n").grid(row=0, column=1,columnspan=3)
		gobackbutton = tk.Button(self, bd = "2", fg = "white", bg = "blue", font = "Helvetica 12", text="Home",command=lambda: window_asktocancel("Home",controller)).grid(row=5,column=4,rowspan=1)
		exitButton = tk.Button(self, bd = "2", fg = "white", bg = "red", font = "Helvetica 12", text ="Close", command=lambda: window_asktocancel("Quit",controller)).grid(row=5,column=5,rowspan=1)
		self.load_progress(controller)
	def load_progress(self, controller):
		i=1;j=2; # Column and row incrementers
		for key in sorted(Application.StatusPage_checks):
			labelName = tk.Label(self,font = "Helvetica 12",text= key + "  ").grid(column=i, row=j)
			labelSecond = tk.Label(self, font = "Helvetica 10",text=Application.StatusPage_checks[key], fg = "white")
			if Application.StatusPage_checks[key] == "PASS":
				labelSecond.configure(bg = "Green")
			else:
				labelSecond.configure(bg = "Red")
				logbutton = tk.Button(self, bd = "2", fg = "white", bg = "gray", font = "Helvetica 9", text ="See Log", command = lambda: window_popup("Error Log",Application.errorLog[0])).grid(row=4,column=4,rowspan=1)
			labelSecond.grid(column=i+2, row=j)
			j = j+1
		pad_children(self) # Assign padding to child widgets

## Run GUI		
app = Application()
app.mainloop()