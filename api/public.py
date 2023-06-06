import json
import os

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

from pyiron_base import Project
from workflow.Simulation import ComsolSimulation
import pandas as pd

KnowNow_URL = "https://git.tu-berlin.de/felipebaca/know-now/-/raw/main/KnowNow_V8_ttl.owl"
g = Graph() # create an empty graph
g.parse(KnowNow_URL, format = "ttl") # load the ontology

def query_sparql(sparql: str) :
    results = g.query(prepareQuery(sparql))
    headers = [str(var) for var in results.vars]
    rows = [[str(val) for val in row] for row in results]
    return json.dumps([dict(zip(headers, row)) for row in rows])

def upload_file_to_server(save_to, file):

    status = 'No file uploaded'
    try:
        save_directory = os.path.join("/home/knownow/KnowNow/", save_to)
        file_path = os.path.join(save_directory, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        status = "file uploaded success"
    except:
        status = "file uploaded faild"

    return status

def get_objects():
    pr = Project(path="ComsolSim_Workflow")
    pr.remove_jobs(recursive=True, silently=True)
    job = pr.create_job(job_type=ComsolSimulation, job_name="ComsolSim")
    options = job.get_objects().to_json(orient='records')

    return options