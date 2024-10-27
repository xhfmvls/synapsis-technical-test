import subprocess

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

# Example usage
project_key = "sast-automation"
scan_project_directory = "."
sonar_host_url = "http://localhost:9000"
sonar_token = "sqp_28ebcbc83b6279e76dde9f1f88e82dfa19dc8c79"

run_sonar_scanner(project_key, scan_project_directory, sonar_host_url, sonar_token)
