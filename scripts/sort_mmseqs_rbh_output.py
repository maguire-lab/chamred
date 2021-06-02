# %%
import pandas as pd
import os
# %%
unsorted_file = "../results/mmseqs_resfinder_vs_card.rbh.tsv"
sorted_file = os.path.join(os.path.dirname(unsorted_file), f'{os.path.splitext(os.path.basename(unsorted_file))[0]}.sorted.tsv')
# %%
headers = ['query', 'target', 'fident', 'alnlen', 'mismatch', 'gapopen', 'qstart', 'qend', 'tstart', 'tend', 'evalue', 'bits']
df = pd.read_csv(unsorted_file, sep="\t", names = headers)
# %%
df = df.assign(query=lambda df: df['query'].str.split("_").str[0])
# %%
# sort by query and get best match using fident and alnlen
df = (df
    .sort_values(
        by=['query', 'fident', 'alnlen'],
        ascending=[True, False, False]
    )
)
# remove duplicates
df = df.drop_duplicates(subset=['query'])
# now resort based on query
df = (df
    .sort_values(
        by=['query'],
        key = lambda x: x.str.lower()
    )
)
# %%
df.to_csv(sorted_file, index=False, sep="\t")
# %%
