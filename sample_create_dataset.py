import copy
import json
import os
from datetime import date, timedelta
from os.path import join as opj
from uuid import uuid4

import requests
from dotenv import load_dotenv

load_dotenv()


def create_and_push(apitoken,
                    ckanbase,
                    dataset_dict,
                    resources,
                    default_contract):
    headers = {"Authorization": apitoken}

    # First create the dataset
    creation_url = opj(ckanbase, "api/3/action/package_create")
    r = requests.post(creation_url, headers=headers, data=dataset_dict)
    rj = r.json()
    if r.status_code > 299:
        print("---ERROR Creating Dataset------------------------\n",
              json.dumps(rj, indent=1))
        return None

    package_id = rj["result"]["id"]

    # Let's say this dataset has two resources
    resource_url = opj(ckanbase, "api/3/action/resource_create")
    resource_ids = []
    for resource in resources:
        resource["package_id"] = package_id
        r = requests.post(resource_url, headers=headers, data=resource)
        rj = r.json()
        if r.status_code > 299:
            print("---ERROR Creating Resources------------------------\n",
                  json.dumps(rj, indent=1))
            return None
        resource_ids.append(rj["result"]["id"])

    # First we pushit to the DSC
    push_url = opj(ckanbase, "ids/actions/push_package/", package_id)
    r = requests.get(push_url, headers=headers)
    print("-------")
    rj = r.json()
    if r.status_code > 299:
        print("---ERROR Pushing to DSC------------------------\n",
              json.dumps(rj, indent=1))
        return None


    # Finally we push it to the Broker with a Contract
    publish_url = opj(ckanbase, "ids/actions/publish/", package_id)
    contract_data = copy.deepcopy(default_contract)
    contract_data["pkg_id"] = package_id
    r = requests.post(publish_url, json=contract_data, headers=headers)
    print("-------")
    rj = r.json()
    if r.status_code > 299:
        print("---ERROR Creating Contract------------------------\n",
              json.dumps(rj, indent=1))
        return None

    return package_id


if __name__ == "__main__":
    ckanbase = os.getenv("CKAN_URL", "http://localhost:5000/")
    apitoken = os.getenv("CKAN_TOKEN")


    # ----- Contract details ----
    contract_duration = 1000  # days
    start_date = date.today()
    end_date = start_date + timedelta(days=contract_duration)
    default_contract = contract_data = {
        "title": "MISSING",
        "pkg_id": "MISSING",
        "contract_start_date": start_date.isoformat(),
        "contract_start_time": "07:07:16",
        "contract_start_tz": "Africa/Abidjan",
        "contract_end_date": end_date.isoformat(),
        "contract_end_time": "11:11:00",
        "contract_end_tz": "Africa/Abidjan",
        "PROVIDE_ACCESS": "",
        "save": ""
    }

    # ----- The dataset ----
    name = 'an-api-test-' + str(uuid4())[-6:]  # This is an ID, has to be
    #     lowercase alphanumeric. We create a random one for tests
    dataset_dict = {
        'name': name,
        'title': "An API TEst Dataset " + name[-6:],
        'notes': 'A long description of my dataset' + name[-6:],
        'owner_org': 'victor-organization',  # <-- I know this exists,
        # created it beforehand in
        'theme': "https://trusts.org/vacabulary/themes/Industry"
        # the UI
    }

    # ----- Its resources
    resources = [
        {"url": "http://resource.url/first",
         "description": "The first resource"},
        {"url": "http://resource.url/first",
         "description": "The second resource"},
    ]

    create_and_push(apitoken,
                    ckanbase,
                    dataset_dict,
                    resources,
                    default_contract)
