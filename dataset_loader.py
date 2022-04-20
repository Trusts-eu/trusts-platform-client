import json
import os
import requests

from uuid import uuid4

from dotenv import load_dotenv


load_dotenv()

URL_CREATE_DATASET = os.path.join(
    os.getenv("CKAN_URL", "http://localhost:5000/"),
    "api/3/action/package_create")
URL_CREATE_RESOURCE = os.path.join(
    os.getenv("CKAN_URL", "http://localhost:5000/"),
    "api/3/action/resource_create")


def main(fpath):
    with open(fpath) as f:
        dataset = json.load(f)
    dataset['name'] = dataset['name'].lower()
    dataset['name'] = dataset['name']+str(uuid4())[-6:]
    dataset['owner_org'] = dataset['owner_org'].lower()
    load_europeana_dataset(dataset)


def load_europeana_dataset(dataset):
    headers = {"Authorization": os.getenv("CKAN_TOKEN")}
    resources = dataset.pop('resources')
    r = requests.post(URL_CREATE_DATASET, headers=headers, data=dataset)

    resources["package_id"] = r.json()["result"]["id"]
    resources.pop('created')
    r = requests.post(URL_CREATE_RESOURCE, headers=headers, data=resources)


if __name__ == "__main__":
    fpath = 'path/to/file.json'
    main(fpath)
