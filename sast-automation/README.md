# sast-automation

## Overview

This directory contains the solution for the **Static Application Security Testing and Automation** Challenge.<br>
For this challenge, I created a script that allow you to generate SonarQube vulnerability (security hotspots) report in PDF format.<br>

Below is a brief explanation of the script, the explanation of the approach used to script, documentation on how to run the script, and several notes regarding the solution.

## Code

### Techstack / Reqruitments
- Python (language of the Script)
- SonarQube (SAST App)
- SonarScanner CLI (CLI for SonarQube)
- Java 17 (to run SonarQube SonarScanner CLI)

### Python Libraries Used
- subprocess
- requests
- pandas
- reportlab
- argparse

## Approach
### Problem 1
Required to create a script/program to interface with a SAST.
#### Solution:
Create a script with **Python** that able to communicate/interface with **SonarQube** through its CLI (**SonarScanner CLI**) and API Request. I chose **SonarQube** SAST because it is an open-source tool, which allow me to run it on my own machine.<br>
### Problem 2
Required to scan the source code in a specified directory.
#### Solution:
Use **SonarScanner CLI** that enable us to scan a specific directory as long as we create the **sonar-project.properties** file is the base directory.<br>
### Problem 3
Required to output the vulnerability in a formatted PDF format.
#### Solution:
Use **reportlab** library that are used for generating PDFs and graphics. I provide the generated report example on this directory (**report_example.pdf**)<br><br>

## Setup (Documentation)

### 1. Install all required libraries
```sh
pip install requests

pip install pandas

pip install reportlab
```

### 2. Create the project in SonarQube
```
Projects -> Create Project -> Local Project -> [Create Project]
```

### 3. Generate User Token
```
Account (Administrator) -> Security -> [Generate User Token]
```

### 4. Setting up the sonar-project.properties file on base directory
```sh
# fill the fields with you environment setup (from the second step)
sonar.projectKey=
sonar.projectName=
sonar.sources=.
sonar.sourceEncoding=UTF-8
```

### 5. Setting up the Project Permission
```
Project Settings -> Permissions -> [Add Execute Analysis Permission to the designated User/Group]
```

### 6. Run the script on base directory
```sh
python .\generate-sq-report.py --project [Project-Name] --token [SonarQube-Token]
```