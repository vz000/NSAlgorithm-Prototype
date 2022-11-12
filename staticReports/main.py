import os

apk_list = os.listdir('./Safe/')
print(apk_list)
for apk in apk_list:
	os.system("./getReport.sh "+str(apk))
