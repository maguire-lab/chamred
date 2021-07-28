# CharmeDb 
![CharmeDb](docs/images/CharmeDb.png)  
(pronounced 'charmed' `/tʃɑː(r)md/`)
  


Previously known as Project ![mAMRite](docs/images/mAMRite_small.png)  

(Abandoned for obvious trademark issues and the fact that the joke may be lost on non-Brits)  

## Introduction
This project originated from the dilema a scientist faces when choosing a database that stores antimicrobial resistance determinants. Multiple databases exist with comparative strengths and weaknesses. This project builds on the concepts of the [haAMRonization](https://github.com/pha4ge/hAMRonization) project aiming to aggeregate and combine the information contained within the metadata associated with each project. The problem is exacerbated by the fact that the equivalent antimicrobial resistance genes (ARGs) can be named differently in each database.

The hypothesis for the project is as follows:  
 * given a match in one database
 * find the matches in other databases
 * aggregate the combined desriptive information pertaining to antimicrobial resistance contained in the union of the metadata
 * report this to user for them to make intelligent informed choices

## Methodology
 * Download sequences and associated metadata of ARGs from 3 databases
   * [CARD](https://card.mcmaster.ca/) ([Manuscript](http://www.ncbi.nlm.nih.gov/pubmed/31665441))
   * [NCBI AMR Reference Gene Catalog](https://www.ncbi.nlm.nih.gov/pathogens/refgene/) 
   * [Resfinder 4](https://bitbucket.org/genomicepidemiology/resfinder/src/4.0/) ([Manuscipt](https://academic.oup.com/jac/article/75/12/3491/5890997))  
   Details can be found in the [appendices](/docs/appendices.md#data-download)
 * Parse the data to
   * extract the protein sequences and write into fasta format with the gene identifiers as the record ids.
   * extract the associated metadata and convert to a consistent `JSON` format  
   Details can be found in the [appendices](/docs/appendices.md#data-parsing)
 * Find best matches of each gene from one source database against the other two target databases
   * Where a reciprocal best hit (RBH) exists, report this.  
     Details can be found in the [appendices](/docs/appendices.md#analyse-for-reciprocal-best-hits-rbhs).  
     A summary of the results can be found [here](/docs/appendices.md#summary-of-rbh-analysis)
   * If a RBH does not exist, report the best match as long as thresholds for coverage and indentity are met.   
    A summary of the results can be found [here](/docs/appendices.md#summary-of-non-rbh-searches)
  
  For this purpose the [MMseqs2](https://pubmed.ncbi.nlm.nih.gov/29035372/) search tool was used that in its most sensitive mode is 100x faster than blastp and almost as sensitive. In a [comparative manuscript](https://pubmed.ncbi.nlm.nih.gov/33099302/) demonstrated that even in the worst cases mmseqs would not miss more than 10% of the RBH produced by blastp. MMseqs2 also contains a convenient wrapper to perform the all-by-all search necessary to find RBHs.
* From the outputs of the MMseqs2 searches the RBHs or best matches of each gene from one database against the other two databases can be parsed to produce a `Directed Graph`. This netowrk was constructed using the [networkx](https://networkx.org/) python package.  
  Details of the method can be found [here](docs/appendices.md#building-a-networkx-graph)  
  In this graph 
  * the nodes represent a protein from one database
    * Node attributes contain the phenotype from the JSON metadata
  * the edges link nodes and represent the matches and attributes include
    * type either RBH or OWH (one way hit)
    * coverage (alignment length/query length)
    * identity (percent identity of match)  
  See the image below for a pictoral example using made up data  
  ![network diagram](docs/images/chamredb_network.png) 


## Querying the graph
The graph can be queried in one of 3 ways  
1) Querying an individual gene by specifying the identifier `-i` and database `-d`
    ```
    chamredb query -d ncbi -i WP_012695489.1 
    ```
    Alternatively the gene name can be used
    ```
    chamredb query -d ncbi -i qnrB2
    ```
    The output reports the matches and metadata from the other databases  
    ![qnrB2](/docs/images/qnrB2.png)

    Another example where the matches are one way hits not RBHs
    ```
    chamredb query -d resfinder -i "aac(3)-IIIb"
    ```
    ![aac(3)-IIIb](/docs/images/aac(3)-IIIb.png)
    In these outputs ↔ means a RBH, and ➡ a search hit

2) Providing a list of identifiers from a single database `-d` in a text file `-f` and specifying a path for the tsv output file 
    ```
    chamredb query -d card -f docs/data/card_ids.txt  -o docs/data/card_ids.tsv
    ```
    This will produce a [TSV file](/docs/data/card_ids.tsv) containing the matches and associated metadata with one row per id in the text file
3) Use the [hAMRonization softare](https://github.com/pha4ge/hAMRonization) to convert the outputs from an antimicrobial resistance gene detection tools into a unified format. Concatenate and summarize AMR detection reports into a single summary JSON file using the `hamronize summarize` command from this package. The JSON output from this step can be used to query ChamreDb.  
**Please Note** only outputs using data derived from AMR detection tools that have searched either the `CARD`, `NCBI` or `Resfinder 4 ` databases can be used.
    ```
    chamredb query -j docs/data/hamronize_summary.json -o docs/data/hamronize_summary.tsv
    ```
    This will produce a [TSV file](/docs/data/hamronize_summary.tsv) containing the matches and associated metadata with one row per id in the text file
