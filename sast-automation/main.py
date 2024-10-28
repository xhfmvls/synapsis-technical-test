import subprocess
import requests
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

def get_hotspot_details(sonar_host_url, hotspot_key, sonar_token):
    url = f"{sonar_host_url}/api/hotspots/show"
    params = {'hotspot': hotspot_key}
    headers = {
        'Authorization': f'Bearer {sonar_token}'  # Use Bearer token for authentication
    }

    # Send a GET request to fetch the hotspot details
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()  # Return the JSON data if successful
    else:
        print(f"Failed to fetch hotspot details for {hotspot_key}: {response.status_code} - {response.text}")

def json_to_pdf(data, output_pdf_path, sonar_token, project_key):
    # Load data
    components = data['components']
    hotspots = data['hotspots']
    
    # Create PDF document
    pdf = SimpleDocTemplate(output_pdf_path, pagesize=A4)
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    table_title_style = styles['Heading2']
    normal_style = styles['Heading4']
    hotspots_title_style = styles['Heading3']
    content_style = styles['Normal']

    components_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    hotspots_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8)  # Shrinked font size for hotspots
    ])
    
    # Overview
    elements.append(Paragraph(f"Project: {project_key}", styles['Heading1']))
    elements.append(Paragraph(f"Visit: http://localhost:9000/dashboard?id={project_key} for more details.", styles['Heading3']))
    elements.append(Paragraph(f"{len(hotspots)} Security Hotspot(s)", styles['Heading3']))
    elements.append(Spacer(1, 0.5 * inch))  # Space after overview

    # Components Table
    elements.append(Paragraph("Components", table_title_style))
    components_data = [[
        "Key", "Qualifier", "Name", "Path"
    ]] + [[
        comp['key'], 
        comp['qualifier'], 
        comp['name'], 
        comp.get('path', "")  # Use get to avoid KeyError, returning "" if 'path' is missing
    ] for comp in components]
    
    components_table = Table(components_data)
    components_table.setStyle(components_table_style)
    elements.append(components_table)
    
    # Add space between tables
    elements.append(Spacer(1, 0.5 * inch))

    # Hotspots Table
    elements.append(Paragraph("Hotspots", table_title_style))

    # Create a dictionary for component key-to-path lookup
    component_path_map = {comp['key']: comp.get('path', '') for comp in components}

    # Generate the hotspots data with component paths
    hotspots_data = [[
        "Key", "Component Path", "Security Category", 
        "Vulnerability Probability", "Line"
    ]] + [[
        hs['key'], component_path_map.get(hs['component'], 'N/A'),  # Replace component key with path
        hs['securityCategory'], hs['vulnerabilityProbability'], hs['line']
    ] for hs in hotspots]
    
    hotspots_table = Table(hotspots_data)
    hotspots_table.setStyle(hotspots_table_style)
    elements.append(hotspots_table)

    # Add space between table and details
    elements.append(Spacer(1, 0.5 * inch))

    # Hotspot Details
    elements.append(Paragraph("Hotspots Details", table_title_style))

    for hs in hotspots:
        elements.append(Paragraph(hs['key'], hotspots_title_style))
        
        # Fetch detailed information for the current hotspot
        hotspot_details = get_hotspot_details("http://localhost:9000", hs['key'], sonar_token)
        
        if hotspot_details:  # Check if details were fetched successfully
            # Extract relevant information from the rule
            rule = hotspot_details.get('rule', {})
            security_category = rule.get('securityCategory', 'N/A')
            vulnerability_probability = rule.get('vulnerabilityProbability', 'N/A')
            risk_description = rule.get('riskDescription', 'N/A')
            
            # Create paragraphs for the extracted information
            elements.append(Paragraph(f"Component: {next(comp['path'] for comp in components if comp['key'] == hs['component'])}", normal_style))
            elements.append(Paragraph(f"Security Category: {security_category}", normal_style))
            elements.append(Paragraph(f"Vulnerability Probability: {vulnerability_probability}", normal_style))
            elements.append(Paragraph(f"Line: {hs['line']}", normal_style))
            elements.append(Paragraph(f"Message: {hs['message']}", normal_style))
            elements.append(Paragraph(f"Risk Description:", normal_style))
            elements.append(Paragraph(f"{risk_description}", content_style))
            elements.append(Spacer(1, 0.2 * inch))  # Space after each hotspot detail
    
    # Build PDF
    pdf.build(elements)


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
        return response.json()
    else:
        print(f"Failed to fetch hotspots: {response.status_code} - {response.text}")
        return []


# Example usage
project_key = ""
scan_project_directory = "."
sonar_host_url = "http://localhost:9000"
sonar_token = ""

# Run the SonarQube scanner
run_sonar_scanner(project_key, scan_project_directory, sonar_host_url, sonar_token)

# Fetch hotspots from SonarQube
hotspots = get_hotspots(sonar_host_url, project_key, sonar_token)

# Convert hotspots json into pdf report
json_to_pdf(hotspots, 'hotspots_report.pdf', sonar_token, project_key)

# TODO: Get data by args flag from command line