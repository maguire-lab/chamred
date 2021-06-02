import os
import pandas as pd
from Bio import SeqIO

metadata_file =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "ncbi.metadata.tsv"
)

metadata = pd.read_csv(metadata_file, sep="\t")


metadata = metadata.query('scope == "core" and type == "AMR" and subtype =="AMR"' )

metadata = metadata.sort_values(by=['gene_family', 'allele'])

metadata = metadata.filter(['allele', 'gene_family', 'refseq_protein_accession'])

# combine allele and gene family and drop duplicates
metadata = (metadata
    .assign(allele = metadata['allele'].combine_first(metadata['gene_family']))
    .drop(columns=['gene_family'])
    .drop_duplicates(subset=['allele'])
)


deduplicated_accessions = list(metadata['refseq_protein_accession'])

in_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_fastas",
            "ncbi.protein.raw.fasta"
)

out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_fastas",
            "ncbi.protein.fasta"
)


with open(in_path) as in_file, open(out_path, "w") as out_file:
    accessions_added = []
    for record in SeqIO.parse(in_file, "fasta"):

        accession, allele = (record.id.split("|")[1],record.id.split("|")[4])
        if accession in deduplicated_accessions and accession not in accessions_added:
            accessions_added.append(accession)
            out_file.write(f">{accession}\n{str(record.seq)}\n")


