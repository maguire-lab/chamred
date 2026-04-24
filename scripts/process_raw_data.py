import os
import pandas as pd
import pronto 
import json
from pronto import relationship
from Bio import SeqIO

from typing import Sequence
import orfipy_core 
import re
from Bio.Seq import Seq




META_DB_PATH="chamredb/data/db_metadata/"
FASTA_DB_PATH="chamredb/data/db_fastas/"

# CARD
def parse_card():
    metadata_file = META_DB_PATH + "card.metadata.obo"
    o = pronto.Ontology(metadata_file)
    metadata = {}
    for term in o.terms():
        metadata[term.id] = {'name': term.name}
        # add is_a superclass
        if len(list(term.superclasses(distance=1, with_self=False))) > 0:
            is_a = ','.join([f"{term.id}:{term.name}" for term in term.superclasses(distance=1, with_self=False)])
            metadata[term.id]['is_a'] = is_a
        # parse relationship
        relationships = term.relationships
        for relationship in relationships:
            if relationship.name.startswith('confers_resistance'):
                antibiotics = ','.join([term.name for term in relationships[relationship]])
                if "phenotype" not in metadata[term.id]:
                    metadata[term.id]["phenotype"] = []
                metadata[term.id]["phenotype"].append(f"{relationship.name.replace('_', ' ')}: {antibiotics}")
    
    # second pass to pull out extra confers resistance from is_a relationships
    for id in metadata:
        if "is_a" in metadata[id]:
            is_a_ARO_id = ":".join(metadata[id]["is_a"].split(":")[0:2])
            if "phenotype" in metadata[is_a_ARO_id]:
                if "phenotype" not in metadata[id]:
                    metadata[id]["phenotype"] = []
                metadata[id]["phenotype"].append(metadata[is_a_ARO_id]["phenotype"])
    out_path = META_DB_PATH + "card.metadata.json"
    
    with open(out_path, "w") as out_file:
        out_file.write(
            json.dumps(metadata, sort_keys=True, indent=2)
        )
    print("## CARD metadata processed") 
    
    in_path = FASTA_DB_PATH + "protein_fasta_protein_homolog_model.fasta"
    
    
    out_path = FASTA_DB_PATH + "card.protein.fasta"
    
    with open(in_path) as in_file, open(out_path, "w") as out_file:
        for record in SeqIO.parse(in_file, "fasta"):
            aro_id, description = (record.id.split("|")[2],record.id.split("|")[3])
            out_file.write(f">{aro_id}\n{str(record.seq)}\n")
    print("## CARD protein processed") 



# NCBI
def parse_ncbi():
    metadata_file =  META_DB_PATH + "ncbi.metadata.tsv"
    
    # %%
    metadata_df = pd.read_csv(metadata_file, sep="\t")
    
    # %%
    metadata_df = metadata_df.query('scope == "core" and subtype !="POINT"' )
    
    metadata_df = metadata_df.sort_values(by=['gene_family', 'allele'])
    
    metadata_df = metadata_df.filter(['allele', 'gene_family', 'subclass', 'refseq_protein_accession', 'refseq_nucleotide_accession'])
    
    # %%
    # combine allele and gene family and drop duplicates
    metadata_df = (metadata_df
        .assign(allele = metadata_df['allele'].combine_first(metadata_df['gene_family']))
        .drop(columns=['gene_family'])
        # .drop_duplicates(subset=['allele'])
    )
    
    # %%
    metadata_deduplicated = metadata_df.drop_duplicates(subset=['allele'])
    
    # %%
    # aggregated metdata
    aggregated_refseq_protein_accessions = (
        metadata_df.groupby(['allele'])['refseq_protein_accession']
        .apply(list)
        .reset_index()
        .rename(columns={"refseq_protein_accession": "aggregated_refseq_protein_accession"})
    )
    duplicated_refseq_protein_accessions =  (
        aggregated_refseq_protein_accessions['aggregated_refseq_protein_accession']
        .apply(lambda x: x[1:])
    )
    
    duplicated_refseq_protein_accessions = (
        aggregated_refseq_protein_accessions
        .assign(duplicated_refseq_protein_accessions = duplicated_refseq_protein_accessions)
        .drop(columns=['aggregated_refseq_protein_accession'])
    )
    # %%
    # aggregated metdata
    aggregated_refseq_nucleotide_accessions = (
        metadata_df
        .groupby(['allele'])['refseq_nucleotide_accession']
        .apply(list)
        .reset_index()
        .rename(columns={"refseq_nucleotide_accession": "aggregated_refseq_nucleotide_accessions"})
    )
    
    duplicated_refseq_nucleotide_accessions =  (
        aggregated_refseq_nucleotide_accessions['aggregated_refseq_nucleotide_accessions']
        .apply(lambda x: x[1:])
    )
    
    duplicated_refseq_nucleotide_accessions = (
        aggregated_refseq_nucleotide_accessions
        .assign(duplicated_refseq_nucleotide_accessions = duplicated_refseq_nucleotide_accessions)
        .drop(columns=['aggregated_refseq_nucleotide_accessions'])
    )
    
    # %%
    # join together dataframes with deduplicated and duplicates
    metadata_deduplicated = (
        metadata_deduplicated
        .join(duplicated_refseq_protein_accessions.set_index('allele'), on='allele')
        .join(duplicated_refseq_nucleotide_accessions.set_index('allele'), on='allele')
    )
    
    # %%
    metadata = {}
    for _, row in metadata_deduplicated.iterrows():
        id = row['refseq_protein_accession']
        metadata[id] = {
            'name': row['allele'],
            'alternative_id': {
                'nucleotide_accession': row['refseq_nucleotide_accession']
            },
            'duplicate_allele_ids': {
                'protein_accessions': row['duplicated_refseq_protein_accessions'],
                'nucleotide_accessions': row['duplicated_refseq_nucleotide_accessions']
            },
            'phenotype': f"confers resistance to subclass {row['subclass']}"
        }
    
    out_path = META_DB_PATH + "ncbi.metadata.json"
    
    with open(out_path, "w") as out_file:
        out_file.write(
            json.dumps(metadata, sort_keys=True, indent=2)
        )
    print("## NCBI Metadata Parsed")

    metadata_file = META_DB_PATH + "ncbi.metadata.tsv"
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

    
    in_path = FASTA_DB_PATH + "ncbi.protein.raw.fasta"
    out_path = FASTA_DB_PATH + "ncbi.protein.fasta"
    with open(in_path) as in_file, open(out_path, "w") as out_file:
        accessions_added = []
        for record in SeqIO.parse(in_file, "fasta"):
    
            accession, allele = (record.id.split("|")[1],record.id.split("|")[4])
            if accession in deduplicated_accessions and accession not in accessions_added:
                accessions_added.append(accession)
                out_file.write(f">{accession}\n{str(record.seq)}\n")
    print("## NCBI Fasta Parsed")

def parse_resfinder():
    # ResFinder
    in_file = open(FASTA_DB_PATH + 'resfinder.nucl.fasta')
    out_file = open(FASTA_DB_PATH + 'resfinder.protein.fasta', 'w')
    genes_added = []
    for record in SeqIO.parse(in_file, "fasta"):
        id = record.id.split("_")[0]
        if id in genes_added:
            continue
        genes_added.append(id)
        sequence = str(record.seq)
        max_length = 0
        orf_start = None
        orf_end = None
        orf_description = None
        orf_frame = None
        # find best ORF
        for start,stop,strand,description in orfipy_core.orfs(sequence, partial3 = True):
            if stop - start > max_length:
                max_length = stop - start
                orf_start = start
                orf_end = stop
                orf_frame = int(re.search('ORF_frame=([-\d]+)', description).group(1))
        if (orf_frame < 1):
            protein_sequence = record.seq[orf_start:orf_end].reverse_complement().translate()
        else:
            protein_sequence = record.seq[orf_start:orf_end].translate()
    
        out_file.write(f">{id}\n{protein_sequence}\n")
    
    
    metadata_file = META_DB_PATH + "resfinder.metadata.tsv"
    
    
    metadata_df = pd.read_csv(metadata_file, sep = "\t")
    metadata_df = metadata_df[['Gene_accession no.', 'Phenotype']]
    
    metadata = {}
    for _, row in metadata_df.iterrows():
        name = row['Gene_accession no.'].split("_")[0]
        metadata[name] = {
            'name': name,
            'phenotype': [f"confers resistance to {row['Phenotype']}"]
        }
    
    out_path =  META_DB_PATH + "resfinder.metadata.json"
    
    
    with open(out_path, "w") as out_file:
        out_file.write(
            json.dumps(metadata, sort_keys=True, indent=2)
        )

if __name__ == '__main__':

    parse_card()
    parse_ncbi()
    parse_resfinder()
