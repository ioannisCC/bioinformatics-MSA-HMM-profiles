import numpy as np


# initialize matrix with penalties
def initialize_matrix(n: int, m: int, gap_penalty: int):

    matrix = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1):
        matrix[i][0] = matrix[i-1][0] + gap_penalty # intialize the first row based on gap penalty
    for j in range(1, m + 1):
        matrix[0][j] = matrix[0][j-1] + gap_penalty # intialize the first column based on gap penalty

    return matrix

# compute the score for a current cell in the matrix
def calculate_scores(sequence1: list, sequence2: list, gap_penalty: int, match_reward: int, mismatch_penalty: int):

    n, m = len(sequence1), len(sequence2)
    matrix = initialize_matrix(n=n, m=m, gap_penalty=gap_penalty)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if sequence1[i - 1] == sequence2[j - 1]: # if the two characters are the same (they match)
                score_diagonal = matrix[i - 1][j - 1] + match_reward # add match reward
            else: # if the two characters are not the same (mismatch)
                score_diagonal = matrix[i - 1][j - 1] + mismatch_penalty # add mismatch penalty
            score_up = matrix[i - 1][j] + gap_penalty
            score_left = matrix[i][j - 1] + gap_penalty
            matrix[i][j] = max(score_diagonal, score_up, score_left) # get the max score out of the three cases
    
    return matrix

# get the best alignment
def traceback(matrix: list, sequence1: list, sequence2: list, gap_penalty: int, match_reward: int, mismatch_penalty: int):

    aligned_sequence1 = ""
    aligned_sequence2 = ""
    i, j = len(sequence1), len(sequence2)
    penalty_or_reward = -100
    
    while i > 0 and j > 0:
        score = matrix[i][j] # begin from the right down edge of the matrix
        score_diagonal = matrix[i - 1][j - 1]
        score_up = matrix[i - 1][j]
        
        # check if characters are the same to add reward or penalty
        if sequence1[i - 1] == sequence2[j - 1]:
            penalty_or_reward = match_reward
        else:
            penalty_or_reward = mismatch_penalty
        
        if score == score_diagonal + penalty_or_reward:
            aligned_sequence1 = sequence1[i - 1] + aligned_sequence1
            aligned_sequence2 = sequence2[j - 1] + aligned_sequence2
            i -= 1
            j -= 1
        elif score == score_up + gap_penalty: # if the score came from up then is a gap for sequence 2
            aligned_sequence1 = sequence1[i - 1] + aligned_sequence1
            aligned_sequence2 = "-" + aligned_sequence2
            i -= 1
        else:  # any other case, if the score came from left then is a gap for sequence 1
            aligned_sequence1 = "-" + aligned_sequence1
            aligned_sequence2 = sequence2[j - 1] + aligned_sequence2
            j -= 1

    while i > 0: # handle the situation where the top row of the scoring matrix were reached
        aligned_sequence1 = sequence1[i - 1] + aligned_sequence1
        aligned_sequence2 = "-" + aligned_sequence2
        i -= 1

    while j > 0: # handle the situation where the leftmost column of the scoring matrix were reached
        aligned_sequence1 = "-" + aligned_sequence1
        aligned_sequence2 = sequence2[j - 1] + aligned_sequence2
        j -= 1
    
    return aligned_sequence1, aligned_sequence2

# perform MSA
def multiple_sequence_alignment(sequences: list, alpha: int):
    
    gap_penalty = -alpha
    match_reward = 1
    mismatch_penalty = -alpha / 2
    
    aligned_sequences = [sequences[0]]

    print('\nDataset')
    for sequence in sequences:
        print(sequence)
    print('\n')
    length = len(sequences)
    
    for i in range(1, length):
        sequence1 = aligned_sequences[-1]
        sequence2 = sequences[i]
        
        matrix = calculate_scores(sequence1=sequence1, sequence2=sequence2, gap_penalty=gap_penalty, match_reward=match_reward, mismatch_penalty=mismatch_penalty)
        aligned_sequence1, aligned_sequence2 = traceback(matrix=matrix, sequence1=sequence1, sequence2=sequence2, gap_penalty=gap_penalty, match_reward=match_reward, mismatch_penalty=mismatch_penalty)
        
        aligned_sequences[-1] = aligned_sequence1
        aligned_sequences.append(aligned_sequence2)
    
    return aligned_sequences

if __name__ == "__main__":

    dataset = []

    with open('datasetA', 'r') as file:
        lines = file.readlines()
        for line in lines:
            dataset.append(line.strip())

    alpha = 1 # since both AM end in an odd number 

    aligned_sequences = multiple_sequence_alignment(sequences=dataset, alpha=alpha)

    with open('aligned_sequences', 'w') as file:
        for sequence in aligned_sequences:
            file.write(sequence + "\n")

    print('\nAligned Dataset')
    for result in aligned_sequences:
        print(result)
