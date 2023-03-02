from draft_static_detectors import Permission_Ngram

class TrainNSA():
    def __init__(self, n : int, nonSelfDataset : str, selfDataset : str, r : int) -> None:
        self.n = n
        self.r = r
        self.selfset = []
        self.detector_set = []
        self.selfDataset = selfDataset
        generate_all_detectors = Permission_Ngram(nonSelfDataset,'rw',n)
        self.first_detector_set = generate_all_detectors.get_draft_detectors()
        self.permission_list = generate_all_detectors.get_permission_list()

    def __generateSelfDetectors(self) -> None:
        with open(self.selfDataset) as dataset:
            for row in dataset:
                local_ngrams = []
                permissions = row.split(",")
                start = 0
                n_local_ngrams = 0
                while n_local_ngrams < self.r:
                    n_gram = permissions[start:start+self.n]
                    clean_list = []
                    if len(n_gram) >= self.n:
                        for word in n_gram:
                            if word in self.permission_list:
                                exp = self.permission_list.index(word.rstrip())
                                clean_list.append(2**exp)
                            else:
                                clean_list.append(0)
                        n_gram = clean_list[0] | clean_list[1] | clean_list[2]
                        if n_gram not in local_ngrams:
                            local_ngrams.append(n_gram)
                            start = start + self.n
                        else:
                            start += 1
                    n_local_ngrams += 1
                self.selfset.append(local_ngrams)

    def __generateNonSelf(self) -> None:
        for ngram in self.first_detector_set:
            match = 0
            for chunk in self.selfset:
                if ngram in chunk:
                    match = 1
            if match == 0:
                self.detector_set.append(ngram)
    
    def fit(self) -> list:
        self.__generateSelfDetectors()
        self.__generateNonSelf()
        return self.detector_set

model = TrainNSA(3,'permissions-rw.csv','permissions-gw.csv',3)
print(model.fit())