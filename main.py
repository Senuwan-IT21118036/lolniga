import subprocess
import requests
import json
import time

startTime = time.time()

# Replace 'your_api_key' with your actual API key
api_key = '4619bf69-ee30-49e4-b5c2-7de43908683f'

import subprocess

def get_installed_software():
    try:
        # Run the 'dpkg --list' command for Debian-based distributions
        output = subprocess.check_output(['dpkg', '--list']).decode('utf-8')
    except subprocess.CalledProcessError:
        try:
            # Run the 'rpm -qa' command for Red Hat-based distributions
            output = subprocess.check_output(['rpm', '-qa']).decode('utf-8')
        except subprocess.CalledProcessError:
            return []

    # Parse the output to extract the names and versions of the installed software packages
    installed_software = []
    for line in output.split('\n'):
        if line.startswith('ii'):
            software_name = line.split()[1]
            software_version = line.split()[2]
            installed_software.append((software_name, software_version))

    return installed_software

# Print the list of installed software with their versions
installed_software = get_installed_software()
for software_name, software_version in installed_software:
    print(f"{software_name}: {software_version}")
    # Define the URL for the NVD API
    url = f'https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={software_name}&resultsPerPage=100'

    # Send a GET request to the NVD API using the requests library
    response = requests.get(url, headers={'X-Api-Key': api_key})

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the software version is in the list of vulnerable versions
        for item in data['result']['CVE_Items']:
            cve_description = item['cve']['description']['description_data'][0]['value']
            if software_version in cve_description:
                print(f'Vulnerability found for {software_name} version {software_version}: {cve_description}')
    else:
        print(f'Error: Unable to connect to NVD API. Status code: {response.status_code}')
        time.sleep(20)

    time.sleep(5)
print('Time taken:', time.time() - startTime)
