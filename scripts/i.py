import random


def string_composition(strings: list):

    patterns = [
    'AATTGA',
    'CGCTTAT',
    'GGACTCAT',
    'TTATTCGTA'
    ]
    alphabet = ['A', 'C', 'G', 'T']
    new_string = ""

    for i in range(random.randint(1, 3)):
        new_string += alphabet[i]  # (random.randint(1, 3) returns 1 or 2 or 3

    for pattern in patterns:
        print(pattern, " PATTERN \n")
        pattern_list = list(pattern)  # converting pattern to list in order to modify it https://stackoverflow.com/questions/1228299/changing-a-character-in-a-string
        number_of_replacements = random.randint(0, 2) # up to 2 replacements
        
        for replacement in range(number_of_replacements):
            to_be_replaced_symbol_index = random.randint(0, len(pattern)-1)

            if random.randint(0,1):
                # if 1 (if true)  to_be_replaced_symbol_index will be replaced with another symbol
                replacement_symbol_index = random.randint(0, len(pattern)-1)
                print(to_be_replaced_symbol_index, "the symbol will be replaced which is the: ", pattern[to_be_replaced_symbol_index], ",will be replaced with the following:", pattern[replacement_symbol_index])
                pattern_list[to_be_replaced_symbol_index] = pattern_list[replacement_symbol_index]
            else:
                # it will be replaced with an empty string ""
                print(to_be_replaced_symbol_index, "the symbol which is the: ", pattern[to_be_replaced_symbol_index], ",will be deleted")
                pattern_list[to_be_replaced_symbol_index] = ""

        pattern = "".join(pattern_list)
        print(pattern)
        new_string += pattern
    
    for symbol in range(random.randint(1, 2)):  # add 1 or 2 symbols from the alphabet into the new_string
        new_string += alphabet[random.randint(0, 3)]

    strings.append(new_string)

def generate_datasets():

    strings = []
    for x in range(50):
        string_composition(strings=strings)  

    datasetA = random.sample(strings, 15)    #https://stackoverflow.com/questions/15511349/select-50-items-from-list-at-random
    datasetB = [s for s in strings if s not in datasetA]

    with open('datasetA', 'w') as file:
        for sequence in datasetA:
            file.write(sequence + "\n")

    with open('datasetB', 'w') as file:
        for sequence in datasetB:
            file.write(sequence + "\n")

    return datasetA, datasetB


if __name__ == "__main__":

    print('\n')
    A, B = generate_datasets()

    print('Dataset A' + '\n')
    for sequence in A:
        print(sequence + '\n')

    print('Dataset B' + '\n')
    for sequence in B:
        print(sequence + '\n')
