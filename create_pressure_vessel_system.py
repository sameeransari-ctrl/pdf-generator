#!/usr/bin/env python3
"""
Pressure Vessel Inspection Report Generator
This script generates a fillable PDF template for the Pressure Vessel Inspection Report
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def create_pressure_vessel_template():
    """Create a fillable PDF template for Pressure Vessel Inspection Report"""
    
    filename = "Pressure_Vessel_Inspection_Report_TEMPLATE.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # ============================================================
    # PAGE 1 - COVER PAGE
    # ============================================================
    
    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 120, width, 120, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 70, "PRESSURE VESSEL INSPECTION REPORT")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 95, "WESTERN AIR COMPLIANCE")
    c.drawString(50, height - 110, "Inspection • Testing • Certification")
    
    # Prepared For Section
    y = height - 160
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Prepared For:")
    
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Client / Company:")
    c.rect(150, y - 5, 350, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Address:")
    c.rect(150, y - 5, 350, 18, stroke=True, fill=False)
    
    # Prepared By Section
    y -= 45
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Prepared By:")
    
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Western Air Compliance")
    c.drawString(50, y - 15, "Technician: Glenn Scatchard")
    c.drawString(50, y - 30, "Email: info@westernaircompliance.com.au")
    c.drawString(50, y - 45, "Phone: 0459 851 411")
    
    # Report Details
    y -= 85
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Report Date:")
    c.rect(150, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Job Number:")
    c.rect(150, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Reference:")
    c.rect(150, y - 5, 150, 18, stroke=True, fill=False)
    
    # Confidentiality Notice
    y -= 60
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Confidentiality Notice")
    
    y -= 20
    c.setFont("Helvetica", 8)
    notice_text = """This report has been prepared exclusively for the client specified above. 
It contains information relating to the inspection, testing, and assessment of pressure 
equipment and associated components. No part of this report may be reproduced, 
distributed, or used without written permission from Western Air Compliance."""
    
    text_lines = notice_text.split('\n')
    for line in text_lines:
        c.drawString(50, y, line.strip())
        y -= 12
    
    c.showPage()
    
    # ============================================================
    # PAGE 2 - MAIN INSPECTION REPORT
    # ============================================================
    
    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, height - 40, "PRESSURE VESSEL INSPECTION REPORT TO AS/NZS 3788:2024")
    
    # Main content area
    y = height - 100
    c.setFillColor(colors.black)
    
    # Client Information Section
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Client & Equipment Details")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Client / Company:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Site:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Address:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Contact:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Manufacturer:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "PO / Reference No:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Model:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Asset No:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Serial No:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Test Date:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Test Number:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Unit Type:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    # Vessel Details Section
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Vessel Details")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Manufacturer:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Serial No:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Manufactured Date:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Design Code:")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Location:")
    c.rect(170, y - 5, 180, 18, stroke=True, fill=False)
    
    c.drawString(370, y, "Corrosion Allowance (mm):")
    c.rect(430, y - 5, 150, 18, stroke=True, fill=False)
    
    c.showPage()
    
    # ============================================================
    # PAGE 3 - DESIGN INFORMATION & TEST RESULTS
    # ============================================================
    
    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 40, "DESIGN INFORMATION & TEST RESULTS")
    
    y = height - 100
    c.setFillColor(colors.black)
    
    # Pressure Vessel Design Information
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Pressure Vessel Design Information")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Type:")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    c.drawString(360, y, "Tank Capacity:")
    c.rect(460, y - 5, 110, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Design Registration No:")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    c.drawString(360, y, "Hydrostatic Test Date:")
    c.rect(460, y - 5, 110, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "WorkSafe Registration No:")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    c.drawString(360, y, "Design Temperature (°C):")
    c.rect(460, y - 5, 110, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Commissioning Date:")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    c.drawString(360, y, "Ambient Air Temp (°C):")
    c.rect(460, y - 5, 110, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Design Pressure (kPa):")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    c.drawString(360, y, "Shell Length (mm):")
    c.rect(460, y - 5, 110, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Operating Pressure (kPa):")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    c.drawString(360, y, "Shell Diameter (mm):")
    c.rect(460, y - 5, 110, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Test Pressure (kPa):")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Hazard Level (AS/NZS 3788:2024):")
    c.rect(200, y - 5, 140, 18, stroke=True, fill=False)
    
    # Inspection Criteria Section
    y -= 50
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Compliance Standards & Inspection Criteria")
    c.setFillColor(colors.black)
    
    y -= 20
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Inspection carried out in accordance with:")
    c.drawString(50, y - 15, "• AS/NZS 3788:2024 - Pressure Equipment - In-Service Inspection")
    c.drawString(50, y - 30, "• AS 1210 - Pressure Vessels")
    
    # Inspection Results Section
    y -= 70
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Inspection Results")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Visual Inspection:")
    
    checkbox_y = y + 2
    c.rect(170, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(190, y, "PASS")
    
    c.rect(240, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(260, y, "FAIL")
    
    y -= 25
    c.drawString(50, y, "Pressure Test:")
    
    checkbox_y = y + 2
    c.rect(170, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(190, y, "PASS")
    
    c.rect(240, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(260, y, "FAIL")
    
    y -= 25
    c.drawString(50, y, "Safety Devices:")
    
    checkbox_y = y + 2
    c.rect(170, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(190, y, "PASS")
    
    c.rect(240, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(260, y, "FAIL")
    
    # Overall Result
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Overall Result:")
    
    c.rect(180, y - 5, 80, 25, fill=False, stroke=True)
    c.setFillColor(colors.black)
    
    c.showPage()
    
    # ============================================================
    # PAGE 4 - COMMENTS AND SIGNATURE
    # ============================================================
    
    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 40, "COMMENTS & CERTIFICATION")
    
    y = height - 100
    c.setFillColor(colors.black)
    
    # Comments Section
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Inspection Comments & Observations")
    c.setFillColor(colors.black)
    
    y -= 20
    c.rect(50, y - 120, 510, 120, stroke=True, fill=False)
    
    # Recommendations Section
    y -= 150
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Recommendations")
    c.setFillColor(colors.black)
    
    y -= 20
    c.rect(50, y - 80, 510, 80, stroke=True, fill=False)
    
    # Next Inspection Due
    y -= 110
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Next Inspection Due:")
    c.rect(200, y - 5, 150, 20, stroke=True, fill=False)
    
    # Inspector Declaration
    y -= 50
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Inspector Declaration")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica", 9)
    declaration = """I certify that the pressure vessel detailed above has been inspected in accordance 
with AS/NZS 3788:2024, and that the results recorded are true and correct at the time of inspection."""
    
    lines = declaration.split('\n')
    for line in lines:
        c.drawString(50, y, line.strip())
        y -= 12
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Inspector: Glenn Scatchard")
    
    y -= 30
    c.drawString(50, y, "Signature:")
    c.line(130, y - 5, 300, y - 5)
    
    c.drawString(350, y, "Date:")
    c.line(400, y - 5, 520, y - 5)
    
    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, "Western Air Compliance | ABN - 36 280 464 689")
    c.drawString(400, 30, f"Page 4 of 4")
    
    c.save()
    print(f"Template PDF created: {filename}")
    return filename

def create_pressure_vessel_web_form():
    """Create an HTML form for Pressure Vessel Inspection Report"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pressure Vessel Inspection Report Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2E75B6 0%, #1a4d7a 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 26px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .form-content {
            padding: 40px;
        }
        
        .form-section {
            margin-bottom: 35px;
            padding-bottom: 25px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .form-section:last-child {
            border-bottom: none;
        }
        
        .section-title {
            font-size: 20px;
            color: #2E75B6;
            margin-bottom: 20px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }
        
        .section-title::before {
            content: '';
            width: 4px;
            height: 24px;
            background: #2E75B6;
            margin-right: 12px;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .form-row.single {
            grid-template-columns: 1fr;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
        }
        
        label {
            font-size: 14px;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        input[type="text"],
        input[type="date"],
        input[type="number"],
        textarea,
        select {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #2E75B6;
            box-shadow: 0 0 0 3px rgba(46, 117, 182, 0.1);
        }
        
        textarea {
            min-height: 80px;
            resize: vertical;
            font-family: Arial, sans-serif;
        }
        
        .checkbox-group {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .checkbox-option {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .checkbox-option input[type="checkbox"] {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        
        .button-group {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        
        button {
            flex: 1;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #2E75B6 0%, #1a4d7a 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(46, 117, 182, 0.4);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .button-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚙️ Pressure Vessel Inspection Report Generator</h1>
            <p>Western Air Compliance | AS/NZS 3788:2024 Compliance</p>
        </div>
        
        <div class="form-content">
            <form id="pressureVesselForm">
                <!-- Client Information Section -->
                <div class="form-section">
                    <div class="section-title">Client & Equipment Details</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientCompany">Client / Company Name *</label>
                            <input type="text" id="clientCompany" name="clientCompany" required>
                        </div>
                        <div class="form-group">
                            <label for="site">Site</label>
                            <input type="text" id="site" name="site">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientAddress">Address *</label>
                            <input type="text" id="clientAddress" name="clientAddress" required>
                        </div>
                        <div class="form-group">
                            <label for="contact">Contact</label>
                            <input type="text" id="contact" name="contact">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="manufacturer">Manufacturer *</label>
                            <input type="text" id="manufacturer" name="manufacturer" required>
                        </div>
                        <div class="form-group">
                            <label for="poReference">PO / Reference No</label>
                            <input type="text" id="poReference" name="poReference">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="model">Model *</label>
                            <input type="text" id="model" name="model" required>
                        </div>
                        <div class="form-group">
                            <label for="assetNo">Asset No</label>
                            <input type="text" id="assetNo" name="assetNo">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="serialNo">Serial No *</label>
                            <input type="text" id="serialNo" name="serialNo" required>
                        </div>
                        <div class="form-group">
                            <label for="testDate">Test Date *</label>
                            <input type="date" id="testDate" name="testDate" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="testNumber">Test Number *</label>
                            <input type="text" id="testNumber" name="testNumber" required>
                        </div>
                        <div class="form-group">
                            <label for="unitType">Unit Type</label>
                            <input type="text" id="unitType" name="unitType">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="reportDate">Report Date *</label>
                            <input type="date" id="reportDate" name="reportDate" required>
                        </div>
                        <div class="form-group">
                            <label for="jobNumber">Job Number *</label>
                            <input type="text" id="jobNumber" name="jobNumber" required>
                        </div>
                    </div>
                </div>
                
                <!-- Vessel Details Section -->
                <div class="form-section">
                    <div class="section-title">Vessel Details</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="vesselManufacturer">Manufacturer</label>
                            <input type="text" id="vesselManufacturer" name="vesselManufacturer">
                        </div>
                        <div class="form-group">
                            <label for="vesselSerialNo">Serial No</label>
                            <input type="text" id="vesselSerialNo" name="vesselSerialNo">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="manufacturedDate">Manufactured Date</label>
                            <input type="date" id="manufacturedDate" name="manufacturedDate">
                        </div>
                        <div class="form-group">
                            <label for="designCode">Design Code</label>
                            <input type="text" id="designCode" name="designCode" value="AS 1210-3">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="location">Location</label>
                            <input type="text" id="location" name="location" value="Itinerant">
                        </div>
                        <div class="form-group">
                            <label for="corrosionAllowance">Corrosion Allowance (mm)</label>
                            <input type="number" id="corrosionAllowance" name="corrosionAllowance" step="0.1">
                        </div>
                    </div>
                </div>
                
                <!-- Design Information Section -->
                <div class="form-section">
                    <div class="section-title">Pressure Vessel Design Information</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="vesselType">Type</label>
                            <input type="text" id="vesselType" name="vesselType">
                        </div>
                        <div class="form-group">
                            <label for="tankCapacity">Tank Capacity</label>
                            <input type="text" id="tankCapacity" name="tankCapacity">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="designRegNo">Design Registration No</label>
                            <input type="text" id="designRegNo" name="designRegNo">
                        </div>
                        <div class="form-group">
                            <label for="hydrostaticTestDate">Hydrostatic Test Date</label>
                            <input type="date" id="hydrostaticTestDate" name="hydrostaticTestDate">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="worksafeRegNo">WorkSafe Registration No</label>
                            <input type="text" id="worksafeRegNo" name="worksafeRegNo">
                        </div>
                        <div class="form-group">
                            <label for="designTemp">Design Temperature (°C)</label>
                            <input type="number" id="designTemp" name="designTemp" step="0.1">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="commissioningDate">Commissioning Date</label>
                            <input type="date" id="commissioningDate" name="commissioningDate">
                        </div>
                        <div class="form-group">
                            <label for="ambientTemp">Ambient Air Temperature (°C)</label>
                            <input type="number" id="ambientTemp" name="ambientTemp" step="0.1">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="designPressure">Design Pressure (kPa) *</label>
                            <input type="number" id="designPressure" name="designPressure" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label for="shellLength">Shell Length (mm)</label>
                            <input type="number" id="shellLength" name="shellLength" step="0.1">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="operatingPressure">Operating Pressure (kPa) *</label>
                            <input type="number" id="operatingPressure" name="operatingPressure" step="0.01" required>
                        </div>
                        <div class="form-group">
                            <label for="shellDiameter">Shell Diameter (mm)</label>
                            <input type="number" id="shellDiameter" name="shellDiameter" step="0.1">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="testPressure">Test Pressure (kPa)</label>
                            <input type="number" id="testPressure" name="testPressure" step="0.01">
                        </div>
                        <div class="form-group">
                            <label for="hazardLevel">Hazard Level (AS/NZS 3788:2024)</label>
                            <select id="hazardLevel" name="hazardLevel">
                                <option value="">Select hazard level</option>
                                <option value="A">Level A</option>
                                <option value="B">Level B</option>
                                <option value="C">Level C</option>
                                <option value="D">Level D</option>
                                <option value="E">Level E</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <!-- Inspection Results Section -->
                <div class="form-section">
                    <div class="section-title">Inspection Results</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Visual Inspection</label>
                            <div class="checkbox-group">
                                <div class="checkbox-option">
                                    <input type="radio" id="visualPass" name="visualInspection" value="PASS">
                                    <label for="visualPass">PASS</label>
                                </div>
                                <div class="checkbox-option">
                                    <input type="radio" id="visualFail" name="visualInspection" value="FAIL">
                                    <label for="visualFail">FAIL</label>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Pressure Test</label>
                            <div class="checkbox-group">
                                <div class="checkbox-option">
                                    <input type="radio" id="pressurePass" name="pressureTest" value="PASS">
                                    <label for="pressurePass">PASS</label>
                                </div>
                                <div class="checkbox-option">
                                    <input type="radio" id="pressureFail" name="pressureTest" value="FAIL">
                                    <label for="pressureFail">FAIL</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Safety Devices</label>
                            <div class="checkbox-group">
                                <div class="checkbox-option">
                                    <input type="radio" id="safetyPass" name="safetyDevices" value="PASS">
                                    <label for="safetyPass">PASS</label>
                                </div>
                                <div class="checkbox-option">
                                    <input type="radio" id="safetyFail" name="safetyDevices" value="FAIL">
                                    <label for="safetyFail">FAIL</label>
                                </div>
                            </div>
                        </div>
                        <div class="form-group">
                            <label>Overall Result</label>
                            <div class="checkbox-group">
                                <div class="checkbox-option">
                                    <input type="radio" id="overallPass" name="overallResult" value="PASS" checked>
                                    <label for="overallPass">PASS</label>
                                </div>
                                <div class="checkbox-option">
                                    <input type="radio" id="overallFail" name="overallResult" value="FAIL">
                                    <label for="overallFail">FAIL</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Comments Section -->
                <div class="form-section">
                    <div class="section-title">Comments & Recommendations</div>
                    
                    <div class="form-row single">
                        <div class="form-group">
                            <label for="comments">Inspection Comments & Observations</label>
                            <textarea id="comments" name="comments" placeholder="Enter inspection observations, findings, and any deviations noted..."></textarea>
                        </div>
                    </div>
                    
                    <div class="form-row single">
                        <div class="form-group">
                            <label for="recommendations">Recommendations</label>
                            <textarea id="recommendations" name="recommendations" placeholder="Enter any recommendations for repairs, maintenance, or follow-up actions..."></textarea>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="nextInspectionDue">Next Inspection Due</label>
                            <input type="date" id="nextInspectionDue" name="nextInspectionDue">
                        </div>
                    </div>
                </div>
                
                <!-- Signature Section -->
                <div class="form-section">
                    <div class="section-title">Inspector Declaration</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="inspectorName">Inspector Name</label>
                            <input type="text" id="inspectorName" name="inspectorName" value="Glenn Scatchard">
                        </div>
                        <div class="form-group">
                            <label for="signatureDate">Signature Date</label>
                            <input type="date" id="signatureDate" name="signatureDate">
                        </div>
                    </div>
                </div>
                
                <!-- Action Buttons -->
                <div class="button-group">
                    <button type="button" class="btn-secondary" onclick="resetForm()">Clear Form</button>
                    <button type="submit" class="btn-primary">📄 Generate PDF Report</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        // Set today's date as default
        document.getElementById('reportDate').valueAsDate = new Date();
        document.getElementById('testDate').valueAsDate = new Date();
        document.getElementById('signatureDate').valueAsDate = new Date();
        
        // Form submission
        document.getElementById('pressureVesselForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            
            // Create a blob and download
            const jsonData = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `PressureVesselReport_${data.jobNumber}_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            alert('✅ Report data saved! In production, this would generate a filled PDF.');
        });
        
        function resetForm() {
            if (confirm('Are you sure you want to clear all form data?')) {
                document.getElementById('pressureVesselForm').reset();
                
                // Reset dates to today
                document.getElementById('reportDate').valueAsDate = new Date();
                document.getElementById('testDate').valueAsDate = new Date();
                document.getElementById('signatureDate').valueAsDate = new Date();
            }
        }
    </script>
</body>
</html>"""
    
    with open('pressure_vessel_form.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Web form generator created: pressure_vessel_form.html")
    print("Open this file in any web browser to fill out inspection reports!")

if __name__ == "__main__":
    print("=" * 60)
    print("Pressure Vessel Inspection Report Generator")
    print("=" * 60)
    print()
    
    # Create the template PDF
    template_file = create_pressure_vessel_template()
    print()
    
    # Create the web form
    create_pressure_vessel_web_form()
    print()
    
    print("=" * 60)
    print("✅ FILES CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("1. Pressure_Vessel_Inspection_Report_TEMPLATE.pdf - Base PDF template")
    print("2. pressure_vessel_form.html - Interactive web form")
    print()
    print("USAGE:")
    print("------")
    print("Open 'pressure_vessel_form.html' in any web browser")
    print("Fill in the form with inspection details")
    print("Click 'Generate PDF Report' to save the data")
    print()