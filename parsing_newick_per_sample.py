import argparse
import pandas as pd
from ete3 import Tree

# Function to subset the TSV file for a specific sample
def subset_tsv(tsv_file, sample_column):
    # Read the TSV file into a pandas DataFrame
    df = pd.read_csv(tsv_file, sep='\t')

    # Keep only the "#OTU" column and the specific sample column
    if sample_column not in df.columns:
        raise ValueError(f"Sample column '{sample_column}' not found in the TSV file.")

    subset_df = df[["OTU_ID", sample_column]]

    # Keep only rows where the sample column has non-zero values
    filtered_df = subset_df[subset_df[sample_column] != 0]

    # Extract the "#OTU" values to a list
    taxa_to_keep = filtered_df["OTU_ID"].tolist()

    return taxa_to_keep

# Function to prune the tree
def prune_tree(nwk_file, taxa_to_keep, output_file):
    # Load the reference tree
    tree = Tree(nwk_file)

    # Prune the tree to keep only the desired taxa
    pruned_tree = tree.copy()
    pruned_tree.prune(taxa_to_keep, preserve_branch_length=True)

    # Save the subsetted tree
    pruned_tree.write(outfile=output_file)

# Main function to loop over all samples
def main(tsv_file, nwk_file, output_dir, metadata_file):
    # Read the metadata file to get the sample columns
    with open(metadata_file, 'r') as f:
        sample_columns = [line.strip() for line in f.readlines()][2:]  # Skip the first two lines

    for sample_column in sample_columns:
        print(f"Processing sample: {sample_column}")

        # Step 1: Subset the TSV file and get the list of taxa
        taxa_to_keep = subset_tsv(tsv_file, sample_column)

        # Step 2: Prune the tree
        output_file = f"{output_dir}/{sample_column}_subset_tree.nwk"
        prune_tree(nwk_file, taxa_to_keep, output_file)

        print(f"Pruned tree saved for sample '{sample_column}' to {output_file}")

# Specify file paths and sample columns

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prune a tree for individual samples.")
    parser.add_argument("--tsv", required=True, help="Path to the feature table TSV file")
    parser.add_argument("--nwk", required=True, help="Path to the reference Newick tree file")
    parser.add_argument("--metadata", required=True, help="Path to the metadata file")
    parser.add_argument("--output", required=True, help="Directory to save pruned trees")

   args = parser.parse_args()

# Run the main function
    main(args.tsv, args.nwk, args.output, args.metadata)
