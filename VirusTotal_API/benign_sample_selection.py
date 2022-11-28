# Use sample function from random
# THIS IS VERSION 3.1 (LATE OCT 2022) FROM THE ORIGINAL SCRIPT RAN IN EARLY OCT 2022
from random import sample
import csv

fileNumber = 0
rowNumber = 1
fileName = "Ben" + str(fileNumber) + ".csv"
completeList = []
for fileNumber in range(0,5):
    with open(fileName, 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        # Iterate over each row after the header in the csv
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            inputRow = [rowNumber,row[0]]
            completeList.append(inputRow)
            rowNumber+=1

oldList = []
with open('benignAPK.csv','r') as old_file:
    csv_reader = csv.reader(old_file)
    for row in csv_reader:
        oldList.append(row[0])

# Selección probabilística simple
newList = []
for row in completeList:
    if row[0] in oldList:
        continue
    else:
        newList.append([row[0],row[1]])

# second argument may be changed depending of the number of samples required.
reducedList = sample(newList,400)
with open('benignAPKv2.csv','w+',encoding='UTF8') as order_file:
    writer = csv.writer(order_file)
    for row in reducedList:
        writer.writerow(row)