#!/usr/bin/env python3
import re
import argparse
from pyteomics import mzml
import csv

def convert_scan_indices(tab_file_path, mzml_file_path, output_file_path):
    """
    Convert MS2 scan indices to absolute scan indices (including MS1 scans)
    Parameters:
    -----------
    tab_file_path: str
        Path to the tab-delimited file with MS2 scan indices
    mzml_file_path: str
        Path to the mzML file
    output_file_path: str
        Path to write the output tab-delimited file with corrected indices
    """
    print(f"Processing mzML file: {mzml_file_path}")
    # Build a mapping of MS2 scan positions
    ms2_positions = []
    absolute_index = 0
    with mzml.read(mzml_file_path) as reader:
        for spectrum in reader:
            ms_level = spectrum.get('ms level')
            if ms_level == 2:
                ms2_positions.append(absolute_index)
            absolute_index += 1
    print(f"Found {len(ms2_positions)} MS2 scans among {absolute_index} total scans")

    # Now process the tab-delimited file
    print(f"Processing tab file: {tab_file_path}")
    output_rows = []
    with open(tab_file_path, 'r') as tab_file:
        reader = csv.reader(tab_file, delimiter='\t')
        header = next(reader)
        output_rows.append(header)

        for row in reader:

            if row and row[3].startswith('['):
                continue

            # Extract scan index from the "scan" field - now just expecting a number
            scan_field = row[1]

            # Try to extract the scan number directly
            if scan_field.isdigit():
                ms2_idx = int(scan_field)
            else:
                # Still support "scan=X" format as fallback
                scan_match = re.match(r'scan=(\d+)', scan_field)
                if scan_match:
                    ms2_idx = int(scan_match.group(1))
                else:
                    print(f"Warning: Could not extract scan number from '{scan_field}'")
                    output_rows.append(row)  # Keep original row
                    continue

            # Get the true MS2 index using the formula
            adjusted_ms2_idx = int(ms2_idx / 3)

            # Check if the index is valid
            if 0 <= adjusted_ms2_idx < len(ms2_positions):
                # Get the absolute position of this MS2 scan
                absolute_idx = ms2_positions[adjusted_ms2_idx]
                # Replace the scan field with index=# format
                row[1] = f"index={absolute_idx}"
            else:
                print(f"Warning: Invalid MS2 index {ms2_idx} (adjusted to {adjusted_ms2_idx})")
                print(f"Valid range is 0-{len(ms2_positions)-1}")

            output_rows.append(row)

    # Write output file
    print(f"Writing output to: {output_file_path}")
    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter='\t')
        writer.writerows(output_rows)
    print(f"Conversion complete. Processed {len(output_rows)-1} entries.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert MS2 scan indices to absolute scan indices')
    parser.add_argument('tab_file', help='Path to the tab-delimited file')
    parser.add_argument('mzml_file', help='Path to the mzML file')
    parser.add_argument('output_file', help='Path to write the output file')

    args = parser.parse_args()
    convert_scan_indices(args.tab_file, args.mzml_file, args.output_file)
