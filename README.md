# project mAMRite
![mAMRite](images/mAMRite.png)

## Download data

### CARD
#### Metadata
ARO ontology
```
wget https://github.com/arpcard/aro/raw/master/src/ontology/aro.obo -O db_metadata/card.obo
```
#### Sequence data
##### Protein
```
wget https://card.mcmaster.ca/latest/data
tar -xvf data ./protein_fasta_protein_homolog_model.fasta
mv protein_fasta_protein_homolog_model.fasta db_fastas/card.protein.fasta
```

##### Nucleotide
```
tar -xvf data ./nucleotide_fasta_protein_homolog_model.fasta
mv nucleotide_fasta_protein_homolog_model.fasta db_fastas/card.nucl.fasta
```

### NCBI

#### Metadata
```
wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/ReferenceGeneCatalog.txt -O db_metadata/ncbi.metadata.tsv
```

#### Sequence data
##### Protein
```
wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/AMRProt -O db_fastas/ncbi.protein.raw.fasta
```
Nucleotide sequences
```
wget https://ftp.ncbi.nlm.nih.gov/pathogen/Antimicrobial_resistance/AMRFinderPlus/database/latest/AMR_CDS -O db_fastas/ncbi.nucl.raw.fasta
```

### Resfinder

#### Metadata
```
wget https://bitbucket.org/genomicepidemiology/resfinder_db/src/master/phenotypes.txt -O db_metadata/resfinder.metadata.txt
```

#### Sequences
```
git clone https://bitbucket.org/genomicepidemiology/resfinder_db
cat resfinder_db/*.fsa > db_fastas/resfinder.nucl.fasta
```

## Parse data
### NCBI
Only include those in the core AMT/AMR (acquired) set and remove duplicates with  the script [parse_ncbi_proteins.py](scripts/parse_ncbi_proteins.py)

This produced the output file [ncbi.protein.fasta](db_fastas/ncbi.protein.fasta) with 4542 protein sequences

### Resfinder
Found best ORF from nucleotide and removed duplicated gene/alleles with the script
[resfinder_orfs_to_proteins.py](scripts/resfinder_orfs_to_proteins.py)

This produced the output file [resfinder.protein.fasta](db_fastas/resfinder.protein.fasta) with 2543 protein sequences

## Analyse for Reciprocal Best Hits (RBHs)
Used the [MMseqs2](https://github.com/soedinglab/MMseqs2) software that allows very fast protein clustering - see this [publication](https://www.nature.com/articles/s41467-018-04964-5)
Performance characteristics in this [comparison publication](https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-020-07132-6)

Commands run were
1. run resfinder with MMseqs2 easy-rbh analysis to produce [mmseqs_resfinder_vs_card.rbh.tsv](results/mmseqs_resfinder_vs_card.rbh.tsv)
    ```
    mmseqs easy-rbh db_fastas/resfinder.protein.fasta  db_fastas/card.protein.fasta  results/mmseqs_resfinder_vs_card.rbh.tsv tmp -s 7.5
    ```
    Sorted the outputs with [sort_mmseqs_output.py](scripts/sort_mmseqs_output.py) to produce the output [mmseqs_resfinder_vs_card.rbh.sorted.tsv](results/mmseqs_resfinder_vs_card.rbh.sorted.tsv)
2. run NCBI with MMseqs2 easy-rbh analysis to produce [mmseqs_ncbi_vs_card.rbh.tsv](results/mmseqs_ncbi_vs_card.rbh.tsv)
    ```
    mmseqs easy-rbh db_fastas/ncbi.protein.fasta  db_fastas/card.protein.fasta  results/mmseqs_ncbi_vs_card.rbh.tsv tmp -s 7.5
    ```
    Sorted the outputs with [sort_mmseqs_output.py](scripts/sort_mmseqs_output.py) to produce the output [mmseqs_ncbi_vs_card.rbh.sorted.tsv](results/mmseqs_ncbi_vs_card.rbh.sorted.tsv)

### Summary of RBH analysis

| Comparison | Number of proteins |Number of RBH |
| ----| ---- | ----- |
| Resfinder vs Card |  2543 (Resfinder)<br>2979 (CARD) | 2159 (84.9% of Resfinder proteins) |
| NCBI vs Card |  4542 (Resfinder)<br>2979 (CARD) | 2690 (59.2% of NCBI proteins) |

