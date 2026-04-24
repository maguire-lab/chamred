#!/bin/bash
set -euo pipefail
#wget https://github.com/arpcard/aro/raw/master/src/ontology/aro.obo -O chamredb/data/db_metadata/card.metadata.obo
#wget https://card.mcmaster.ca/latest/data -O card_update.tar.gz
#tar -xvf card_update.tar.gz -C chamredb/data/db_fastas ./protein_fasta_protein_homolog_model.fasta 
#tar -xvf card_update.tar.gz -C chamredb/data/db_fastas ./nucleotide_fasta_protein_homolog_model.fasta 
#rm -rf card_update.tar.gz
#
#wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/ReferenceGeneCatalog.txt -O chamredb/data/db_metadata/ncbi.metadata.tsv
#wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/AMRProt.fa -O chamredb/data/db_fastas/ncbi.protein.raw.fasta
#wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/AMR_CDS.fa -O chamredb/data/db_fastas/ncbi.nucl.raw.fasta
#
#wget https://bitbucket.org/genomicepidemiology/resfinder_db/raw/master/phenotypes.txt -O chamredb/data/db_metadata/resfinder.metadata.tsv
#git clone https://bitbucket.org/genomicepidemiology/resfinder_db
#cat resfinder_db/*.fsa > chamredb/data/db_fastas/resfinder.nucl.fasta
#rm -rf resfinder_db

## Data Parsing
python scripts/process_raw_data.py 

#bash find_rbhs_and_search_matches.sh
#
#python chamredb/build_graph_from_mmseqs_data.py
