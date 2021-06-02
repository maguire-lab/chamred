import os
from Bio import SeqIO
from pronto.relationship import Relationship

in_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "card_db",
            "protein_fasta_protein_homolog_model.fasta"
)

out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_fastas",
            "card.protein.fasta"
)

with open(in_path) as in_file, open(out_path, "w") as out_file:
    for record in SeqIO.parse(in_file, "fasta"):

        aro_id, description = (record.id.split("|")[2],record.id.split("|")[3])
        out_file.write(f">{aro_id}\n{str(record.seq)}\n")


