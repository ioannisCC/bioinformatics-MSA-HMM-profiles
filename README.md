# bioinformatics-MSA-HMM-profiles


Overview

This assignment involves the processing and analysis of synthetic DNA sequences using various computational methods:

	Synthetic Data Generation:
			Objective: Generate synthetic DNA sequences using specific patterns.
			Patterns: pattern1=ΑΑΤΤGA, pattern2=CGCTTAT, pattern3=GGACTCAT, pattern4=TTATTCGTA.
			Data Output: Two datasets, datasetA and datasetB, are produced and stored in separate files.
	2.	Multiple Sequence Alignment (MSA):
			Algorithm: Implementation of the Needleman-Wunsch algorithm for global alignment.
			Scoring Scheme:
			Gap penalty (α) for horizontal and vertical transitions.
			Score (+1) for local similarity.
			Penalty (-α/2) for local dissimilarity.
			Process:
			Matrix initialization with gap penalties.
			Scoring matrix computation by evaluating the maximum value from three neighboring cells.
			Traceback from the bottom-right to reconstruct the optimal alignment.
			Output: A file containing aligned sequences.
	3.	Hidden Markov Model (HMM):
			Objective: Construct an HMM profile and compute alignment scores and paths for datasetB.
			HMM Profile:
			Match States (M): Represent conserved positions with nucleotide frequencies.
			Insertion States (I): Model variable regions in aligned sequences.
			Deletion States (D): Handle gaps without emitting symbols.
			Algorithm: Implementation of the Viterbi algorithm for finding the most probable sequence of hidden states and alignment scores.
			Process:
			Calculate emission and transition probabilities.
			Use dynamic programming to find the most probable alignment path.

This assignment integrates synthetic data generation, sequence alignment, and probabilistic modeling to analyze and align DNA sequences.
