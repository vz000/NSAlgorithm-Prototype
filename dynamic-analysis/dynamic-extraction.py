import os
import time

for i in range(1,10): # change for a list of the dir files
    sample_number = i
    sample_name = "./SafeSamples/g-sample" + str(sample_number) + ".apk"
    os.system('aapt dump badging ' + sample_name +' > aapt_output.txt')
    get_line = open('aapt_output.txt','r',encoding="utf8")
    try:
        first_line = get_line.readlines()[0]
        pkg_name = first_line.split(' ')[1].split('=')[1].strip("'")
        print(pkg_name)
        os.system('adb install ' + sample_name)
        os.system("adb shell monkey -p " + pkg_name + " 1")
        time.sleep(10)
        os.system('adb shell "ps -e | grep ' + pkg_name + '" > pid.txt')
        get_line = open("pid.txt",'r',encoding="utf8")
        first_line = get_line.readlines()[0]
        process_output = first_line.split(' ')
        pid = [x for x in process_output if x != '']
        file_logs = '/data/app/logs-sequence'+str(sample_number)+'.txt'
        os.system('adb shell "timeout 15 strace -p ' + str(pid[1]) + ' -o '+ file_logs + '"')
        os.system('adb shell monkey -p ' + pkg_name + " -v 50")
        time.sleep(20)
    except Exception as e:
        print("Deleting APK...")
        #os.remove(sample_name)
        print(e)
