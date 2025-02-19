#!/usr/bin/env python3
import argparse
import csv
import re

def extract_sequences_to_fasta(tab_file_path, fasta_file_path):
    """
    Extract unique sequences from a tab-delimited file and save them in FASTA format.
    Parameters:
    -----------
    tab_file_path: str
        Path to the tab-delimited file containing sequences
    fasta_file_path: str
        Path to write the output FASTA file
    """
    print(f"Processing tab file: {tab_file_path}")
    # Extract unique sequences from the tab file
    unique_sequences = set()
    with open(tab_file_path, 'r') as tab_file:
        reader = csv.reader(tab_file, delimiter='\t')
        # Get the header row and find the sequence column index
        header = next(reader)
        try:
            seq_col_idx = header.index('sequence')
        except ValueError:
            print("Error: Could not find 'sequence' column in the tab file")
            return

        # Compile regex pattern to match only uppercase A-Z
        pattern = re.compile(r'[^A-Z]')

        # Extract unique sequences
        for row in reader:
            if len(row) > seq_col_idx:
                original_sequence = row[seq_col_idx].strip()
                if original_sequence:
                    unique_sequences.add(original_sequence)

    # Write sequences to FASTA file
    print(f"Writing {len(unique_sequences)} unique sequences to: {fasta_file_path}")
    with open(fasta_file_path, 'w') as fasta_file:
        for original_sequence in sorted(unique_sequences):
            # Clean the sequence for the sequence line (only keep A-Z)
            cleaned_sequence = re.sub(r'[^A-Z]', '', original_sequence)
            fasta_file.write(f">{original_sequence}\n{cleaned_sequence}\n")

    print(f"FASTA file generation complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract unique sequences to FASTA format')
    parser.add_argument('tab_file', help='Path to the tab-delimited file')
    parser.add_argument('fasta_file', help='Path to write the output FASTA file')
    args = parser.parse_args()
    extract_sequences_to_fasta(args.tab_file, args.fasta_file)
