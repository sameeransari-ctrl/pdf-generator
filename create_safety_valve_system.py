#!/usr/bin/env python3
"""
Safety Valve Report Generator with Automatic Tolerance Calculations
This script generates a fillable PDF form for the Safety Valve Report
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
import json
import os

def create_safety_valve_template():
    """Create a fillable PDF template for Safety Valve Report"""
    
    filename = "Safety_Valve_Report_TEMPLATE.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # ============================================================
    # PAGE 1 - COVER PAGE
    # ============================================================
    
    # Header - Company Logo placeholder
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 120, width, 120, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 70, "SAFETY RELIEF VALVE TEST REPORT")
    
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
    y -= 40
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Prepared By:")
    
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Western Air Compliance")
    c.drawString(50, y - 15, "Technician: Glenn Scatchard")
    c.drawString(50, y - 30, "Email: info@westernaircompliance.com.au")
    c.drawString(50, y - 45, "Phone: 0459 851 411")
    
    # Report Details
    y -= 80
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
    # PAGE 2 - MAIN TEST REPORT
    # ============================================================
    
    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 40, "SAFETY RELIEF VALVE TEST REPORT TO AS 1271:2003")
    
    # Main content area
    y = height - 100
    c.setFillColor(colors.black)
    
    # Client Information Section (left column)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Client / Company:")
    c.rect(170, y - 5, 200, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Address:")
    c.rect(170, y - 5, 200, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Test Number:")
    c.rect(170, y - 5, 200, 18, stroke=True, fill=False)
    
    # Right column details
    y_right = height - 100
    c.drawString(400, y_right, "Site:")
    c.rect(470, y_right - 5, 120, 18, stroke=True, fill=False)
    
    y_right -= 25
    c.drawString(400, y_right, "Contact:")
    c.rect(470, y_right - 5, 120, 18, stroke=True, fill=False)
    
    y_right -= 25
    c.drawString(400, y_right, "PO / Reference No:")
    c.rect(470, y_right - 5, 120, 18, stroke=True, fill=False)
    
    y_right -= 25
    c.drawString(400, y_right, "Test Date:")
    c.rect(470, y_right - 5, 120, 18, stroke=True, fill=False)
    
    # Valve Identification Section
    y = height - 220
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Valve Identification")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Size:")
    c.rect(120, y - 5, 120, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Manufacturer:")
    c.rect(120, y - 5, 120, 18, stroke=True, fill=False)
    
    y -= 25
    c.drawString(50, y, "Model:")
    c.rect(120, y - 5, 120, 18, stroke=True, fill=False)
    
    # Right column - Valve details
    y_right = height - 245
    c.drawString(270, y_right, "Discharge Type:")
    c.rect(370, y_right - 5, 100, 18, stroke=True, fill=False)
    
    y_right -= 25
    c.drawString(270, y_right, "Valve Serial No:")
    c.rect(370, y_right - 5, 100, 18, stroke=True, fill=False)
    
    y_right -= 25
    c.drawString(270, y_right, "Blowdown Type:")
    c.rect(370, y_right - 5, 100, 18, stroke=True, fill=False)
    
    # ============================================================
    # CRITICAL SECTION: Set Pressure and Tolerance Calculations
    # ============================================================
    
    y = height - 350
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Set Pressure & Tolerance Calculation")
    c.setFillColor(colors.black)
    
    y -= 30
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Set Pressure (kPa):")
    
    # Highlight the input field with blue background
    c.setFillColor(colors.HexColor('#E7F3FF'))
    c.rect(200, y - 5, 130, 22, fill=True, stroke=True)
    c.setFillColor(colors.black)
    
    # Calculation results - with gray background for calculated fields
    y -= 35
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Lower Tolerance (-3%):")
    c.setFillColor(colors.HexColor('#F0F0F0'))
    c.rect(200, y - 5, 130, 22, fill=True, stroke=True)
    c.setFillColor(colors.black)
    
    y -= 35
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Upper Tolerance (+3%):")
    c.setFillColor(colors.HexColor('#F0F0F0'))
    c.rect(200, y - 5, 130, 22, fill=True, stroke=True)
    c.setFillColor(colors.black)
    
    # Acceptance Criteria
    y -= 50
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Acceptance Criteria & Gauge Details")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Standard: AS 1271-2003 - Safety Valves, Bursting Discs and Other Pressure Relief Devices")
    
    y -= 25
    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Test Gauge ID:")
    c.rect(140, y - 5, 100, 15, stroke=True, fill=False)
    
    c.drawString(270, y, "Gauge Model:")
    c.rect(350, y - 5, 120, 15, stroke=True, fill=False)
    
    y -= 20
    c.drawString(50, y, "Gauge Serial No:")
    c.rect(140, y - 5, 100, 15, stroke=True, fill=False)
    
    c.drawString(270, y, "Recalibration Due:")
    c.rect(380, y - 5, 90, 15, stroke=True, fill=False)
    
    c.showPage()
    
    # ============================================================
    # PAGE 3 - TEST RESULTS
    # ============================================================
    
    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 60, width, 60, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 40, "TEST RESULTS")
    
    y = height - 100
    c.setFillColor(colors.black)
    
    # Final Test Results
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Final Test Results")
    c.setFillColor(colors.black)
    
    y -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Average Final Lift Pressure (kPa):")
    c.rect(260, y - 5, 120, 18, stroke=True, fill=False)
    
    y -= 30
    c.drawString(50, y, "Average Final Reseat Pressure (kPa):")
    c.rect(260, y - 5, 120, 18, stroke=True, fill=False)
    
    y -= 30
    c.drawString(50, y, "Flow Rate (scfm):")
    c.rect(260, y - 5, 120, 18, stroke=True, fill=False)
    
    y -= 30
    c.drawString(50, y, "Blowdown %:")
    c.rect(260, y - 5, 120, 18, stroke=True, fill=False)
    
    c.drawString(400, y, "Allowable: <15%")
    
    # Test Results Summary
    y -= 50
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Test Results:")
    
    y -= 25
    c.setFont("Helvetica", 10)
    checkbox_y = y + 2
    
    # Checkboxes
    c.rect(100, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(120, y, "Leak Test: PASS")
    
    c.rect(250, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(270, y, "Set Pressure Test: PASS")
    
    c.rect(450, checkbox_y, 12, 12, stroke=True, fill=False)
    c.drawString(470, y, "Blowdown %: PASS")
    
    # Overall Result
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Overall Result:")
    
    c.rect(180, y - 5, 80, 25, fill=False, stroke=True)
    c.setFillColor(colors.black)
    
    # Comments Section
    y -= 60
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Comments & Deviations")
    c.setFillColor(colors.black)
    
    y -= 20
    c.rect(50, y - 60, 510, 60, stroke=True, fill=False)
    c.setFont("Helvetica", 9)
    c.drawString(55, y - 10, "Valve has been tested and found to be within the ±3% required tolerance of the marked set pressure")
    
    # Technician Declaration
    y -= 100
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, y, "Technician Declaration")
    c.setFillColor(colors.black)
    
    y -= 25
    c.setFont("Helvetica", 9)
    declaration = """I certify that the safety valve detailed above has been inspected and tested in accordance 
with AS 1271:2003, and that the results recorded are true and correct at the time of inspection."""
    
    lines = declaration.split('\n')
    for line in lines:
        c.drawString(50, y, line.strip())
        y -= 12
    
    y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Technician: Glenn Scatchard")
    
    y -= 30
    c.drawString(50, y, "Signature:")
    c.line(130, y - 5, 300, y - 5)
    
    c.drawString(350, y, "Date:")
    c.line(400, y - 5, 520, y - 5)
    
    # Footer
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, "Western Air Compliance | ABN - 36 280 464 689")
    c.drawString(400, 30, f"Page 3 of 3")
    
    c.save()
    print(f"Template PDF created: {filename}")
    return filename

def create_web_form_generator():
    """Create an HTML form that generates filled PDFs with automatic calculations"""
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Safety Valve Report Generator</title>
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
            font-size: 28px;
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
        textarea {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="date"]:focus,
        input[type="number"]:focus,
        textarea:focus {
            outline: none;
            border-color: #2E75B6;
            box-shadow: 0 0 0 3px rgba(46, 117, 182, 0.1);
        }
        
        input[type="number"].highlight {
            background: #E7F3FF;
            border-color: #2E75B6;
            font-weight: bold;
        }
        
        input[readonly] {
            background: #f5f5f5;
            color: #666;
            cursor: not-allowed;
        }
        
        .calculated-field {
            background: #f0f0f0 !important;
            font-weight: bold;
            color: #2E75B6;
        }
        
        .calc-label {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .calc-badge {
            background: #2E75B6;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: bold;
        }
        
        textarea {
            min-height: 80px;
            resize: vertical;
            font-family: Arial, sans-serif;
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
        
        .info-box {
            background: #E7F3FF;
            border-left: 4px solid #2E75B6;
            padding: 15px;
            margin-top: 20px;
            border-radius: 8px;
        }
        
        .info-box h3 {
            color: #2E75B6;
            margin-bottom: 8px;
            font-size: 16px;
        }
        
        .info-box p {
            color: #555;
            font-size: 14px;
            line-height: 1.6;
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
            <h1>🔧 Safety Valve Report Generator</h1>
            <p>Western Air Compliance | Automatic Tolerance Calculator</p>
        </div>
        
        <div class="form-content">
            <form id="safetyValveForm">
                <!-- Client Information Section -->
                <div class="form-section">
                    <div class="section-title">Client Information</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="clientCompany">Client / Company Name *</label>
                            <input type="text" id="clientCompany" name="clientCompany" required>
                        </div>
                        <div class="form-group">
                            <label for="clientAddress">Address *</label>
                            <input type="text" id="clientAddress" name="clientAddress" required>
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
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="reference">Reference</label>
                            <input type="text" id="reference" name="reference">
                        </div>
                        <div class="form-group">
                            <label for="testNumber">Test Number *</label>
                            <input type="text" id="testNumber" name="testNumber" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="site">Site</label>
                            <input type="text" id="site" name="site">
                        </div>
                        <div class="form-group">
                            <label for="contact">Contact</label>
                            <input type="text" id="contact" name="contact">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="poReference">PO / Reference No</label>
                            <input type="text" id="poReference" name="poReference">
                        </div>
                        <div class="form-group">
                            <label for="testDate">Test Date *</label>
                            <input type="date" id="testDate" name="testDate" required>
                        </div>
                    </div>
                </div>
                
                <!-- Valve Identification Section -->
                <div class="form-section">
                    <div class="section-title">Valve Identification</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="valveSize">Valve Size *</label>
                            <input type="text" id="valveSize" name="valveSize" required>
                        </div>
                        <div class="form-group">
                            <label for="manufacturer">Manufacturer *</label>
                            <input type="text" id="manufacturer" name="manufacturer" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="model">Model *</label>
                            <input type="text" id="model" name="model" required>
                        </div>
                        <div class="form-group">
                            <label for="dischargeType">Discharge Type</label>
                            <input type="text" id="dischargeType" name="dischargeType" value="Atmosphere">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="valveSerialNo">Valve Serial No *</label>
                            <input type="text" id="valveSerialNo" name="valveSerialNo" required>
                        </div>
                        <div class="form-group">
                            <label for="blowdownType">Blowdown Type</label>
                            <input type="text" id="blowdownType" name="blowdownType" value="Non-Adjustable">
                        </div>
                    </div>
                </div>
                
                <!-- Set Pressure & Tolerance Calculation Section -->
                <div class="form-section">
                    <div class="section-title">Set Pressure & Tolerance Calculation</div>
                    
                    <div class="info-box">
                        <h3>📊 Automatic Tolerance Calculator</h3>
                        <p>Enter the Set Pressure value below, and the tolerance range (±3%) will be calculated automatically in real-time.</p>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="setPressure">Set Pressure (kPa) *</label>
                            <input type="number" id="setPressure" name="setPressure" class="highlight" 
                                   step="0.01" min="0" required 
                                   placeholder="Enter set pressure value">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="lowerTolerance" class="calc-label">
                                <span>Lower Tolerance (-3%)</span>
                                <span class="calc-badge">AUTO-CALC</span>
                            </label>
                            <input type="text" id="lowerTolerance" name="lowerTolerance" 
                                   class="calculated-field" readonly 
                                   placeholder="Auto-calculated">
                        </div>
                        <div class="form-group">
                            <label for="upperTolerance" class="calc-label">
                                <span>Upper Tolerance (+3%)</span>
                                <span class="calc-badge">AUTO-CALC</span>
                            </label>
                            <input type="text" id="upperTolerance" name="upperTolerance" 
                                   class="calculated-field" readonly 
                                   placeholder="Auto-calculated">
                        </div>
                    </div>
                </div>
                
                <!-- Gauge Details Section -->
                <div class="form-section">
                    <div class="section-title">Gauge Details</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="testGaugeId">Test Gauge ID</label>
                            <input type="text" id="testGaugeId" name="testGaugeId" value="N/A">
                        </div>
                        <div class="form-group">
                            <label for="gaugeModel">Gauge Model</label>
                            <input type="text" id="gaugeModel" name="gaugeModel" value="Druck DPI104">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="gaugeSerialNo">Gauge Serial No</label>
                            <input type="text" id="gaugeSerialNo" name="gaugeSerialNo" value="6113016">
                        </div>
                        <div class="form-group">
                            <label for="recalibrationDue">Recalibration Due</label>
                            <input type="date" id="recalibrationDue" name="recalibrationDue">
                        </div>
                    </div>
                </div>
                
                <!-- Test Results Section -->
                <div class="form-section">
                    <div class="section-title">Test Results</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="avgLiftPressure">Average Final Lift Pressure (kPa)</label>
                            <input type="number" id="avgLiftPressure" name="avgLiftPressure" step="0.01">
                        </div>
                        <div class="form-group">
                            <label for="avgReseatPressure">Average Final Reseat Pressure (kPa)</label>
                            <input type="number" id="avgReseatPressure" name="avgReseatPressure" step="0.01">
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="flowRate">Flow Rate (scfm)</label>
                            <input type="number" id="flowRate" name="flowRate" step="0.01">
                        </div>
                        <div class="form-group">
                            <label for="blowdownPercent">Blowdown %</label>
                            <input type="number" id="blowdownPercent" name="blowdownPercent" step="0.01">
                        </div>
                    </div>
                </div>
                
                <!-- Comments Section -->
                <div class="form-section">
                    <div class="section-title">Comments & Deviations</div>
                    
                    <div class="form-row single">
                        <div class="form-group">
                            <label for="comments">Comments</label>
                            <textarea id="comments" name="comments" 
                                      placeholder="Valve has been tested and found to be within the ±3% required tolerance of the marked set pressure">Valve has been tested and found to be within the ±3% required tolerance of the marked set pressure</textarea>
                        </div>
                    </div>
                </div>
                
                <!-- Signature Section -->
                <div class="form-section">
                    <div class="section-title">Technician Declaration</div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label for="technicianName">Technician Name</label>
                            <input type="text" id="technicianName" name="technicianName" value="Glenn Scatchard">
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
        // Automatic tolerance calculation
        document.getElementById('setPressure').addEventListener('input', function() {
            const setPressure = parseFloat(this.value);
            
            if (!isNaN(setPressure) && setPressure > 0) {
                const lowerTolerance = (setPressure * 0.97).toFixed(2);
                const upperTolerance = (setPressure * 1.03).toFixed(2);
                
                document.getElementById('lowerTolerance').value = lowerTolerance + ' kPa';
                document.getElementById('upperTolerance').value = upperTolerance + ' kPa';
            } else {
                document.getElementById('lowerTolerance').value = '';
                document.getElementById('upperTolerance').value = '';
            }
        });
        
        // Set today's date as default
        document.getElementById('reportDate').valueAsDate = new Date();
        document.getElementById('testDate').valueAsDate = new Date();
        document.getElementById('signatureDate').valueAsDate = new Date();
        
        // Form submission
        document.getElementById('safetyValveForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Collect form data
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            
            // Add calculated values
            data.lowerToleranceValue = document.getElementById('lowerTolerance').value;
            data.upperToleranceValue = document.getElementById('upperTolerance').value;
            
            // For now, save as JSON (in production, this would generate the PDF)
            const jsonData = JSON.stringify(data, null, 2);
            
            // Create a blob and download
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `SafetyValveReport_${data.jobNumber}_${Date.now()}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            alert('✅ Report data saved! In production, this would generate a filled PDF.\\n\\nTo complete this system, you would need a backend server to generate the actual PDF from this data.');
        });
        
        function resetForm() {
            if (confirm('Are you sure you want to clear all form data?')) {
                document.getElementById('safetyValveForm').reset();
                document.getElementById('lowerTolerance').value = '';
                document.getElementById('upperTolerance').value = '';
                
                // Reset dates to today
                document.getElementById('reportDate').valueAsDate = new Date();
                document.getElementById('testDate').valueAsDate = new Date();
                document.getElementById('signatureDate').valueAsDate = new Date();
            }
        }
    </script>
</body>
</html>"""
    
    with open('safety_valve_form.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Web form generator created: safety_valve_form.html")
    print("Open this file in any web browser to fill out reports with automatic calculations!")

if __name__ == "__main__":
    print("=" * 60)
    print("Safety Valve Report Generator")
    print("=" * 60)
    print()
    
    # Create the template PDF
    template_file = create_safety_valve_template()
    print()
    
    # Create the web form
    create_web_form_generator()
    print()
    
    print("=" * 60)
    print("✅ FILES CREATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("1. Safety_Valve_Report_TEMPLATE.pdf - Base PDF template")
    print("2. safety_valve_form.html - Interactive web form with auto-calculations")
    print()
    print("USAGE:")
    print("------")
    print("Open 'safety_valve_form.html' in any web browser")
    print("Fill in the form - tolerances calculate automatically!")
    print("Click 'Generate PDF Report' to save the data")
    print()