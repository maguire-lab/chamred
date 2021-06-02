import pandas as pd
import json
import os

metadata_file =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "ncbi.metadata.tsv"
)

metadata_df = pd.read_csv(metadata_file, sep="\t")


metadata_df = metadata_df.query('scope == "core" and type == "AMR" and subtype =="AMR"' )

metadata_df = metadata_df.sort_values(by=['gene_family', 'allele'])

metadata_df = metadata_df.filter(['allele', 'gene_family', 'subclass', 'refseq_protein_accession'])

# combine allele and gene family and drop duplicates
metadata_df = (metadata_df
    .assign(allele = metadata_df['allele'].combine_first(metadata_df['gene_family']))
    .drop(columns=['gene_family'])
    .drop_duplicates(subset=['allele'])
)

metadata = {}
for _, row in metadata_df.iterrows():
    id = row['refseq_protein_accession']
    name = row['allele']
    metadata[id] = {
        'name': name,
        'subclass': row['subclass']
    }

out_path =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "ncbi.metadata.json"
)

with open(out_path, "w") as out_file:
    out_file.write(
        json.dumps(metadata, sort_keys=True, indent=2)
    )