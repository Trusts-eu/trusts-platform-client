import os

import requests
from os.path import join as opj
import datetime
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv()

ckanbase = os.getenv("CKAN_URL","http://localhost:5000/")
apitoken = os.getenv("CKAN_TOKEN")

# ----- The dataset
name = 'an-api-test-'+str(uuid4())[-6:] #This is an ID, has to be
  #     lowercase alphanumeric. We create a random one for tests
dataset_dict = {
    'name': name,
    'title': "An API TEst Dataset "+name[-6:],
    'notes': 'A long description of my dataset'+name[-6:],
    'owner_org': 'vorg'   # <-- I know this exists, created it beforehand in
    # the UI
}

# ----- Its resources
resources = [
    {"url":"http://resource.url/first",
     "description": "The first resource"},
{"url":"http://resource.url/first",
     "description": "The second resource"},
]

# ----- A simple contract
duration = datetime.timedelta(days=10)
contract = {"title": "A simple contract",
            "contract_start" : datetime.datetime.now().isoformat(),
            "contract_end": (datetime.datetime.now()+duration).isoformat()

            }


headers = {"Authorization":apitoken}

# First create the dataset
creation_url = opj(ckanbase, "api/3/action/package_create")
r = requests.post(creation_url, headers=headers, data=dataset_dict)
rj = r.json()
package_id = rj["result"]["id"]

# Let's say this dataset has two resources
resource_url = opj(ckanbase,"api/3/action/resource_create")
resource_ids = []
for resource in resources:
    resource["package_id"] = package_id
    r = requests.post(resource_url, headers=headers, data=resource)
    rj = r.json()
    resource_ids.append(rj["result"]["id"])

# First we pushit to the DSC
push_url = opj(ckanbase,"/ids/actions/push_package/",package_id)

# Then we add a contract to it






