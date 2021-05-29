# %%
import pandas as pd
from Bio import SeqIO
# %%
metadata = pd.read_csv("../db_metadata/ncbi.metadata.tsv", sep="\t")

# %%
metadata = metadata.query('scope == "core" and type == "AMR" and subtype =="AMR"' )
# %%
metadata = metadata.sort_values(by=['gene_family', 'allele'])
# %%
metadata = metadata.filter(['allele', 'gene_family', 'refseq_protein_accession'])
# %%
# combine allele and gene family and drop duplicates
metadata = (metadata
    .assign(allele = metadata['allele'].combine_first(metadata['gene_family']))
    .drop(columns=['gene_family'])
    .drop_duplicates(subset=['allele'])
)

# %%
deduplicated_accessions = list(metadata['refseq_protein_accession'])
# %%
with open("/data/mAMRite/db_fastas/ncbi.protein.raw.fasta") as in_file, open("/data/mAMRite/db_fastas/ncbi.protein.fasta", "w") as out_file:
    accessions_added = []
    for record in SeqIO.parse(in_file, "fasta"):

        accession, allele = (record.id.split("|")[1],record.id.split("|")[4])
        if accession in deduplicated_accessions and accession not in accessions_added:
            accessions_added.append(accession)
            out_file.write(f">{allele}\n{str(record.seq)}\n")

# %%
