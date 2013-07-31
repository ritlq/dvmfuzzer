31/7/2013: 	Fix bug that prevent working with big apk.
			Deletes META-INF in apk to prevent cert error when installing

Todo:

Intergrate program with GUI


How to use:

Edit config.py to state the paths to dependencies

Install zuff for byte changing method
http://caca.zoy.org/wiki/zzuf

Download smali/baksmali for instruction swapping method
State the path to smali/baksmali in config.py
https://code.google.com/p/smali/

Download and install EasyGUI
http://easygui.sourceforge.net/

-Start android emulator
-Edit line 185 in dvm_fuzzer.py then run it

dvm_fuzzer.py is the backend
gui.py(frontend) is to be intergrated
