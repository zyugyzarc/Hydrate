import os
import webview
from time import sleep
from document import Document
import simpleaudio as sa

#deps: pywebview, simpleaudio

document = Document(None)

dark_theme = False

sound = sa.WaveObject.from_wave_file('ringtone.wav')

MINUTES, SECONDS = 29, 60

def alert():
	alertwin = webview.create_window('', url='alert.html', frameless=True, on_top=True, width=300, height=400)
	try: webview.start(load, alertwin)
	except: pass
	sleep(10)
	alertwin.destroy()

def kill():
	document.flags['run'] = False

def change_theme():
	global dark_theme
	dark_theme = not dark_theme

	steps = 1
	if dark_theme:
		document.eval_js(f" document.querySelector(':root').style.setProperty('--fgcolor','hsl(0,0%,95%)') ")
		document.eval_js(f" document.querySelector(':root').style.setProperty('--bgcolor','hsl(0,0%,3%)') ")
	else:
		document.eval_js(f" document.querySelector(':root').style.setProperty('--bgcolor','hsl(0,0%,95%)') ")
		document.eval_js(f" document.querySelector(':root').style.setProperty('--fgcolor','hsl(0,0%,3%)') ")


def reset_timer():
	document.flags['time'] = 0

def main(window):
	document.window = window
	document.flags['time'] = 0
	document.flags['run'] = True
	window.expose(*funcs)
	window.set_title('H20')
	sleep(1)
	while document.flags['run']:
		document.flags['time'] +=1
		document.flags['time'] = document.flags['time'] % (60*MINUTES + SECONDS)
		t = document.flags['time']
		document.get('time').innerHTML(f"{MINUTES-(t//60)}:{SECONDS-(t%60)}")
		if document.flags['time'] == 0:
			sound.play()
			alert()
		sleep(1)


def load(window):
	sleep(3)
	window.destroy()

try:
	funcs = [eval(i) for i in dir() if i[0] != '_' and type(eval(i)) == type(main)]

	html = open('struct.html','r').read()
	html = html.replace('py','pywebview.api')
	open('temp.html','w').write(html)
	tempwin = webview.create_window('', url='load.html', frameless=True, width=300, height=400)
	webview.start(load, tempwin)
	window = webview.create_window('H20', url='temp.html', min_size=(400,300))#, #html=html)
	window.closed += kill
	webview.start(main, window, gui='qt')
	os.remove('temp.html')
except:
	import installer
