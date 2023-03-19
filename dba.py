import os.path

import dataset

DBNAME = "mjdata.db"

def connect() -> dataset:
    path = os.path.dirname(os.path.realpath(__file__))
    return dataset.connect(f"sqlite:///{os.path.join(path, DBNAME)}")

def fetch_phrases() -> list:
    list = []
    for row in connect()['info']:
        list.append(row['phrase'])

    return list