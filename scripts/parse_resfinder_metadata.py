import pandas as pd
import os
import json
metadata_file =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "resfinder.metadata.tsv"
)

metadata_df = pd.read_csv(metadata_file, sep = "\t")
metadata_df = metadata_df[['Gene_accession no.', 'Phenotype']]

metadata = {}
for _, row in metadata_df.iterrows():
    name = row['Gene_accession no.'].split("_")[0]
    metadata[name] = {
        'name': name,
        'phenotype': row['Phenotype']
    }

out_path =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "resfinder.metadata.json"
)

with open(out_path, "w") as out_file:
    out_file.write(
        json.dumps(metadata, sort_keys=True, indent=2)
    )