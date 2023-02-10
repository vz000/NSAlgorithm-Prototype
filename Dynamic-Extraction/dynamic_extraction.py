import os

# Must run in a loop to complete the validation process: 
# 5 apks deleted from original repo.
# Only installing 50
for i in range(0,50):
    sample_number = i
    sample_name = "./SafeSamples/g-sample" + str(sample_number) + ".apk"
    os.system('aapt dump badging ' + sample_name +' > aapt_output.txt')
    get_line = open('aapt_output.txt','r',encoding="utf8")
    try:
        first_line = get_line.readlines()[0]
        pkg_name = first_line.split(' ')[1].split('=')[1].strip("'")
        print(pkg_name)
        output = os.system('adb install ' + sample_name)
    except:
        print("Deleting APK...")
        os.remove(sample_name)
