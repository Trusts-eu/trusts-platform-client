## Python client for the TRUSTS platfrom

This collection of python scripts and modules is meant to be a way to 
programatically access the TRUSTS platform. 

### Pre-requisistes

1. (Optional but recommended) create a python virtual environment and 
   activate it
1. Clone this repo
1. Make a copy of the `.env_example` file and call it `.env`
1. Get an API token from your platform's node. Go to  
   http://ckan.url/user/admin/api-tokens  logged in as user admin.
   
1. Paste this token in the `.env` file
1. Install the required libraries with `pip install -r requirements.txt`


### Things that you can try already

1. Create a dataset in ckan `python sample_create_dataset.py`
