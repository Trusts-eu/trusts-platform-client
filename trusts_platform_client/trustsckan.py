import json
import requests
from urllib.parse import urljoin

from datetime import date, timedelta
from uuid import uuid4

from ckanapi import RemoteCKAN


def helper_create_contract_data():
    """
    Create an exemplary contract dictionary.
    """
    contract_duration = 1000  # days
    start_date = date.today()
    end_date = start_date + timedelta(days=contract_duration)
    return {
        "contract_start_date": start_date.isoformat(),
        "contract_start_time": "07:07:16",
        "contract_start_tz": "Africa/Abidjan",
        "contract_end_date": end_date.isoformat(),
        "contract_end_time": "11:11:00",
        "contract_end_tz": "Africa/Abidjan",
        "PROVIDE_ACCESS": "",
        "save": ""
    }


def helper_load_europeana_dataset(fpath):
    """
    Load a Europeana dataset and transform it to the TRUSTS requirements.
    """

    with open(fpath) as f:
        dataset = json.load(f)

    uuid_dataset = str(uuid4())[:6]
    dataset['name'] = dataset['name'].lower()
    dataset['name'] = dataset['name'] + uuid_dataset
    dataset['title'] = dataset['title'] + " UUID: " + uuid_dataset
    dataset['theme'] = "https://trusts.poolparty.biz/Themes/40"
    dataset['owner_org'] = dataset['owner_org'].lower()
    return dataset


class TRUSTSCKAN(RemoteCKAN):
    """
    TRUSTSCKAN is a Python module to access the TRUSTS API. It is built on top
    of *ckanapi* and extends it with the additional functionality of TRUSTS,
    i.e. pushing to the Dataspace Connector and to the central node.
    """

    URL_PUSH_TO_DSC = "ids/actions/push_package/"
    URL_PUSH_TO_CENTRAL = "ids/actions/publish/"

    def post_dataset(self, dataset, contract_data):
        """
        Post a dataset including its contract_data to TRUSTS.

        :param dataset: the metadata of the dataset.
        :param contract_data: the legal details for dataset exchange.
        """

        resources = dataset.pop('resources')
        res = self.call_action('package_create', data_dict=dataset)

        package_id = res['id']
        resources["package_id"] = package_id
        resources.pop('created')
        contract_data['title'] = dataset['title']
        contract_data['pkg_id'] = package_id

        push_url, publish_url = self.__create_url(package_id)

        # requests
        res = self.call_action('resource_create', data_dict=resources)
        headers = {"Authorization": self.apikey}
        _ = requests.get(push_url, headers=headers)
        _ = requests.post(publish_url, json=contract_data, headers=headers)

    def __create_url(self, package_id):
        """
        Creates the final URLs to push the packages to.
        """
        push_url = urljoin(self.address, self.URL_PUSH_TO_DSC, package_id)
        publish_url = urljoin(self.address, self.URL_PUSH_TO_CENTRAL,
                              package_id)
        return push_url, publish_url
