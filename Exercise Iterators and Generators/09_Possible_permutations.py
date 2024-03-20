from itertools import permutations
def possible_permutations(numbers: list):
    for number in permutations(numbers):
        yield list(number)





[print(n) for n in possible_permutations([1, 2, 3])]