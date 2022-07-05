import json
import os
import requests
from datetime import date, timedelta

from uuid import uuid4

from dotenv import load_dotenv


load_dotenv()

URL_CREATE_DATASET = os.path.join(
    os.getenv("CKAN_URL", "http://localhost:5000/"),
    "api/3/action/package_create")
URL_CREATE_RESOURCE = os.path.join(
    os.getenv("CKAN_URL", "http://localhost:5000/"),
    "api/3/action/resource_create")
URL_PUSH_TO_DSC = os.path.join(
    os.getenv("CKAN_URL", "http://localhost:5000/"),
    "ids/actions/push_package/")
URL_PUSH_TO_CENTRAL = os.path.join(
    os.getenv("CKAN_URL", "http://localhost:5000/"),
    "ids/actions/publish/")

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


def main(europeana_dir):
    for i, fname in enumerate(os.listdir(europeana_dir)[:200]):
        load_europeana_dataset(os.path.join(europeana_dir, fname))


def load_europeana_dataset(fpath):
    with open(fpath) as f:
        dataset = json.load(f)
    dataset['name'] = dataset['name'].lower()
    dataset['name'] = dataset['name']+str(uuid4())[-6:]
    dataset['theme'] = "https://trusts.poolparty.biz/Themes/40"
    dataset['owner_org'] = dataset['owner_org'].lower()
    post_dataset(dataset)


def post_dataset(dataset):
    headers = {"Authorization": os.getenv("CKAN_TOKEN")}
    resources = dataset.pop('resources')
    r = requests.post(URL_CREATE_DATASET, headers=headers, data=dataset)
    package_id = r.json()["result"]["id"]

    resources["package_id"] = package_id
    resources.pop('created')
    r = requests.post(URL_CREATE_RESOURCE, headers=headers, data=resources)

    push_url = URL_PUSH_TO_DSC + package_id
    r = requests.get(push_url, headers=headers)

    contract_data = default_contract
    contract_data["pkg_id"] = package_id
    contract_data["title"] = "Contract for "+dataset["title"]
    publish_url = URL_PUSH_TO_CENTRAL + package_id
    r = requests.post(publish_url, json=contract_data, headers=headers)


if __name__ == "__main__":
    fpath = 'europeana_test_jsons'
    main(fpath)
