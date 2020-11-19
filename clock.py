from tkinter import *
from tkinter.ttk import *
import datetime
import platform
try:
	import winsound 
except:
	import os 

window = Tk()
window.title("Slow Timer")
window.geometry('500x250')
window.configure(bg='black')

mygreen = "#d2ffd2"
myred = "#dd0202"

style = Style()

style.theme_create( "yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": mygreen },
            "map":       {"background": [("selected", myred)],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("yummy")

tabs_control = Notebook(window)
timer_tab = Frame(tabs_control)
tabs_control.add(timer_tab, text='Timer')
tabs_control.pack(expand = 1, fill ="both")

options = [1, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]
variable = StringVar(window)
variable.set(options[0]) 

w = OptionMenu(window, variable, *options)
w.pack()

def timer_counter(label, speed):
	def count():
		global timer_running
		if timer_running:
			global timer_counter_num
			if timer_counter_num==66600:
				for i in range(10):
					display="Time Is Up"
					if platform.system() == 'Windows':
						winsound.Beep(5000,1000)
					elif platform.system() == 'Darwin':
						os.system('say Time is Up')
					elif platform.system() == 'Linux':
						os.system('beep -f 5000')
				timer_running=False
				timer('reset')
			else:
				tt = datetime.datetime.fromtimestamp(timer_counter_num) 
				string = tt.strftime("%H:%M:%S") 
				display=string
				timer_counter_num -= 1*speed
			label.config(text=display)
			label.after(1000, count)
	count()

def timer(work, *args):
	speed = float(variable.get())
	if work == 'start':
		global timer_running, timer_counter_num
		timer_running=True
		if timer_counter_num == 66600:
			timer_time_str = timer_get_entry.get()
			hours,minutes,seconds=timer_time_str.split(':')
			minutes = int(minutes)  + (int(hours) * 60)
			seconds = int(seconds) + (minutes * 60)
			timer_counter_num = timer_counter_num + seconds  
		timer_counter(timer_label, speed)
		timer_start.config(state='disabled')
		timer_stop.config(state='enabled')
		timer_reset.config(state='enabled')
		timer_get_entry.delete(0,END)
	elif work == 'stop':
		timer_running=False
		timer_start.config(state='enabled')
		timer_stop.config(state='disabled')
		timer_reset.config(state='enabled')
	elif work == 'reset':
		timer_running=False
		timer_counter_num=66600
		timer_start.config(state='enabled')
		timer_stop.config(state='disabled')
		timer_reset.config(state='disabled')
		timer_get_entry.config(state='enabled')
		timer_label.config(text = 'Timer')

variable.trace('w', timer)
timer_counter_num = 66600
timer_running = False
timer_get_entry = Entry(timer_tab, font='arial 15 bold')
timer_get_entry.pack(anchor='center')
timer_instructions_label = Label(timer_tab, font = 'calibri 10 bold', text = "Hours:Minutes:Seconds")
timer_instructions_label.pack(anchor='s')
timer_label = Label(timer_tab, font='calibri 40 bold', text='Timer')
timer_label.pack(anchor='center')
timer_start = Button(timer_tab, text='Start', command=lambda:timer('start'))
timer_start.pack(anchor='center')
timer_stop = Button(timer_tab, text='Stop', state='disabled',command=lambda:timer('stop'))
timer_stop.pack(anchor='center')
timer_reset = Button(timer_tab, text='Reset', state='disabled', command=lambda:timer('reset'))
timer_reset.pack(anchor='center')
window.mainloop()