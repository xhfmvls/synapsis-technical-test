import subprocess
import requests

def run_sonar_scanner(project_key, scan_project_directory, sonar_host_url, sonar_token):
    # Use the full path to sonar-scanner.bat
    sonar_scanner_path = 'D:\\sonarscanner\\sonar-scanner-6.2.1.4610-windows-x64\\bin\\sonar-scanner.bat'
    
    # Construct the command with the provided arguments
    command = [
        sonar_scanner_path,
        f'-Dsonar.projectKey={project_key}',
        f'-Dsonar.sources={scan_project_directory}',
        f'-Dsonar.host.url={sonar_host_url}',
        f'-Dsonar.token={sonar_token}'
    ]

    try:
        # Run the command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        # Print the output
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Print the error output if the command fails
        print(f"Error: {e.stderr}")

def get_hotspots(sonar_host_url, project_key, sonar_token):
    # Construct the URL for fetching hotspots
    url = f"{sonar_host_url}/api/hotspots/search"
    params = {'project': project_key}
    headers = {
        'Authorization': f'Bearer {sonar_token}'  # Use Bearer token for authentication
    }

    # Send a GET request to fetch the hotspots
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        hotspots = response.json().get('hotspots', [])
        # Print each hotspot's key and description
        for hotspot in hotspots:
            print(f"Hotspot Key: {hotspot['key']}")
        return hotspots
    else:
        print(f"Failed to fetch hotspots: {response.status_code} - {response.text}")
        return []


# Example usage
project_key = ""
scan_project_directory = "."
sonar_host_url = "http://localhost:9000"
sonar_token = ""

run_sonar_scanner(project_key, scan_project_directory, sonar_host_url, sonar_token)
get_hotspots(sonar_host_url, project_key, sonar_token)