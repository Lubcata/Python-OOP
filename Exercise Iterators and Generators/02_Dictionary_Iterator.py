class dictionary_iter:
    def __init__(self, dictionary: dict):
        self.items = list(dictionary.items())
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx == len(self.items) - 1:
            raise StopIteration

        self.idx += 1
        return self.items[self.idx]


#  not passing in judge but still correct
class dictionary_iterator:
    def __init__(self, dictionary: dict):  # {1: "1", 2: "2"}
        self.items = dictionary.items()  # dictionary.items() => dict_items([(1, "1"), (2, "2")])

    def __iter__(self):
        return iter(self.items)


result = dictionary_iter({1: "1", 2: "2"})
for x in result:
    print(x)
