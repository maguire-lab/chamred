import pronto
import json
import os
import re

from pronto import relationship
metadata_file =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "chamredb", "data", "db_metadata",
            "card.metadata.obo"
)
o = pronto.Ontology(metadata_file)

metadata = {}
for term in o.terms():
    #print(term)
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
    # add publication metadata
    if len(list(term.definition.xrefs)) > 0:
        metadata[term.id]["PMID"] = []
        for item in term.definition.xrefs:
            metadata[term.id]["PMID"].append(item.id.replace("PMID:", ""))

# second pass to pull out extra confers resistance from is_a relationships
for id in metadata:
    #print(metadata[id])
    if "is_a" in metadata[id]:
        is_a_ARO_id = ":".join(metadata[id]["is_a"].split(":")[0:2])
        if "phenotype" in metadata[is_a_ARO_id]:
            if "phenotype" not in metadata[id]:
                metadata[id]["phenotype"] = []
            metadata[id]["phenotype"].append(metadata[is_a_ARO_id]["phenotype"])

out_path =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "chamredb", "data", "db_metadata",
            "card.metadata.json"
)

with open(out_path, "w") as out_file:
    out_file.write(
        json.dumps(metadata, sort_keys=True, indent=2)
    )