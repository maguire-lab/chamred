# find rbhs
# resfinder
mmseqs easy-rbh db_fastas/resfinder.protein.fasta  db_fastas/card.protein.fasta  results/mmseqs_resfinder_vs_card.rbh.tsv tmp -s 7.5

mmseqs easy-rbh db_fastas/resfinder.protein.fasta  db_fastas/ncbi.protein.fasta  results/mmseqs_resfinder_vs_ncbi.rbh.tsv tmp -s 7.5

# ncbi
mmseqs easy-rbh db_fastas/ncbi.protein.fasta  db_fastas/card.protein.fasta  results/mmseqs_ncbi_vs_card.rbh.tsv tmp -s 7.5

mmseqs easy-rbh db_fastas/ncbi.protein.fasta  db_fastas/resfinder.protein.fasta  results/mmseqs_ncbi_vs_resfinder.rbh.tsv tmp -s 7.5

# card
mmseqs easy-rbh db_fastas/card.protein.fasta  db_fastas/resfinder.protein.fasta  results/mmseqs_card_vs_resfinder.rbh.tsv tmp -s 7.5

mmseqs easy-rbh db_fastas/card.protein.fasta  db_fastas/ncbi.protein.fasta  results/mmseqs_card_vs_ncbi.rbh.tsv tmp -s 7.5


# create mmseqs search DBs
mmseqs createdb db_fastas/resfinder.protein.fasta mmseqs_DBs/resfinder.protein
mmseqs createindex mmseqs_DBs/resfinder.protein tmp

mmseqs createdb db_fastas/ncbi.protein.fasta mmseqs_DBs/ncbi.protein
mmseqs createindex mmseqs_DBs/ncbi.protein tmp

mmseqs createdb db_fastas/card.protein.fasta mmseqs_DBs/card.protein
mmseqs createindex mmseqs_DBs/card.protein tmp

# perform search
# resfinder
mmseqs search mmseqs_DBs/resfinder.protein mmseqs_DBs/card.protein mmseqs_search_DBs/resfinder_vs_card_search tmp -s 7.0 --max-accept 3

mmseqs search mmseqs_DBs/resfinder.protein mmseqs_DBs/ncbi.protein mmseqs_search_DBs/resfinder_vs_ncbi_search tmp -s 7.0 --max-accept 3

# ncbi
mmseqs search mmseqs_DBs/ncbi.protein mmseqs_DBs/card.protein mmseqs_search_DBs/ncbi_vs_card_search tmp -s 7.0 --max-accept 3

mmseqs search mmseqs_DBs/ncbi.protein mmseqs_DBs/resfinder.protein mmseqs_search_DBs/ncbi_vs_resfinder_search tmp -s 7.0 --max-accept 3

# card
mmseqs search mmseqs_DBs/card.protein mmseqs_DBs/ncbi.protein mmseqs_search_DBs/card_vs_ncbi_search tmp -s 7.0 --max-accept 3

mmseqs search mmseqs_DBs/card.protein mmseqs_DBs/resfinder.protein mmseqs_search_DBs/card_vs_resfinder_search tmp -s 7.0 --max-accept 3

# make alignment files
# resfinder
mmseqs convertalis  mmseqs_DBs/resfinder.protein mmseqs_DBs/card.protein mmseqs_search_DBs/resfinder_vs_card_search results/mmseqs_resfinder_vs_card.search.tsv

mmseqs convertalis  mmseqs_DBs/resfinder.protein mmseqs_DBs/ncbi.protein mmseqs_search_DBs/resfinder_vs_ncbi_search results/mmseqs_resfinder_vs_ncbi.search.tsv

# ncbi
mmseqs convertalis  mmseqs_DBs/ncbi.protein mmseqs_DBs/card.protein mmseqs_search_DBs/ncbi_vs_card_search results/mmseqs_ncbi_vs_card.search.tsv

mmseqs convertalis  mmseqs_DBs/ncbi.protein mmseqs_DBs/resfinder.protein mmseqs_search_DBs/ncbi_vs_resfinder_search results/mmseqs_ncbi_vs_resfinder.search.tsv

# card
mmseqs convertalis  mmseqs_DBs/card.protein mmseqs_DBs/resfinder.protein mmseqs_search_DBs/card_vs_resfinder_search results/mmseqs_card_vs_resfinder.search.tsv

mmseqs convertalis  mmseqs_DBs/card.protein mmseqs_DBs/ncbi.protein mmseqs_search_DBs/card_vs_ncbi_search results/mmseqs_card_vs_ncbi.search.tsv