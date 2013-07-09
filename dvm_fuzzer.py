#!/usr/bin/python

import time
import os
import zipfile
import sys
import config
import shutil
from subprocess import Popen, PIPE
import re
import fnmatch
from math import floor
from random import randint

# read in classes.dex
#def read_classes(self, path):
#	f = open(path, "rb")
#	fileData = f.read()
#	f.close()
#	return fileData

class Dvmfuzzer:
	def getPkgAct(self, path):
		#Use aapt to fetch pakage name and main activity from apk file
		stdout = Popen(config.aapt+' dump badging '+path+' | awk -F" " \'/package/ {print $2}\'|awk -F"\'" \'/name=/ {print $2}\'', shell=True, stdout=PIPE).stdout
		pkg = stdout.read()
		stdout = Popen(config.aapt+' dump badging '+path+' | awk -F" " \'/launchable-activity/ {print $2}\'|awk -F"\'" \'/name=/ {print $2}\'', shell=True, stdout=PIPE).stdout
		act = stdout.read()
		return pkg, act

	def fuzz(self, apkpath, fuzz_percent, loop_times, type):
		timed = time.asctime(time.localtime(time.time()))
		os.mkdir(timed)
		os.chdir(timed)
		
		os.mkdir("apk")
		os.mkdir("dex")
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
				
		stdout = Popen("cat dex/classes.dex | xxd > dex/orig_classes.txt", shell=True)
		stdout.wait()
		
		pkg,act = self.getPkgAct("apk/a.apk")
		
		for i in range(int(loop_times)):
			
			if type is 'zuff':
				stdout = Popen("cat dex/orig_classes.dex | zzuf -r " + fuzz_percent + " > dex/classes.dex", shell=True, stdout=PIPE)
				stdout.wait()
			elif type is 'swap':
				self.swapinstruction(fuzz_percent)
				
			
			stdout = Popen("cat dex/classes.dex | xxd > dex/"+str(i)+"_classes.txt", shell=True)
			stdout.wait()
			
			shutil.copyfile("dex/classes.dex", "dex/"+str(i)+"_classes.dex")
			shutil.copyfile("apk/a.apk", "apk/b.apk")
			
			stdout = Popen('zip -j "apk/b.apk" "dex/classes.dex"', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen(config.sdk+'/tools/zipalign -v -f 4 "apk/b.apk" "apk/c.apk"', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen('jarsigner -verbose -keystore '+'"'+config.androiddebugkey+'"'+' -storepass android -keypass android -digestalg SHA1 -sigalg MD5withRSA -sigfile CERT -signedjar "apk/b.apk" "apk/c.apk" androiddebugkey', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen(config.sdk+'/platform-tools/adb install "apk/b.apk"', shell=True, stdout=PIPE).stdout
			print "Installing"
			print stdout.read()
			
			stdout = Popen(config.sdk+'/platform-tools/adb shell am start -n '+pkg.strip()+'/'+act, shell=True, stdout=PIPE)
			print "Running"
			stdout.wait()
			
			time.sleep(5)
			#insert monkeyrunner option here
			
			stdout = Popen(config.sdk+'/platform-tools/adb logcat -c', shell=True, stdout=PIPE)
			stdout.wait()
			
			stdout = Popen(config.sdk+'/platform-tools/adb logcat -d > logcat/'+str(i)+'_logcat.txt', shell=True, stdout=PIPE)
			stdout.wait()

			print "Unistalling"
			stdout = Popen(config.sdk+'/platform-tools/adb shell rm -r /data/data/'+pkg, shell=True, stdout=PIPE)
			stdout.wait()
			stdout = Popen(config.sdk+'/platform-tools/adb uninstall '+pkg, shell=True, stdout=PIPE).stdout
			print stdout.read()
		
		print "Done"	

			

	def swapinstruction(self, fuzz_percent):
		if not os.path.exists("dex/dexout"):
			os.mkdir("dex/dexout")
		
		stdout = Popen('java -jar '+config.baksmali+' -o dex/dexout dex/orig_classes.dex', shell=True, stdout=PIPE)
		stdout.wait()

		restring = ""
		with open('../instructions.txt') as f:
			parts = []
			for line in f:
				parts.append('^\s*'+line.rstrip('\n'))
			restring = re.compile('|'.join(parts))
			

		matches = []
		for root, dirnames, filenames in os.walk('dex/dexout'):
		  for filename in fnmatch.filter(filenames, '*.smali'):
			  matches.append(os.path.join(root, filename))

		linestore = []
		linenum = 0
		for file in matches:
			with open(file) as f:
				for line in f:
					if re.match(restring, line):
						details = {}
						details["linenum"] = linenum
						details["line"] = line
						linenum = linenum + 1
						linestore.append(details)
						
		totallines = linenum-1
		
		pair = [2]
		pairs = []
		for i in range(int(floor(totallines*float(fuzz_percent)))):
			pair.append(randint(0,totallines))
			pair.append(randint(0,totallines))
			pairs.append(pair)
			
		for p in pairs:
			linenum = 0
			for file in matches:
				with open("dex/temp", "wt") as out:
					with open(file) as f:
						for line in f:
							if linenum == p[0]:
								for l in linestore:
									if l["linenum"] == p[1]:
										out.write(l["line"])
							elif linenum == p[1]:
								for l in linestore:
									if l["linenum"] == p[0]:
										out.write(l["line"])
							else:
								out.write(line)
											
							if re.match(restring, line):
								linenum = linenum + 1
				
				#Remove original file
				os.remove(file)
				#Move new file
				shutil.move("dex/temp", file)

		stdout = Popen('java -Xmx512M -jar '+config.smali+' dex/dexout -o dex/classes.dex', shell=True, stdout=PIPE)
		stdout.wait()

	def main(self):
		self.fuzz('/root/Desktop/JetBoy-debug.apk', '0.004', '3', 'swap')
		#self.fuzz('/root/Desktop/JetBoy-debug.apk', '0.004', '3', 'zuff')


		
if __name__ == "__main__":
    Dvmfuzzer().main()
	
	
