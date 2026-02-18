import gzip
import pandas as pd


def convert_annot_to_csv(input_file, output_file):
    """
    Convert a gzipped annotation file (.annot.gz) to CSV format.
    
    Args:
        input_file (str): Path to the input .annot.gz file
        output_file (str): Path to the output CSV file
    
    Returns:
        pd.DataFrame: The converted DataFrame
    """
    # Find where the actual data table starts
    with gzip.open(input_file, 'rt') as f:
        lines = f.readlines()
        
        # Find the line with !platform_table_begin
        data_start_idx = None
        
        for i, line in enumerate(lines):
            if line.strip() == '!platform_table_begin':
                data_start_idx = i + 1  # Header is on the next line
                break

    # Read the data starting from the header
    with gzip.open(input_file, 'rt') as f:
        all_lines = f.readlines()
        
        # Get header (line right after !platform_table_begin)
        header_line = all_lines[data_start_idx].strip()
        headers = [h.strip() for h in header_line.split('\t')]
        
        print(f"Found {len(headers)} columns")
        print(f"First few headers: {headers[:5]}")
        
        # Read data rows (start after the header line)
        data_rows = []
        for line in all_lines[data_start_idx + 1:]:
            line = line.strip()
            if line and not line.startswith('!'):  # Skip metadata lines
                row = line.split('\t')
                # Ensure row has same number of columns as headers
                if len(row) == len(headers):
                    data_rows.append(row)
                elif len(row) > 0:  # Some rows might have different lengths
                    # Pad or truncate to match header length
                    if len(row) < len(headers):
                        row.extend([''] * (len(headers) - len(row)))
                    else:
                        row = row[:len(headers)]
                    data_rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(data_rows, columns=headers)

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"\nSuccessfully converted {input_file} to {output_file}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns[:5])}...")  # Show first 5 columns
    
    return df


if __name__ == "__main__":
    # Default values for running as standalone script
    input_file = 'data/00-raw/GPL570.annot.gz'
    output_file = 'data/00-raw/GPL570_annot.csv'
    convert_annot_to_csv(input_file, output_file)
