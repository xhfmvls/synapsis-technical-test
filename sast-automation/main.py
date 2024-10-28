import subprocess
import requests
import json
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

def json_to_pdf(data, output_pdf_path):
    # Load data
    components = data['components']
    hotspots = data['hotspots']
    
    # Create PDF document
    pdf = SimpleDocTemplate(output_pdf_path, pagesize=A4)
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    table_title_style = styles['Heading2']
    normal_style = styles['BodyText']
    hotspots_title_style = styles['Heading3']

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
    
    # Components Table
    elements.append(Paragraph("Components", table_title_style))
    components_data = [[
        "Key", "Qualifier", "Name", "Path"
    ]] + [[comp['key'], comp['qualifier'], comp['name'], comp['path']] for comp in components]
    
    components_table = Table(components_data)
    components_table.setStyle(components_table_style)
    elements.append(components_table)
    
    # Add space between tables
    elements.append(Spacer(1, 0.5 * inch))

    # Hotspots Table
    elements.append(Paragraph("Hotspots", table_title_style))

    # Create a dictionary for component key-to-path lookup
    component_path_map = {comp['key']: comp['path'] for comp in components}

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
    
    # Add hotspot details
    for hs in hotspots:
        elements.append(Paragraph(hs['key'], hotspots_title_style))
        elements.append(Paragraph(f"Component: {next(comp['path'] for comp in components if comp['key'] == hs['component'])}", normal_style))
        elements.append(Paragraph(f"Security Category: {hs['securityCategory']}", normal_style))
        elements.append(Paragraph(f"Vulnerability Probability: {hs['vulnerabilityProbability']}", normal_style))
        elements.append(Paragraph(f"Line: {hs['line']}", normal_style))
        elements.append(Paragraph(f"Message: {hs['message']}", normal_style))
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
hotspots = get_hotspots(sonar_host_url, project_key, sonar_token)

# TODO: Convert hotspots into pdf report
# TODO: Get data by args flag from command line