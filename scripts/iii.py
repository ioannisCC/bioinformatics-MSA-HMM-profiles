import numpy as np
from collections import Counter
import pandas as pd


def emission_probabilities(aligned_sequences: list, chars: list):

    emission_probabilities = {}
    aligned_length = len(aligned_sequences[0])
    
    for position in range(aligned_length):
        counts = Counter(sequence[position] for sequence in aligned_sequences)  # count characters at this position across all sequences
        emission_probabilities[position] = {}

        total_count = sum(counts.values())  # total count of characters at this position

        for char in chars:
            if total_count > 0:
                emission_probabilities[position][char] = counts.get(char, 0) / total_count
            else:
                emission_probabilities[position][char] = 0.0
    
    return emission_probabilities

def transition_probabilities(aligned_sequences: list):
    transitions = {} # counts of transitions between states
    state_count = {} # total count of transitions from each state
    
    for sequence in aligned_sequences:
        previous_state = "S" # start
        if previous_state not in transitions:
            transitions[previous_state] = {}
        if previous_state not in state_count:
            state_count[previous_state] = 0

        for char in sequence:
            if char == "-":
                current_state = "D"  # deletion
            else:
                current_state = "M"  # match
            
            if current_state not in transitions[previous_state]:
                transitions[previous_state][current_state] = 0
            transitions[previous_state][current_state] += 1
            state_count[previous_state] += 1

            previous_state = current_state
            if previous_state not in transitions:
                transitions[previous_state] = {}
            if previous_state not in state_count:
                state_count[previous_state] = 0
        
        if "E" not in transitions[previous_state]:
            transitions[previous_state]["E"] = 0
        transitions[previous_state]["E"] += 1  # end
        state_count[previous_state] += 1

    # 'I' states
    for state in transitions:
        if "I" not in transitions[state]:
            transitions[state]["I"] = 0
        transitions[state]["I"] += 1
        state_count[state] += 1

    transition_probabilities = {}
    for previous_state in transitions:
        transition_probabilities[previous_state] = {}
        for current_state in transitions[previous_state]:
            this_transitions = transitions[previous_state][current_state]
            sum_of_transitions = state_count[previous_state]
            transition_probabilities[previous_state][current_state] =  this_transitions / sum_of_transitions
    
    return transition_probabilities


def viterbi_algorithm(sequence: str, emission_probabilities: list, transition_probabilities: list, chars: list):
    sequence_length = len(sequence)
    emission_probabilities_length = len(emission_probabilities)
    
    # Viterbi matrix and path matrix
    viterbi_matrix = np.zeros((emission_probabilities_length + 1, sequence_length + 1))
    path_matrix = np.zeros((emission_probabilities_length + 1, sequence_length + 1), dtype=int)
    
    # initialize
    for i in range(1, emission_probabilities_length + 1):
        viterbi_matrix[i][0] = viterbi_matrix[i-1][0] + np.log(transition_probabilities["S"]["M"])
    for j in range(1, sequence_length + 1):
        viterbi_matrix[0][j] = -(10e-8)
    
    # add small value to log to prevent log(0)
    small_value = 1e-8
    
    for i in range(1, emission_probabilities_length + 1):
        for j in range(1, sequence_length + 1):
            char = sequence[j-1]
            if char not in chars:
                continue
            
            match = viterbi_matrix[i-1][j-1] + np.log(transition_probabilities["M"]["M"] + small_value) + np.log(emission_probabilities[i-1][char] + small_value)
            delete = viterbi_matrix[i-1][j] + np.log(transition_probabilities["M"]["D"] + small_value)
            insert = viterbi_matrix[i][j-1] + np.log(transition_probabilities["M"]["I"] + small_value) + np.log(emission_probabilities[i-1][char] + small_value)
            
            viterbi_matrix[i][j] = max(match, delete, insert)
            
            if viterbi_matrix[i][j] == match:
                path_matrix[i][j] = 1  # match state
            elif viterbi_matrix[i][j] == delete:
                path_matrix[i][j] = 2  # delete state
            else:
                path_matrix[i][j] = 3  # insert state
    
    # traceback
    i, j = emission_probabilities_length, sequence_length
    aligned_sequence = ""
    while i > 0 and j > 0:
        if path_matrix[i][j] == 1:
            aligned_sequence = sequence[j-1] + aligned_sequence
            i -= 1
            j -= 1
        elif path_matrix[i][j] == 2:
            aligned_sequence = "-" + aligned_sequence
            i -= 1
        else:
            aligned_sequence = sequence[j-1] + aligned_sequence
            j -= 1
    
    while i > 0:
        aligned_sequence = "-" + aligned_sequence
        i -= 1
    while j > 0:
        aligned_sequence = sequence[j-1] + aligned_sequence
        j -= 1

    alignment_score = viterbi_matrix[emission_probabilities_length][sequence_length]
    
    return aligned_sequence, alignment_score

if __name__ == "__main__":

    aligned_sequencesA = []
    with open('aligned_sequences.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            aligned_sequencesA.append(line.strip())

    # pad the sequneces with '-' at the end to have the same length
    max_length = max(len(seq) for seq in aligned_sequencesA)
    aligned_sequencesA = [seq.ljust(max_length, '-') for seq in aligned_sequencesA]

    # allowed chars
    chars = "ACGT"

    emission_probabilities_aligned_datasetA = emission_probabilities(aligned_sequences=aligned_sequencesA, chars=chars)
    transition_probabilities_aligned_datasetA = transition_probabilities(aligned_sequences=aligned_sequencesA)

    # convert to pandas DataFrame for better presentation
    df = pd.DataFrame(emission_probabilities_aligned_datasetA).fillna(0.000001).transpose()
    print("\nEmission Probability Table aligned DatasetA")
    print(df)

    df = pd.DataFrame(transition_probabilities_aligned_datasetA).fillna(0.000001).transpose()
    print("\nTransition Probability Table aligned DatasetA")
    print(df)

    print('\n')

    dataset = []
    with open('datasetB.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            dataset.append(line.strip())
    
    # pad the sequneces with '-' at the end to have the same length
    max_length = max(len(seq) for seq in dataset)
    sequencesB = [seq.ljust(max_length, '-') for seq in dataset]

    emission_probabilities_aligned_datasetB = emission_probabilities(aligned_sequences=sequencesB, chars=chars)
    transition_probabilities_aligned_datasetB = transition_probabilities(aligned_sequences=sequencesB)

    for sequence in sequencesB:
        aligned_sequence, score = viterbi_algorithm(sequence=sequence, emission_probabilities=emission_probabilities_aligned_datasetB, transition_probabilities=transition_probabilities_aligned_datasetB, chars=chars)
        print(f"Sequence: {sequence}")
        print(f"Aligned Sequence: {aligned_sequence}")
        print(f"Alignment Score: {score}\n")
