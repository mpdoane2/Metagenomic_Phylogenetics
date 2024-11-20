/home/doan0033/data/database/WoL_database/taxonomy/ranks.tsv

import argparse
import pandas as pd

# Function to subset the TSV file for all OTU_IDs
def subset_tsv(tsv_file):
    # Read the TSV file into a pandas DataFrame
    df = pd.read_csv(tsv_file, sep='\t')

    # Check if the "OTU_ID" column exists
    if 'OTU_ID' not in df.columns:
        raise ValueError("The 'OTU_ID' column is not found in the TSV file.")

    # Extract all OTU_ID values to a list
    taxa_to_keep = df['OTU_ID'].tolist()

    return taxa_to_keep

# Function to filter the ranks.tsv file by matching OTU IDs
def filter_ranks_by_otu(ranks_file, otu_ids):
    # Read the ranks.tsv file into a pandas DataFrame
    ranks_df = pd.read_csv(ranks_file, sep='\t')

    # Check if the first column exists and extract it (assumed it's unnamed or has a header)
    if ranks_df.columns[0] not in ranks_df.columns:
        raise ValueError(f"The first column in {ranks_file} does not exist or is not named correctly.")
    
    # Filter rows that match OTU IDs
    filtered_ranks_df = ranks_df[ranks_df[ranks_df.columns[0]].isin(otu_ids)]

    return filtered_ranks_df

# Main function to process the datasets and match OTU IDs
def main(tsv_file, ranks_file, output_file):
    # Step 1: Get the OTU IDs from the feature table TSV file
    otu_ids = subset_tsv(tsv_file)

    # Step 2: Filter the ranks.tsv file by matching OTU IDs
    filtered_ranks_df = filter_ranks_by_otu(ranks_file, otu_ids)

    # Step 3: Save the filtered ranks dataframe to a new file
    filtered_ranks_df.to_csv(output_file, sep='\t', index=False)

    print(f"Filtered ranks saved to {output_file}")

# Command-line argument parsing
if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Filter ranks.tsv by OTU IDs from a feature table TSV.")

    # Add arguments for input and output files
    parser.add_argument("--tsv", required=True, help="Path to the feature table TSV file")
    parser.add_argument("--ranks", required=True, help="Path to the ranks.tsv file")
    parser.add_argument("--output", required=True, help="Path to save the filtered ranks.tsv file")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Run the main function with parsed arguments
    main(args.tsv, args.ranks, args.output)

