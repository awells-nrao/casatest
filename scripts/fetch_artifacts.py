############    Imports    ############

import os, sys, json, requests
from pathlib import Path

############    Variables    ############

baseurl="open-bamboo.nrao.edu"
projectKeys = [ "CASA-REMTA"]
projectKey = projectKeys[0]
############    Functions    ############

def access_api(url):
    headers = { "Accept": "application/json" }
    response = requests.request( "GET", url, headers=headers)
    return json.loads(response.text)

def download_tar_file(url, filename):
    print("Downloading: ", url)
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

fetchurl = f"http://{baseurl}/rest/api/latest/result/{projectKey}"
print(f"Fetching build results from {fetchurl}")
data = access_api(fetchurl)
#print(data)
build_urls = []
buildResultKeys = []
#if 'status-code' in data.keys() and data['status-code'] != 200:
#    print("Error accessing API: ", data['status-code'])
#    continue
for result in data["results"]["result"]:
    if "CASA-REMTA-4" in result['buildResultKey'] or "CASA-REMTA-5" in result['buildResultKey']:
        continue
    buildResultKeys.append(result['buildResultKey'])
buildResultKeys = [item for item in buildResultKeys if item not in set(["CASA-REMTA-60", "CASA-REMTA-61", "CASA-REMTA-62"])]
print("Build Result Keys: ", buildResultKeys)
for directory in buildResultKeys:
    directory_path = os.path.join(os.getcwd(),"results",directory)
    Path(directory_path).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    download_url = f"https://{baseurl}/browse/{directory}/artifact/shared/Tasks-Workdir/work-casatasks-manylinux228-3.12.tar.gz"
    target_file = os.path.join(directory_path,f"{directory}.work-casatasks-manylinux228-3.12.tar.gz")

    if not os.path.exists(target_file):
        print("Fetching : ",directory )
        print("Saving to : ",directory_path )
        print(f"Downloading from {download_url} to {target_file}")
        try:
            download_tar_file(download_url, target_file)
        except Exception as e:
            print(f"Error downloading {download_url}: {e}")
    

