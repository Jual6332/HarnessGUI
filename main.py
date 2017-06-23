import tkinter as tk
import math
import subprocess
from tkinter import messagebox
from tkinter.ttk import Separator, Style

SMALL_FONT = "Helvetica 10"; NORMAL_FONT = "Helvetica 12"; LARGE_FONT = "Verdana 18";

# App
class Application(tk.Tk):
	changesMade = False # Boolean for saving config file
	count=0 # Number of Config Key, Valued Pairs
	configData={} # Dictionary of Original Config Items
	DetailsPage_entries = []; DetailsPage_labels = []; # All read-only widgets
	EditPage_entries = []; EditPage_labels = []; # All editable widgets
	errorLog = [] # Errors encountered by GUI
	firstEdit = True # Edited check, to load changed data
	DetailsPage_labelsGone = False; EditPage_labelsGone = False; 
	key_order = [] # Order of Dictionary Key Elements
	script_name = "runzFile.sh"; # Script to run Harness java project
	sortedData = {} # Dictionary of Config Items, saved by user
	StatusPage_checks = {} # Checks to make, labels for Status Check page
	units = ["y/n","hrs","hrs","mins","hrs","hrs","hrs","None"] # Units for Configs
	units_set = {}

	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs); tk.Tk.wm_title(self,"Harness Interface");
		self.container = tk.Frame(self); self.container.pack(side="top", fill="both", expand=True);
		self.container.grid_rowconfigure(0,weight=1); self.container.grid_columnconfigure(0,weight=1);
		self.frames = {}; self.gather_StatusPage_checks(); # Fill Status Page dictionary
		for F in (StartPage, DetailsPage, EditConfigsPage, StatusCheckPage):
			frame = F(self.container,self); self.frames[F] = frame; frame.grid(row=0, column=0, sticky="nsew") # Create, store, grid
		self.show_frame(StartPage) # Show Home

	def gather_StatusPage_checks(self):
		for I in ["Configuration Settings Loaded","Configuration Settings Set","Harness Script Run"]: Application.StatusPage_checks[I] = "PASS";

	def show_frame(self, cont):
		for frame in self.frames.values(): frame.grid_remove()
		frame = self.frames[cont]
		if cont.__name__ == "DetailsPage" and Application.DetailsPage_labelsGone:
			del frame; frame = DetailsPage(self.container,self);
			self.frames[DetailsPage] = frame
		elif cont.__name__ == "StatusCheckPage": 
			del frame; frame = StatusCheckPage(self.container,self);
			self.frames[StatusCheckPage] = frame
		frame.grid(row=0, column=0, sticky="nsew")

# Global Functions
def close_app(): print("Closing window...Closed."); app.quit();

def initialize_class(self,parent,controller): 
	tk.Frame.__init__(self,parent); self.controller = controller; self.set_page(controller);

def pad_children(self): 
	for child in self.winfo_children(): child.grid_configure(padx=5, pady=5);

def runscript_callback(controller):
	noerror = False; 
	try:
		subprocess.check_output('Scripts/Bash/'+Application.script_name,stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
		noerror = True
	except subprocess.CalledProcessError as e:
		noerror = False
		if "not found" in e.output and "Scripts/Bash/" in e.output: e.output="Script file '" + Application.script_name+ "' not found";
		Application.errorLog.append(e.output); Application.StatusPage_checks["Harness Script Run"] = "FAIL";
	if (noerror):
		subprocess.call('Scripts/Bash/'+Application.script_name, shell=True) # Script accomplishes both Harness build &run 
		Application.StatusPage_checks["Harness Script Run"] = "PASS"
	controller.show_frame(StatusCheckPage)

def window_asktocancel(pageName,controller,errorQuery):
	if not errorQuery:
		if messagebox.askokcancel("Quit", "Harness is running. Are you sure you want to quit?"):
			if pageName == "Home": controller.show_frame(StartPage);
			elif pageName == "Quit": close_app();
	else:
		if pageName == "Home": controller.show_frame(StartPage);
		elif pageName == "Quit": close_app();

def window_callwait(message,self):
    win = window_loadwait(message,self); self.after(2000, win.destroy);

def window_loadwait(message,self):
	win = tk.Toplevel(self); win.transient(); win.title("");
	label = tk.Label(win, font = NORMAL_FONT, text=message); label.grid(row=0, column=0,columnspan=3); label.grid_configure(padx=10, pady=10);
	return win

def window_popup(title,message):
   tk.messagebox.showinfo(title, message)

# Config Data Functions
def load_configdata():
	inputdata = {};
	if (Application.firstEdit or not Application.changesMade): # Better way: Simplify to one with statement!!!!
		with open('Logs/harness_log.txt') as f:
			Application.key_order = []; data = f.readlines();
			for item in data:
				splice = item.split(":"); no_newline = splice[1].split("\n"); no_space = no_newline[0].split(" ");
				Application.configData[splice[0]] = no_space[1]; Application.count = Application.count+1;
				inputdata = Application.configData; Application.key_order.append(splice[0]);
		write_configdata("Backup")
	else: # If changes have been made, load output file
		with open('Logs/out.txt') as f:
			data = f.readlines()
			for item in data:
				splice = item.split(":"); no_newline = splice[1].split("\n");
				no_space = no_newline[0].split(" "); inputdata[splice[0]] = no_space[1];
	return inputdata

def remove_configitems():
	if (not Application.DetailsPage_labelsGone):
		for label in Application.DetailsPage_labels: label.grid_remove(); label.destroy();
		for entry in Application.DetailsPage_entries: entry.grid_remove(); entry.destroy();
		Application.DetailsPage_labelsGone = True

def save_configdata(self,controller): # Gather Entry Data, if changed then Output new values
	num=0; check = True; errorMsg = "Errors:\n------------\n";
	for key in Application.key_order:
		Application.sortedData[key] = Application.EditPage_entries[num].get() # Each key changed, gets its new value
		if key == "forecast" and (not Application.sortedData[key].isalpha()):
			check = False; errorMsg = errorMsg + "- Item 'forecast' must contain only letters\n";
		elif key == "forecast" and (Application.sortedData[key] not in {"no","yes"}):
			check = False; errorMsg = errorMsg + "- Item '"+key+"' must be either yes or no\n";
		elif key != "forecast" and (not Application.sortedData[key].isnumeric()):
			check = False; errorMsg = errorMsg + "- Item '"+key+"' must contain only numbers\n";
		else:
			if Application.configData[key] != Application.sortedData[key]: Application.changesMade = True;
		num = num+1
	if check: # Save changes to CIs
		if (Application.changesMade):
			write_configdata("Save"); remove_configitems(); window_callwait("Saving changes!",self); # Save data, clear DetailsPage, display Saved changed prompt
		controller.show_frame(DetailsPage) # Returns to read-only config settings page
	else: window_popup("Save Failed",errorMsg)

def set_configunits():
	i=0;
	for key in Application.key_order:
		Application.units_set[key] = Application.units[i]; i=i+1;

def write_configdata(method):
	num = 1 # printing incrementally
	if method == "Backup":
		config = open('Logs/harness_log_backup.txt', 'w'); check_dict = Application.configData;
	else:
		config = open('Logs/out.txt', 'w'); check_dict = Application.sortedData;
	for key in Application.key_order:
		if num != Application.count: # Simplify newline!
			config.write(key + ": " + check_dict[key] + "\n") # Print w/ newline
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
		runbutton = tk.Button(self, bd = "2", fg = "white", bg = "green", font = NORMAL_FONT, text = "Run Harness",command=lambda: runscript_callback(controller)).grid(row=5,column=0,rowspan=1)
		newpagebutton = tk.Button(self, bd = "2", fg = "white", bg = "gray", font = NORMAL_FONT, text="View Configs",command=lambda: controller.show_frame(DetailsPage)).grid(row=4,column=0,rowspan=1)
		exitButton = tk.Button(self, bd = "2", fg = "white", bg = "red", font = NORMAL_FONT, text ="Close", command = close_app).grid(row=5,column=4,rowspan=1)
		pad_children(self) # Assign padding to child widgets

def display_ClassConfigs(name,self):
	i=1;j=2; # Column and row incrementers
	sty = Style(self); sty.configure("TSeparator", background="blue");
	if name == "DetailsPage":
		inputdata = load_configdata(); set_configunits(); # Load data, store units
		for key in Application.key_order:
			if i>7:	i = 1; j = j+1; # Column limit exceeded, begin new row
			labelName = tk.Label(self,font = NORMAL_FONT,text=key + ":"); labelName.grid(column=i, row=j);
			fieldName = tk.Entry(self); fieldName.grid(column=i+2, row=j, rowspan=1);
			fieldName.insert(1,inputdata[key]);	fieldName.configure(state="readonly");
			if Application.units_set[key] != "None":
				unitsLabel = tk.Label(self,font = NORMAL_FONT,text="("+Application.units_set[key]+")"); unitsLabel.grid(column=i+4, row=j);
			sep = Separator(self, orient="vertical")
			sep.grid(column=6, row=j-1, rowspan=2, sticky="nsew")
			Application.DetailsPage_entries.append(fieldName); Application.DetailsPage_labels.append(labelName); # Store widgets 
			i = i+6 # Column for Second label/entry pair
	else:
		for key in Application.key_order:
			if i>7: i = 1; j = j+1; # Column limit exceeded, begin new row
			labelName = tk.Label(self,font = NORMAL_FONT,text=key + ":"); labelName.grid(column=i, row=j);
			fieldName = tk.Entry(self); fieldName.grid(column=i+2, row=j);
			fieldName.insert(5,Application.configData[key]); # Create entry, add data
			if Application.units_set[key] != "None":
				unitsLabel = tk.Label(self,font = NORMAL_FONT,text="("+Application.units_set[key]+")"); unitsLabel.grid(column=i+4, row=j);
			sep = Separator(self, orient="vertical")
			sep.grid(column=6, row=j-1, rowspan=2, sticky="nsew")
			Application.EditPage_entries.append(fieldName); Application.EditPage_labels.append(labelName); # Store widgets
			i = i+6 # Column for Second label/entry pair
		Application.firstEdit = False # Config settings have been edited
	pad_children(self) # Assign padding to child widgets

class DetailsPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self,controller):
		inputdata = load_configdata()
		label = tk.Label(self, font = LARGE_FONT, text = "Configuration Settings\n").grid(row=0, column=1,columnspan=3)
		gobackbutton = tk.Button(self, bd = "2", fg = "white", bg = "blue", font = NORMAL_FONT, text="Home",command=lambda: controller.show_frame(StartPage)).grid(row=int(math.ceil(len(Application.key_order)/2))+2,column=13,rowspan=1)
		editbutton = tk.Button(self, bd = "2", fg = "white", bg = "gray", font = NORMAL_FONT, text="Edit",command=lambda: controller.show_frame(EditConfigsPage)).grid(row=int(math.ceil(len(Application.key_order)/2))+2,column=12,rowspan=1)
		display_ClassConfigs("DetailsPage",self)

class EditConfigsPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self,controller):
		label = tk.Label(self, font = LARGE_FONT, text = "Configuration Settings\n").grid(row=0, column=1,columnspan=3)
		savebutton = tk.Button(self, bd = "2", fg = "white", bg = "green", font = NORMAL_FONT, text="Save",command=lambda: save_configdata(self,controller)).grid(row=int(math.ceil(len(Application.key_order)/2))+2,column=12,rowspan=1)
		cancelbutton = tk.Button(self, bd = "2", fg = "white", bg = "red", font = NORMAL_FONT, text="Cancel",command=lambda: controller.show_frame(DetailsPage)).grid(row=int(math.ceil(len(Application.key_order)/2))+2,column=13,rowspan=1)
		display_ClassConfigs("EditConfigsPage",self)

class StatusCheckPage(tk.Frame):
	def __init__(self,parent,controller):
		initialize_class(self,parent,controller)
	def set_page(self, controller):
		label = tk.Label(self, font = LARGE_FONT, text = "Status Check\n").grid(row=0, column=1,columnspan=3)
		error = False; 
		if len(Application.errorLog)>0: error=True;
		gobackbutton = tk.Button(self, bd = "2", fg = "white", bg = "blue", font = NORMAL_FONT, text="Home",command=lambda: window_asktocancel("Home",controller,error)).grid(row=6,column=4,rowspan=1)
		exitButton = tk.Button(self, bd = "2", fg = "white", bg = "red", font = NORMAL_FONT, text ="Close", command=lambda: window_asktocancel("Quit",controller,error)).grid(row=6,column=5,rowspan=1)
		self.load_progress(controller)
	def load_progress(self, controller):
		i=1;j=2; # Column and row incrementers
		for key in sorted(Application.StatusPage_checks):
			labelName = tk.Label(self,font = NORMAL_FONT,text= key + "  ").grid(column=i, row=j)
			labelSecond = tk.Label(self, font = SMALL_FONT,text=Application.StatusPage_checks[key], fg = "white")
			if Application.StatusPage_checks[key] == "PASS": labelSecond.configure(bg = "Green");
			else: 
				labelSecond.configure(bg = "Red"); logbutton = tk.Button(self, bd = "2", fg = "white", bg = "gray", font = "Helvetica 9", text ="See Log", command = lambda: window_popup("Error Log",Application.errorLog[0])).grid(row=4,column=4,rowspan=1)
			labelSecond.grid(column=i+2, row=j)
			j = j+1 # New row
		pad_children(self) # Assign padding to child widgets

## Run GUI		
app = Application()
app.mainloop()