# %%
import pandas as pd
import collections
# %%
resfinder_vs_card_rbhs = list(pd.read_csv("../results/mmseqs_resfinder_vs_card.rbh.sorted.tsv", sep="\t")['query'])
print([item for item, count in collections.Counter(resfinder_vs_card_rbhs).items() if count > 1])
# %%
# get matches from search that do not have rbhs and name them non-rbhs 
headers = ['query', 'target', 'fident', 'alnlen', 'mismatch', 'gapopen', 'qstart', 'qend', 'tstart', 'tend', 'evalue', 'bits']

resfinder_vs_card_non_rbh_results = (
    pd.read_csv("../results/resfinder_vs_card.search.m8.tsv", sep="\t", names=headers)
    .query("query != @resfinder_vs_card_rbhs")
    .sort_values(by=['query'], key=lambda col: col.str.lower())
)

# %%

print(f'Number of RBHs: {len(set(resfinder_vs_card_rbhs))}')

# %%
resfinder_vs_card_non_rbhs = list(set(resfinder_vs_card_non_rbh_results['query']))
print(f'Number of non-RBHs: {len(set(resfinder_vs_card_non_rbhs))}')

# %%
resfinder_vs_card_non_rbh_results.to_csv(
    "../results/resfinder_vs_card.search.filtered.tsv",
    sep="\t",
    index=False
)