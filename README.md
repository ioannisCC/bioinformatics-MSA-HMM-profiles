# bioinformatics-MSA-HMM-profiles


DNA Sequence Analysis Assignment

Overview

This repository provides code for processing and analyzing synthetic DNA sequences using various computational techniques. The assignment covers synthetic sequence generation, multiple sequence alignment (MSA), and Hidden Markov Model (HMM) construction.

Components

1. Synthetic Data Generation

Objective: Generate synthetic DNA sequences based on predefined patterns.

Patterns:

	•	pattern1 = AATTGA
	•	pattern2 = CGCTTAT
	•	pattern3 = GGACTCAT
	•	pattern4 = TTATTCGTA

Output: The code produces two datasets, datasetA and datasetB, saved in separate files.

2. Multiple Sequence Alignment (MSA)

Algorithm: Needleman-Wunsch for global alignment.

Scoring Scheme:

	•	Gap Penalty (α): Applied for horizontal and vertical transitions.
	•	Score (+1): Awarded for local similarity.
	•	Penalty (-α/2): Applied for local dissimilarity.

Process:

	•	Initialize the scoring matrix with gap penalties.
	•	Compute scores by evaluating the maximum value from three neighboring cells (top, left, diagonal).
	•	Perform traceback from the bottom-right to reconstruct the optimal alignment.

Output: Aligned sequences are saved to a file.

3. Hidden Markov Model (HMM)

Objective: Construct an HMM profile and compute alignment scores and paths for datasetB.

HMM Profile:

	•	Match States (M): Represent conserved positions with nucleotide frequencies.
	•	Insertion States (I): Model variable regions in aligned sequences.
	•	Deletion States (D): Handle gaps without emitting symbols.

Algorithm: Viterbi algorithm for finding the most probable sequence of hidden states and alignment scores.

Process:

	•	Calculate emission and transition probabilities.
	•	Use dynamic programming to find the most probable alignment path.

Usage

To generate synthetic data, run the provided scripts to produce datasetA and datasetB. For MSA, execute the alignment script on datasetA. To construct the HMM profile and compute scores, run the HMM script with datasetB.

Feel free to adjust the description as needed!
