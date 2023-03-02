import os
import csv
import xml.etree.ElementTree as ET

# To simulate the real case. Normal apps are stored inside of /data/app/
folderName = "./data/app/"
apkList = os.listdir(folderName)
print(len(apkList))

# In this part of the solution, we need to read the permissions, which are located inside
# of AndroidManifest.xml. Sources are not needed.

for apk_number in range(0,len(apkList)):
    apkLocation = folderName + apkList[apk_number]
    try:
        os.system('apktool d -s ' + apkLocation + ' -o ./data/unpackaged -f')
        manifestTree = ET.parse('./data/unpackaged/AndroidManifest.xml')
        manifestRoot = manifestTree.getroot()
        appPermissions = []
        for manifestChild in manifestRoot:
            if manifestChild.tag == 'uses-permission' or manifestChild.tag == 'permission':
                manifestChildAttr = list(manifestChild.attrib.keys())
                permission = manifestChild.attrib[manifestChildAttr[0]].split(".")
                appPermissions.append(permission[-1])

        with open('./data/permissions.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(appPermissions)
    except:
        print("Deleting APK...")
        os.remove(apkLocation)
