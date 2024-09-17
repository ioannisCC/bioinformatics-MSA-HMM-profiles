import numpy as np

# Define DNA characters and their indices
DNA_chars = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

def forward_algorithm(sequence, A, B, pi):
    T = len(sequence)
    N = len(A)
    
    alpha = np.zeros((N, T))
    
    # Initialization
    alpha[:, 0] = pi * B[:, sequence[0]]
    
    # Induction
    for t in range(1, T):
        alpha[:, t] = np.sum(alpha[:, t-1] * A.T, axis=1) * B[:, sequence[t]]
    
    return alpha

def backward_algorithm(sequence, A, B):
    T = len(sequence)
    N = len(A)
    
    beta = np.zeros((N, T))
    
    # Initialization
    beta[:, T-1] = 1
    
    # Induction
    for t in range(T-2, -1, -1):
        beta[:, t] = np.sum(A * B[:, sequence[t+1]] * beta[:, t+1], axis=1)
    
    return beta


def expectation_step(sequence, A, B, pi, alpha, beta):
    T = len(sequence)
    N = len(A)
    
    gamma = np.zeros((N, T))
    xi = np.zeros((N, N, T-1))
    
    # Compute gamma
    for t in range(T):
        denom = np.sum(alpha[:, t] * beta[:, t])
        gamma[:, t] = (alpha[:, t] * beta[:, t]) / denom if denom != 0 else 0
    
    # Compute xi
    for t in range(T-1):
        denom = np.sum(alpha[:, t] * beta[:, t])
        for i in range(N):
            for j in range(N):
                xi[i, j, t] = (alpha[i, t] * A[i, j] * B[j, sequence[t+1]] * beta[j, t+1]) / denom if denom != 0 else 0
    
    return gamma, xi

def maximization_step(sequence, A, B, gamma, xi):
    N, T = gamma.shape[0], gamma.shape[1]
    
    # Update pi
    pi = gamma[:, 0]
    
    # Update A
    for i in range(N):
        denom = np.sum(gamma[i, :T-1])
        if denom != 0:
            A[i, :] = np.sum(xi[i, :, :T-1], axis=1) / denom
        else:
            A[i, :] = np.zeros(N)  # Handle division by zero case
    
    # Update B
    for j in range(N):
        for k in range(len(DNA_chars)):
            denom = np.sum(gamma[j, :])
            if denom != 0:
                B[j, k] = np.sum(gamma[j, sequence == k]) / denom
            else:
                B[j, k] = 0.0  # Handle division by zero case
    
    return A, B, pi



def baum_welch(sequences, num_states, num_chars, num_iterations):
    # Initialize transition matrix A, emission matrix B, initial state distribution pi
    A = np.random.rand(num_states, num_states)
    A = A / np.sum(A, axis=1, keepdims=True)  # Normalize rows to sum to 1
    
    B = np.random.rand(num_states, num_chars)
    B = B / np.sum(B, axis=1, keepdims=True)  # Normalize rows to sum to 1
    
    pi = np.random.rand(num_states)
    pi = pi / np.sum(pi)  # Normalize to sum to 1
    
    for iteration in range(num_iterations):
        for sequence in sequences:
            alpha = forward_algorithm(sequence, A, B, pi)
            beta = backward_algorithm(sequence, A, B)
            gamma, xi = expectation_step(sequence, A, B, pi, alpha, beta)
            A, B, pi = maximization_step(sequence, A, B, gamma, xi)
    
    return A, B, pi

# Example usage
if __name__ == "__main__":
    sequences = [
        [0, 1, 2, 3, 0, 1, 2, 3],   # Example DNA sequence (ACGTACGT)
        [1, 2, 0, 3, 0, 2, 1, 3]    # Another example DNA sequence (CGTAGCTA)
    ]
    num_states = 3   # Number of states in the HMM
    num_chars = len(DNA_chars)    # Number of DNA characters
    
    num_iterations = 100  # Number of Baum-Welch iterations
    
    A, B, pi = baum_welch(sequences, num_states, num_chars, num_iterations)
    
    print("Estimated Transition Matrix A:")
    print(A)
    print("\nEstimated Emission Matrix B:")
    print(B)
    print("\nEstimated Initial State Distribution pi:")
    print(pi)
