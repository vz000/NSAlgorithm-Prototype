import os
import xml.etree.ElementTree as ET
from pprint import pprint

folderName = "../downloads/"
apkList = os.listdir(folderName)
pprint(apkList)

# In this part of the solution, we need to read the permissions, which are located inside
# of AndroidManifest.xml. Sources are not needed.
for apk in apkList:
    apkLocation = folderName + apk
    os.system('apktool d -s ' + apkLocation + ' -o permissionsExtraction -f')
    manifestTree = ET.parse('./permissionsExtraction/AndroidManifest.xml')
    manifestRoot = manifestTree.getroot()
    for manifestChild in manifestRoot:
        if manifestChild.tag == 'uses-permission':
            manifestChildAttr = list(manifestChild.attrib.keys())
            permission = manifestChild.attrib[manifestChildAttr[0]]
            print(permission)