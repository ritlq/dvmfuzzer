from easygui import *
from Tkinter import *
import sys

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY    = ("Courier")

PROPORTIONAL_FONT_SIZE  = 10
MONOSPACE_FONT_SIZE     =  9
TEXT_ENTRY_FONT_SIZE    = 12

def _fileopenbox():
    msg  = "APK"
    title = "Open files"
    default="*.apk"
    apkpath = fileopenbox(msg,title,default=default)
    return apkpath

def dq(s):
    return '"%s"' % s

def _fuzzpercentage(msg="Please enter your desired fuzz percentage (0.1 - 100)"
	, title="Fuzzing Percentage"
	, default=""
	, lowerbound=0.1
	, upperbound=100
	, image = None
	, root  = None
	, **invalidKeywordArguments
	):

	if "argLowerBound" in invalidKeywordArguments:
		raise AssertionError(
	"\nintegerbox no longer supports the 'argLowerBound' argument.\n"
		+ "Use 'lowerbound' instead.\n\n")
	if "argUpperBound" in invalidKeywordArguments:
		raise AssertionError(
			"\nintegerbox no longer supports the 'argUpperBound' argument.\n"
			+ "Use 'upperbound' instead.\n\n")

	if default != "":
		if type(default) != type(1):
			raise AssertionError(
				"What you have typed is not an acceptable value.", "Error")

	if msg == "":
		msg = ("Enter an integer between " + str(lowerbound)
			+ " and "
			+ str(upperbound)
			)

	while 1:
		reply = enterbox(msg, title, str(default), image=image, root=root)
		if reply == None: return None

		try:
			reply = float(reply)
		except:
			msgbox ("The value that you entered:\n\t%s\nis not an integer." % dq(str(reply))
					, "Error")
			continue

		if reply < lowerbound:
			msgbox ("The value that you entered is less than the minimum value: "
				+ str(lowerbound) + ".", "Error")
			continue

		if reply > upperbound:
			msgbox ("The value that you entered is greater than the maximum value: "
				+ str(upperbound) + ".", "Error")
			continue
		
        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
		reply = reply/100
		return reply

def _looptimes(msg="Please enter your desired number of times to loop."
	, title="Number of Loops"
	, default=""
	, lowerbound=1
	, upperbound=1000
	, image = None
	, root  = None
	, **invalidKeywordArguments
	):

	if "argLowerBound" in invalidKeywordArguments:
		raise AssertionError(
	"\nintegerbox no longer supports the 'argLowerBound' argument.\n"
		+ "Use 'lowerbound' instead.\n\n")
	if "argUpperBound" in invalidKeywordArguments:
		raise AssertionError(
			"\nintegerbox no longer supports the 'argUpperBound' argument.\n"
			+ "Use 'upperbound' instead.\n\n")

	if default != "":
		if type(default) != type(1):
			raise AssertionError(
				"What you have typed is not an acceptable value.", "Error")

	if msg == "":
		msg = ("Enter an integer between " + str(lowerbound)
			+ " and "
			+ str(upperbound)
			)

	while 1:
		reply = enterbox(msg, title, str(default), image=image, root=root)
		if reply == None: return None

		try:
			reply = int(reply)
		except:
			msgbox ("The value that you entered:\n\t%s\nis not an integer." % dq(str(reply))
					, "Error")
			continue

		if reply < lowerbound:
			msgbox ("The value that you entered is less than the minimum value: "
				+ str(lowerbound) + ".", "Error")
			continue

		if reply > upperbound:
			msgbox ("The value that you entered is greater than the maximum value: "
				+ str(upperbound) + ".", "Error")
			continue
		
        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
		return reply
	
	

def _setup():
	while 1:
		choices = [
			"1. Load APK",
			"2. Select Fuzz Percent",
			"3. Select Number of Loops",
			"Begin Fuzzing",
			"Quit"
			]
		
		choice = choicebox(msg = "This is the setup page before the fuzzing begins.", title = "Android DVM Fuzzer - Main Menu", choices = choices)
		
		if not choice: return
		
		reply = choice
		
		if reply == "1. Load APK":
			apkpath = _fileopenbox()
			msgbox("APK Loaded:\n" + str(apkpath), "Result")
		
		elif reply == "2. Select Fuzz Percent":
			fuzzpercent = _fuzzpercentage()
			msgbox("Percentage is:\n" + str(fuzzpercent), "Result")
		
		elif reply == "3. Select Number of Loops":
			looptimes = _looptimes()
			msgbox("Number of loops:\n" + str(looptimes), "Result")
		
		elif reply == "Begin Fuzzing":
			_process()
		
		elif reply == "Quit":
			sys.exit()
		
		else:
			print(reply)
			msgbox("Choice:\n\n" + choice + "\n\nis not recognized", "Program Logic Error")
			return

def _process(msg="aplha", title="beta", text="creta"):
	return textbox(msg, title, text, codebox=1 )

def denyWindowManagerClose():
    """ don't allow WindowManager close
    """
    x = Tk()
    x.withdraw()
    x.bell()
    x.destroy()

#-------------------------------------------------------------------
# textbox
#-------------------------------------------------------------------
def textbox(msg=""
    , title=""
    , text=""
    , codebox=0
    ):

    if msg == "": msg = "Fuzzing in progress"
    if title == "": title = "Android DVM Fuzzer - Fuzzing"

    global boxRoot, __replyButtonText, __widgetTexts, buttonsFrame
    global rootWindowPosition
    choices = ["Stop"]
    __replyButtonText = choices[0]


    boxRoot = Tk()

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )

    screen_width = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width = int((screen_width * 0.8))
    root_height = int((screen_height * 0.5))
    root_xpos = int((screen_width * 0.1))
    root_ypos = int((screen_height * 0.05))

    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    rootWindowPosition = "+0+0"
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand=NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
    boxRoot.geometry(rootWindowPosition)

    mainframe = Frame(master=boxRoot)
    mainframe.pack(side=TOP, fill=BOTH, expand=YES)

    # ----  put frames in the window -----------------------------------
    # we pack the textboxFrame first, so it will expand first
    textboxFrame = Frame(mainframe, borderwidth=3)
    textboxFrame.pack(side=BOTTOM , fill=BOTH, expand=YES)

    message_and_buttonsFrame = Frame(mainframe)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO)

    # -------------------- put widgets in the frames --------------------

    # put a textArea in the top frame
    if codebox:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(textboxFrame,height=25,width=character_width, padx="2m", pady="1m")
        textArea.configure(wrap=NONE)
        textArea.configure(font=(MONOSPACE_FONT_FAMILY, MONOSPACE_FONT_SIZE))

    else:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(
            textboxFrame
            , height=25
            , width=character_width
            , padx="2m"
            , pady="1m"
            )
        textArea.configure(wrap=WORD)
        textArea.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))


    # some simple keybindings for scrolling
    mainframe.bind("<Next>" , textArea.yview_scroll( 1,PAGES))
    mainframe.bind("<Prior>", textArea.yview_scroll(-1,PAGES))

    mainframe.bind("<Right>", textArea.xview_scroll( 1,PAGES))
    mainframe.bind("<Left>" , textArea.xview_scroll(-1,PAGES))

    mainframe.bind("<Down>", textArea.yview_scroll( 1,UNITS))
    mainframe.bind("<Up>"  , textArea.yview_scroll(-1,UNITS))


    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(textboxFrame, orient=VERTICAL, command=textArea.yview)
    textArea.configure(yscrollcommand = rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(textboxFrame, orient=HORIZONTAL, command=textArea.xview)
    textArea.configure(xscrollcommand = bottomScrollbar.set)

    # pack the textArea and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    # Note that we need a bottom scrollbar only for code.
    # Text will be displayed with wordwrap, so we don't need to have a horizontal
    # scroll for it.
    if codebox:
        bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)

    textArea.pack(side=LEFT, fill=BOTH, expand=YES)


    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

    # put the buttons in the buttonsFrame
    okButton = Button(buttonsFrame, takefocus=YES, text="Stop", height=1, width=6)
    okButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __textboxOK
    for selectionEvent in ["Return","Button-1","Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ----------------- the action begins ----------------------------------------
    try:
        # load the text into the textArea
        if type(text) == type("abc"): pass
        else:
            try:
                text = "".join(text)  # convert a list or a tuple to a string
            except:
                msgbox("Exception when trying to convert "+ str(type(text)) + " to text in textArea")
                sys.exit(16)
        textArea.insert(END,text, "normal")

    except:
        msgbox("Exception when trying to load the textArea.")
        sys.exit(16)

    try:
        okButton.focus_force()
    except:
        msgbox("Exception when trying to put focus on okButton.")
        sys.exit(16)
	
	"""_autoscroll()""" # Unused function for auto scrolling
    boxRoot.mainloop()

    # this line MUST go before the line that destroys boxRoot
    areaText = textArea.get(0.0,END)
    boxRoot.destroy()
    return areaText # return __replyButtonText

#-------------------------------------------------------------------
# __textboxOK
#-------------------------------------------------------------------
def __textboxOK(event):
    global boxRoot
    boxRoot.quit()
"""
def _autoscroll(self): 											 #Additional fuction unused
	self.listbox_log.select_set(END)                             #Select the new item
	self.listbox_log.yview(END)                                  #Set the scrollbar to the end of the listbox
"""
def main():
	_setup()


if __name__ == '__main__':
    if True:
        main()