from pprint import pprint
import sys
import hashlib
import pandas as pd
import numpy as np
import os
final_list = []
file_permissions = 'common-permissions-rw.csv'

with open(file_permissions,'r') as list:
    for row in list:
        if "\n" in row:
            row = row.rstrip() # ?
        final_list.append(row)

chunks = []
times = []
data_file = 'permissions-rw.csv' # csv file with permissions
n = 3 # n-gram size
with open(data_file,'r') as permissions:
    row_number = 1
    for row in permissions:
        #print("Sample number: ", row_number)
        permissions = row.split(",")
        end = len(permissions) # amount of permissions and end of list
        start = 0
        while start < end - 1:
            n_gram = permissions[start:start+n]
            #print(n_gram, "->")
            first_match = 0
            clean_list = []
            for word in n_gram:
                clean_list.append(word.rstrip())
                if word in final_list:
                    first_match += 1
                else:
                    clean_list[-1] = 'X'
            n_gram = clean_list
            if first_match > 0:
                reversed_list = n_gram[::-1]
                count = len([i for i in n_gram if i=='X'])
                if n_gram not in chunks and count <= 1 and len(n_gram) == n and reversed_list not in chunks: # and reversed_list not in chunks:
                    # print("Reversed:",reversed_list)
                    chunks.append(n_gram)
                    times.append(1)
                    '''
                    to_md5 = ','.join(n_gram)
                    print(to_md5)
                    to_md5_1 = hashlib.md5(to_md5.encode())
                    print(sys.getsizeof(len(to_md5)))
                    print(len(to_md5_1.hexdigest())/2)
                    '''
                    #print(n_gram)
                if n_gram in chunks:
                    index = chunks.index(n_gram)
                    times[index] += 1
                start = start + 3
            else:
                start += 1
        row_number += 1

print("Amount of unique ngrams:", len(chunks))
#pprint(chunks)
amount_detector = pd.DataFrame({'Detector':chunks,
                                'Times':times})
amount_detector = amount_detector.sort_values(by=['Times'],ascending=False)
print(amount_detector.head(20))