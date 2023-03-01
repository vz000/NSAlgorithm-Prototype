from draft_static_detectors import Permission_Ngram

n = 3
generate_all_detectors = Permission_Ngram('permissions-rw.csv','rw',n)
first_detector_set = generate_all_detectors.get_draft_detectors()
permission_list = generate_all_detectors.get_permission_list()
print("FIRST DETECTOR SET")
print(first_detector_set)
selfset = []
r = 3
with open('permissions-gw.csv') as selfDataset:
    for row in selfDataset:
        local_ngrams = []
        permissions = row.split(",")
        start = 0
        n_local_ngrams = 0
        while n_local_ngrams < r:
            n_gram = permissions[start:start+n]
            clean_list = []
            if len(n_gram) >= n:
                for word in n_gram:
                    if word in permission_list:
                        exp = permission_list.index(word.rstrip())
                        clean_list.append(2**exp)
                    else:
                        clean_list.append(0)
                n_gram = clean_list[0] | clean_list[1] | clean_list[2]
                if n_gram not in local_ngrams:
                    local_ngrams.append(n_gram)
                    start = start + n
                else:
                    start += 1
            n_local_ngrams += 1
        selfset.append(local_ngrams)

print("SELFSET\n")
print(selfset)