import pronto
import json
import os
metadata_file =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "card.metadata.obo"
)
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
            metadata[term.id]["phenotype"] = f"{relationship.name.replace('_', ' ')}: {antibiotics}"

# second pass to pull out extra confers resistance from is_a relationships
for id in metadata:
    if "is_a" in metadata[id]:
        is_a_ARO_id = ":".join(metadata[id]["is_a"].split(":")[0:2])
        if "phenotype" in metadata[is_a_ARO_id]:
            if "phenotype" in metadata[id]:
                metadata[id]["additional_phenotype"] = metadata[is_a_ARO_id]["phenotype"]
            else:
                metadata[id]["phenotype"] = metadata[is_a_ARO_id]["phenotype"]
out_path =  os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "db_metadata",
            "card.metadata.json"
)

with open(out_path, "w") as out_file:
    out_file.write(
        json.dumps(metadata, sort_keys=True, indent=2)
    )