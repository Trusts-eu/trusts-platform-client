# TRUSTS platform client 

The TRUSTS platform client is a way to programatically access the TRUSTS 
platform. It is built on top of [ckanapi](https://github.com/ckan/ckanapi),
which itself is a wrapper around the [CKAN Action API](http://docs.ckan.org/en/latest/api/index.html#action-api-reference).
The TRUSTS platform client extends ckanapi with all functionality required to
fully interoperate with TRUSTS programmatically, i.e. including functionality
to push the Dataspace Connector or to push to the central node. Using ckanapi
as the basis makes sure that all core functionality available in CKAN is also
available from the TRUSTS platform client.

## Installation

1. **Virtual environment (optional but recommended):** create a python virtual environment and 
   activate it:

```
python3 -m venv venv
source venv/bin/activate
```

2. **Installation:**

```
pip install git+https://gitlab.com/trusts-platform/trusts-platform-client.git
```

## Usage

1. Log into your TRUSTS node as an admin user and get an API token in the
   [admin area](http://ckan.url/user/admin/api-tokens).

2. Import the class ```TRUSTSCKAN```, the main class for exchanging data with
TRUSTS:

    ```
    >>> from trusts_platform_client import TRUSTSCKAN
    ```

3. Connect to a running TRUSTS instance:

    ```
    >>> trusts_url = 'http://127.0.0.1:5000/' # Replace this with your actual URL
    >>> CKAN_TOKEN = <YOUR_API_TOKEN>
    >>> _trustsckan = TRUSTSCKAN(trusts_url, apikey=CKAN_TOKEN)
    ```

4. Check that you can access it:

    ```
    >>> _trustsckan.action.status_show()
    ```

5. Import helper functions to create exemplary data for testing purposes:

    ```
    >>> from trusts_platform_client.trustsckan import helper_load_europeana_dataset, helper_create_contract_data
    ```

6. Actually create the exemplary data:

    ```
    >>> dataset = helper_load_europeana_data()
    >>> contract_data = helper_create_contract_data()
    ```

7. Transfer the exemplary data into TRUSTS:

    ```
    >>> _trustsckan.post_dataset(dataset, contract_data)
    ```

## Funding
This code was created as part of project TRUSTS: Trusted secure data sharing space.

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement [No 871481](https://cordis.europa.eu/project/id/871481).




