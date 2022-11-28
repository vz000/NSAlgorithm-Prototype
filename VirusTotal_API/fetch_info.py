from hashlib import md5
import time
from virus_total_apis import PublicApi
from pprint import pprint
import csv

API_KEY = "APIKEY1"
API_KEY2 = "APIKEY2" # in case of running out of daily requests
api = PublicApi(API_KEY)
completeList = []
num_of_rows = 0

with open("benignAPKv2.csv", 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            print(row)
            inputRow = [row[0],row[1]]
            completeList.append(inputRow)
            num_of_rows+=1

num_api_calls = 0
saveToFile = []
for i in range(0,201):
    file_hash = completeList[i][1]
    response = api.get_file_report(file_hash)
    num_api_calls+=1
    print("\nNumber of API call: ", i)
    print("---------------- {id} ----------------".format(id=completeList[i][0]))
    saveToFile.append(completeList[i][0])
    if response["response_code"] == 200:
        try:
            if response["results"]["positives"] > 0:
                print("Considerar archivo como sospechoso.")
            else:
                print("Archivo seguro para su uso.")
        except:
            print("Archivo no encontrado")
            continue
    else:
        print("No ha podido obtenerse el análisis del archivo.")
    print(num_api_calls)
    # so I won't have to copy and paste everything.
    print("Link:")
    print(response["results"]["permalink"])
    if num_api_calls == 4:
        time.sleep(60)
        num_api_calls = 0

with open("download2.csv",'w+') as to_download:
    writer = csv.writer(to_download)
    for row in saveToFile:
        writer.writerow([row])