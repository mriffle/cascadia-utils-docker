#!/usr/bin/env python3
import sys

def concat_tab_files(file_list):
    """
    Concatenate tab-delimited files, keeping only the header from the first file.
    """
    if not file_list:
        print("Error: No input files provided.", file=sys.stderr)
        return 1

    try:
        # Process the first file - keep header and content
        with open(file_list[0], 'r') as first_file:
            header = first_file.readline()
            print(header, end='')  # Print header
            # Print rest of first file
            for line in first_file:
                print(line, end='')

        # Process the remaining files - skip header
        for filename in file_list[1:]:
            with open(filename, 'r') as current_file:
                # Skip header line
                current_file.readline()
                # Print content
                for line in current_file:
                    print(line, end='')

        return 0

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python concat_tab_files.py file1.tsv file2.tsv [file3.tsv ...]", file=sys.stderr)
        sys.exit(1)

    exit_code = concat_tab_files(sys.argv[1:])
    sys.exit(exit_code)
