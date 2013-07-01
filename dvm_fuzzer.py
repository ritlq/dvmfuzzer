#!/usr/bin/python

import time
import os
import zipfile
import sys
import config
import shutil
from subprocess import Popen, PIPE

# read in classes.dex
#def read_classes(self, path):
#	f = open(path, "rb")
#	fileData = f.read()
#	f.close()
#	return fileData

class Dvmfuzzer:
	def zuff(self, apkpath, fuzz_percent, loop_times):
		timed = time.asctime(time.localtime(time.time()))
		os.mkdir(timed)
		os.chdir(timed)
		
		# Create directories if doesn't exist
		if not os.path.exists("apk"):
			os.mkdir("apk")
		if not os.path.exists("dex"):
			os.mkdir("dex")
		if not os.path.exists("logcat"):
			os.mkdir("logcat")
		
		
		shutil.copyfile(apkpath, "apk/a.apk")
		
		# Extract classes.dex into dex directory
		#zfile = zipfile.ZipFile("apk/a.apk")
		#for name in zfile.namelist():
		#	(dirname, filename) = os.path.split(name)
		#	if filename.lower().strip() == "classes.dex":
		#		# Only extract the classes.dex
		#		fd = open(name,"w")
		#		fd.write(zfile.read(str("dex/"+name))
		#		fd.close()
		#		break
		
		stdout = Popen('unzip -j "apk/a.apk" "classes.dex" -d "dex"', shell=True, stdout=PIPE)
		stdout.wait()
				
		shutil.copyfile('dex/classes.dex', 'dex/orig_classes.dex')
				
		zuffstr = "cat dex/orig_classes.dex | zzuf -r " + fuzz_percent + " > dex/classes.dex"
		
		#Use aapt to fetch pakage name and main activity from apk file
		stdout = Popen(config.aapt+' dump badging apk/a.apk | awk -F" " \'/package/ {print $2}\'|awk -F"\'" \'/name=/ {print $2}\'', shell=True, stdout=PIPE).stdout
		pkg = stdout.read()
		stdout = Popen(config.aapt+' dump badging apk/a.apk | awk -F" " \'/launchable-activity/ {print $2}\'|awk -F"\'" \'/name=/ {print $2}\'', shell=True, stdout=PIPE).stdout
		act = stdout.read()

		stdout = Popen("cat dex/classes.dex | xxd > dex/orig_classes.txt", shell=True)
		stdout.wait()
		
		for i in range(int(loop_times)):
			
			stdout = Popen(zuffstr, shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen("cat dex/classes.dex | xxd > dex/"+str(i)+"_classes.txt", shell=True)
			stdout.wait()
			
			shutil.copyfile("dex/classes.dex", "dex/"+str(i)+"_classes.dex")
			
			stdout = Popen('zip -j "apk/a.apk" "dex/classes.dex"', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen(config.sdk+'/tools/zipalign -v -f 4 "apk/a.apk" "apk/b.apk"', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen('jarsigner -verbose -keystore '+'"'+config.androiddebugkey+'"'+' -storepass android -keypass android -digestalg SHA1 -sigalg MD5withRSA -sigfile CERT -signedjar "apk/a.apk" "apk/b.apk" androiddebugkey', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen(config.sdk+'/platform-tools/adb install "apk/a.apk"', shell=True, stdout=PIPE).stdout
			print "Installing"
			print stdout.read()
			
			stdout = Popen(config.sdk+'/platform-tools/adb shell am start -n '+pkg+'/'+act, shell=True, stdout=PIPE)
			print "Running"
			stdout.wait()
			
			stdout = Popen(config.sdk+'/platform-tools/adb logcat -c', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen(config.sdk+'/platform-tools/adb logcat -d > logcat/"$i"_logcat.txt', shell=True, stdout=PIPE)
			stdout.wait()

			print "Unistalling"
			stdout = Popen(config.sdk+'/platform-tools/adb shell rm -r /data/data/'+pkg, shell=True, stdout=PIPE)
			stdout.wait()
			stdout = Popen(config.sdk+'/platform-tools/adb uninstall '+pkg, shell=True, stdout=PIPE).stdout
			print stdout.read()

			

	def swapinstruction(self):
		
			
	def main(self):
		self.zuff('/root/Desktop/JetBoy-debug.apk', '0.004', '3')


		
if __name__ == "__main__":
    Dvmfuzzer().main()
	
	
