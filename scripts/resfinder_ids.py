from Bio import SeqIO

with open("/data/mAMRite/dbs/resfinder.fasta") as in_file, open("/data/mAMRite/resfinder.ids.txt", "w") as out_file:
    for record in SeqIO.parse(in_file, "fasta"):
        out_file.write(f'{record.id}\n')