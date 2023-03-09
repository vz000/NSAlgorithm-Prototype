import os
import time
from threading import Thread

folderName = "./Ramples/"
apkList = os.listdir(folderName)

def start_strace(pid, file_logs):
    os.system('adb shell "timeout 15 strace -p ' + str(pid) + ' -o '+ file_logs + '"')

number = 50 # Ransomware cannot be automated!
# 50 was the last one
apk_number = apkList[number]
apkLocation = folderName + apkList[number] # equals sample_name
os.system('aapt dump badging ' + apkLocation +' > aapt_output.txt')
get_line = open('aapt_output.txt','r',encoding="utf8")
try:
	first_line = get_line.readlines()[0]
	pkg_name = first_line.split(' ')[1].split('=')[1].strip("'")
	print("RW sample: ", apk_number)
	print(pkg_name)
	os.system('adb install ' + apkLocation)
	os.system("adb shell monkey -p " + pkg_name + " 1")
	os.system('adb shell "ps -e | grep ' + pkg_name + '" > pid.txt')
	get_line = open("pid.txt",'r',encoding="utf8")
	first_line = get_line.readlines()[0]
	process_output = first_line.split(' ')
	pid = [x for x in process_output if x != '']
	file_logs = '/data/app/logs-sequence-'+apk_number+'.txt'
	ex_strace = Thread(target=start_strace, args=(pid[1], file_logs))
	ex_strace.start()
	print("Waiting for strace to finish...")
	ex_strace.join()
	os.system('adb pull '+ file_logs)
except Exception as e:
	print("Deleting APK...")
	os.remove(apkLocation)
	print(e)

