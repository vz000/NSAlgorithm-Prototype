from pprint import pprint
final_list = []
file_permissions = 'common-permissions-rw.csv'

with open(file_permissions,'r') as list:
    for row in list:
        if "\n" in row:
            row = row.rstrip() # ?
        final_list.append(row)

chunks = []
data_file = 'permissions-rw.csv' # csv file with permissions
n = 3 # n-gram size
with open(data_file,'r') as permissions:
    row_number = 1
    for row in permissions:
        permissions = row.split(",")
        end = len(permissions) # amount of permissions and end of list
        start = 0
        while start < end - 1:
            n_gram = permissions[start:start+n]
            first_match = 0
            for word in n_gram:
                if word in final_list:
                    first_match += 1
            if first_match > 0:
                if n_gram not in chunks:
                    chunks.append(n_gram)
                start = start + first_match + 1
            else:
                start += 1
        row_number += 1

pprint(chunks)
print("Amount of ngrams:", len(chunks))
