import json
def parse_id_file(id_file):
    with open(id_file) as fh:
        ids = fh.read().splitlines()
    return(ids)


def parse_hamronization_json_file(hamronization_json_file):
    ids_and_dbs = []
    with open(hamronization_json_file) as json_file:
        results = json.load(json_file)
        for result in results:
            database, id = extract_database_and_id(result)
            ids_and_dbs.append(
                {
                    'file': result['input_file_name'],
                    'id': id,
                    'database': database
                }
            )
    return(ids_and_dbs)

def extract_database_and_id(result):
    software = result['analysis_software_name']
    if software == 'abricate':
        database = result['reference_database_id']
        id = result['gene_symbol']
    elif software == 'amrfinderplus':
        database = 'ncbi'
        id = result['reference_accession']
    elif software == 'ariba':
        if result['reference_database_id'] == 'card':
            database = 'card'
            id = f'ARO:{result["gene_name"].split(".")[1]}'
        elif result['reference_database_id'] == 'ncbi':
            database = 'ncbi'
            id = ".".join(result["reference_accession"].split(".")[1:])
    elif software == 'resfinder 4':
        database = 'resfinder'
        id = result['gene_symbol']
    elif software == 'rgi':
        database = 'card'
        id = f'ARO:{result["reference_accession"]}'
    return(database,id)