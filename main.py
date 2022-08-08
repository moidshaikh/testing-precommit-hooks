import ui
import time
import json
import speech
import console
from objc_util import *

'''
1.7
#################################################
# Written by Stephen Childs 01/11/2018          #
# Copyright SRHCI Ltd                           #
# IP and Format rights retained by Steve Childs #
#################################################
#. *********************
#.  SRHC Entertainment *
#.  CQL QUIZ TIMER     *
#.  iPhone Version 1.1 *
#. *********************

# This app was commisioned by the Calderdale Quiz League, UK.
they required timers on iPhones for league team games that restricted
thelength of time a question took to answer. Two minutes for the team
 whose question it was and then if they got the answer wrong; the other
 team was allowed 30 seconds to give an answer. this has speeded up the
  quiz and provided extra tension in having to beat the clock as well

# So in order to make it suitable for use by other Quiz leagues around
the world the iPhone version has been made cutomisable to allow any time
 to be set.

it also will Disable the idle timer (which puts the device to sleep after
 a certain period of inactivity).

 My thanks also to to JonB of the pythonista community for providing a neat soltion for a ticklish problem we encountered.

'''

# initialize timers with default values
state = []
transfer=[]
# load fallback values in case file error
stdtime = [120, 30, 10, 5]
timer1 = [0, 0,  0, 0]
timer2 = [0, 0, 0, 0]
seconds = [0, 0, 0]
start = time.clock()
seconds[0] = (int(start))
textchange_called = [0,0,""]
swchange_called = [0,""]
button=[0,0,0,""]
setaw=[1,1]


class textlook (object):
    def textfield_should_begin_editing(self, textfield):
        console.hud_alert('shouldbegin called {}'.format(textfield.name))
        return True
    def textfield_did_begin_editing(self, textfield):
        console.hud_alert('didbegin called {}'.format(textfield.name))
    def textfield_did_end_editing(self, textfield):
        console.hud_alert('didend called {}'.format(textfield.name))
    def textfield_should_return(self, textfield):
        textfield.end_editing()
        return True
    def textfield_should_change(self, textfield, range, replacement):
        console.hud_alert('shouldchange called {}'.format(textfield.name))
        return True
    def textfield_did_change(self, textfield):
        console.hud_alert('didchange called {}'.format(textfield.name))


    # new countdown value written from display input
@on_main_thread
def textchange(r1):
	name=r1.name
	textchange_called[1] = 1
	textchange_called[2] = name
   	if name == 'textfield1':
   			timer1[1] = int(r1.text)
			timer1[2] = timer1[1]
	if name == 'textfield3':
        	timer1[3] = int(r1.text)
	if name == 'textfield2':
       		timer2[1] = int(r1.text)
       		timer2[2] = timer2[1]
	if name == 'textfield4':
      		timer2[3] = int(r1.text)



def switch(sender):
	sx = sender.value
	if sx is False:
		swchange_called[0] = 1
	if sx is True:
		swchange_called[0] = 2
	return

def setswitch(sender):
	setname = sender.name
	val = sender.value
	if setname == 'switch2':
		if val is True:
			setaw[0] = 1
		if val is False:
			setaw[0] = 0
	if setname == 'switch3':
		if val is True:
			setaw[1] = 1
		if val is False:
			setaw[1] = 0


def action(sender):
	title = sender.title
	button[3]=title
	# have they pressed confer button
	if title == 'Confer':
		if timer1[0] == 0:
			timer1[0] = 1
			#timer1[2] += 1
			button[0]=1
	# have they pressed pass button
	if title == 'Pass':
		if timer2[0] == 0:
			timer2[0] = 1
			#timer2[2] += 1
			timer1[0] = 2
			button[1]=1
	# have they pressed reset button
	if title == 'Reset':
		timer1[0] = 0
		timer1[2] = timer1[1]
		timer2[0] = 0
		timer2[2] = timer2[1]
		button[2]=1





# timerx [ on, setval, curval, warn]
def load_timers(timer1, timer2, stdtime):
	timer1[1] = stdtime[0]
	timer1[2] = stdtime[0]
	timer2[1] = stdtime[1]
	timer2[2] = stdtime[1]
	timer1[3] = stdtime[2]
	timer2[3] = stdtime[3]

def store_timers(timer1, timer2, stdtime):
	stdtime[0] = timer1[1]
	stdtime[1] = timer2[1]
	stdtime[2] = timer1[3]
	stdtime[3] = timer2[3]
	state = stdtime
	save_state('setup.json', state)


# update_display()
#@on_main_thread
def how_long(seconds):
	seconds[2] = seconds[1]
	delta = time.clock()
	seconds[1] = int(delta)

def buttonaction(button,cb,pb,rb,label4,label5):
	# have they pressed confer button
	if button[0] == 1:
		label4.text = str(timer1[2])
		cb.enabled = False
		label4.background_color = '#00ff00'
		button[0] = 0
	# have they pressed pass button
	if button[1] == 1:
		label5.text = str(timer2[2])
		pb.enabled = False
		label5.background_color = '#00ff00'
		# halt the confer timer and not allow restart
		cb.enabled = False
		button[1] = 0
	# have they pressed reset button
	if button[2] == 1:
		timer1[0] = 0
		timer1[2] = timer1[1]
		timer2[0] = 0
		timer2[2] = timer2[1]
		label4.text = str(timer1[2])
		label5.text = str(timer2[2])
		cb.enabled = True
		pb.enabled = True
		label4.background_color = '#00ffff'
		label4.text_color = '#000000'
		label5.background_color = '#00ffff'
		label5.text_color = '#000000'
		button[2] = 0


def switchoff(tf1, tf2, tf3, tf4, sx1, sx2, sx3, cb, pb):
	tf1.enabled = False
	tf2.enabled = False
	tf3.enabled = False
	tf4.enabled = False
	sx2.enabled = False
	sx3.enabled = False
	textchange_called[0] = 0
	swchange_called[0] = 0
	store_timers(timer1, timer2, stdtime)
	cb.enabled = True
	pb.enabled = True


def switchon(tf1,tf2,tf3,tf4,sx1,sx2,sx3,cb,pb):
	tf1.enabled = True
	tf2.enabled = True
	tf3.enabled = True
	tf4.enabled = True
	sx2.enabled = True
	sx3.enabled = True
	textchange_called[0] = 1
	swchange_called[0] = 0
	cb.enabled = False
	pb.enabled = False


def label4_update(label4):
		label4_change = label4
		label4_change.text = str(timer1[2])
		if timer1[2] == timer1[3]:
			label4_change.text_color = '#ffffff'
			label4_change.background_color = '#ff0000'


def label5_update(label5):
		label5_change = label5
		label5_change.text = str(timer2[2])
		if timer2[2] == timer2[3]:
			label5_change.text_color = '#ffffff'
			label5_change.background_color = '#ff0000'


def run_timer1():
	if timer1[0] != 2:
		timer1[2] -= 1
		# print (timer1[2])
		if timer1[2] == timer1[3] and setaw[0]==1:
			speech.say(str(timer1[3]) + 'Seconds remaining', 'en_GB')
	if timer1[2] <= 0:
		timer1[0] = 2
		if setaw[1]==1:
			speech.say('Answer Please', 'en_GB')


def run_timer2():
	if timer2[0] != 2:
		timer2[2] -= 1
		# print (timer2[2])
		if timer2[2] == timer2[3]and setaw[0]==1:
			speech.say(str(timer2[3]) + 'Seconds remaining', 'en_US')
	if timer2[2] <= 0:
		timer2[0] = 2
		if setaw[1]==1:
			speech.say('Answer Please', 'en_US')


def timer_update():
	if timer1[0] == 1:
		run_timer1()
	if timer2[0] == 1:
		run_timer2()


def setvaluesonscreen(tf1,tf2,tf3,tf4,label4,label5):
	#print "here"
	#print textchange_called
	if textchange_called[2]==('textfield1'):
		#print 'checking t1 set time'
		if timer1[1] <= 1 or timer1[1] >= 1801:
			timer1[1] = stdtime[0]
		tf1.text = str(timer1[1])
		#print "looping1"
		label4.text = str(timer1[1])
		#print 'looping2'
	if textchange_called[2]==('textfield3'):
		#print 'checking t1 warning'
		if timer1[3] <= 0 or timer1[3] >= timer1[1]:
			timer1[3] = int(round(timer1[1] / 5))
		tf3.text = str(timer1[3])
		#print 'looping3'
	if textchange_called[2]==('textfield2'):
		#print 'checking t2 set time'
		if timer2[1] <= 0 or timer2[1] >= 1801:
			timer2[1] = stdtime[1]
		tf2.text = str(timer2[1])
		#print "looping4"
		label5.text = str(timer2[1])
		#print 'looping5'
	if textchange_called[2]==('textfield4'):
		if timer2[3] <= 0 or timer2[3] >= timer2[1]:
			timer2[3] = int(round(timer2[1] / 5))
		tf4.text = str(timer2[3])
	#print 'end of update'
	return

# file handlers
def save_state(filename,state):
    with open(filename, 'w') as f:
        json.dump(state, f)

def load_state(filename):
    with open(filename) as f:
        return json.load(f)

try:
    state=load_state('setup.json')
    aa= "stdtime"
    stdtime = state

except IOError:
    print "console.hud_alert('setup file not called')"
    state = stdtime
    save_state('setup.json')


def main():
	state=load_state('setup.json')
	stdtime = state
	# print stdtime, "loaded values"
	#time.sleep(1)
	load_timers(timer1,timer2,stdtime)
	# print timer1,timer2
	v = ui.load_view('cql')
	v.background_color = '#00ffff'
	label4 = v['label4']
	label5 = v['label5']
	cb =v['button1']
	pb = v['button2']
	rb = v['button3']
	sx1 = v['switch1']
	sx2 = v['switch2']
	sx3 = v['switch3']
	tf1 = v['textfield1']
	tf2 = v['textfield2']
	tf3 = v['textfield3']
	tf4 = v['textfield4']
	tf1.enabled = False
	tf2.enabled = False
	tf3.enabled = False
	tf4.enabled = False
	sx2.enabled = False
	sx3.enabled = False
	delegate=textlook()
	x=0
	for tf in [tf1, tf2, tf3, tf4]:
	    tf.action = textchange
	    tf.keyboard_type= ui.KEYBOARD_NUMBER_PAD
	    tf.text = str(stdtime[x])
	    x = x+ 1
	label4_update(label4)
	label5_update(label5)
	v.present('sheet')
	# timing loops engaged and ready to run
	#console.set_idle_timer_disabled(True)
	while True:
		how_long(seconds)
		if button[0] == 1 or button[1] == 1 or button[2] == 1:
			buttonaction(button,cb,pb,rb,label4,label5)
		if seconds[1] != seconds[2] and (timer1[0] == 1 or timer2[0] == 1):
			timer_update()
			label4_update(label4)
			label5_update(label5)
		if textchange_called[0] == 1 and textchange_called[1] == 1:
			setvaluesonscreen(tf1,tf2,tf3,tf4,label4,label5)
			textchange_called[1] = 0
		if swchange_called[0] == 1:
			switchoff(tf1,tf2,tf3,tf4,sx1,sx2,sx3,cb,pb)
		if swchange_called[0] == 2:
			switchon(tf1,tf2,tf3,tf4,sx1,sx2,sx3,cb,pb)
		# check if still on screen
		onscreen = v.on_screen
		if onscreen is False:
			#console.set_idle_timer_disabled(False)
			return False


if __name__ == '__main__':
 	main()
