#!/usr/bin/env python3
"""
Test script for PDF generation
Generates sample PDFs and reviews them
"""

import os
import sys
from datetime import datetime

# Test data for Safety Valve
safety_valve_test_data = {
    'clientCompany': 'ABC Manufacturing Pty Ltd',
    'clientAddress': '123 Industrial Road, Perth WA 6000',
    'reportDate': datetime.now().strftime('%Y-%m-%d'),
    'jobNumber': 'WAC-2024-001',
    'reference': 'VALVE-INSPECT-001',
    'testNumber': 'TV-001',
    'site': 'Main Plant',
    'contact': 'John Smith',
    'poReference': 'PO-12345',
    'testDate': datetime.now().strftime('%Y-%m-%d'),
    'valveSize': '2"',
    'manufacturer': 'Leser',
    'model': 'Type 441',
    'dischargeType': 'Atmosphere',
    'valveSerialNo': 'SN-987654321',
    'blowdownType': 'Non-Adjustable',
    'setPressure': '1000',
    'lowerTolerance': '970.00 kPa',
    'upperTolerance': '1030.00 kPa',
    'testGaugeId': 'N/A',
    'gaugeModel': 'Druck DPI104',
    'gaugeSerialNo': '6113016',
    'recalibrationDue': '2025-03-30',
    'avgLiftPressure': '995',
    'avgReseatPressure': '920',
    'flowRate': '450',
    'blowdownPercent': '7.5',
    'comments': 'Valve has been tested and found to be within the +/- 3% required tolerance of the marked set pressure. All test results are satisfactory.',
    'technicianName': 'Glenn Scatchard',
    'signatureDate': datetime.now().strftime('%Y-%m-%d')
}

# Test data for Pressure Vessel
pressure_vessel_test_data = {
    'clientCompany': 'XYZ Industries Ltd',
    'clientAddress': '456 Factory Lane, Perth WA 6000',
    'site': 'Site B',
    'contact': 'Jane Doe',
    'manufacturer': 'Air Receiver Co',
    'poReference': 'PO-67890',
    'model': 'AR-500',
    'assetNo': 'ASSET-001',
    'serialNo': 'SN-123456789',
    'testDate': datetime.now().strftime('%Y-%m-%d'),
    'testNumber': 'TV-002',
    'unitType': 'Air Receiver',
    'reportDate': datetime.now().strftime('%Y-%m-%d'),
    'jobNumber': 'WAC-2024-002',
    'vesselManufacturer': 'Air Receiver Co',
    'vesselSerialNo': 'SN-123456789',
    'manufacturedDate': '2020-01-15',
    'designCode': 'AS 1210-3',
    'location': 'Itinerant',
    'corrosionAllowance': '1.0',
    'vesselType': 'Vertical',
    'tankCapacity': '500L',
    'designRegNo': 'DR-12345',
    'hydrostaticTestDate': '2020-02-01',
    'worksafeRegNo': 'WR-98765',
    'designTemp': '150',
    'commissioningDate': '2020-03-01',
    'ambientTemp': '25',
    'designPressure': '1200',
    'shellLength': '1200',
    'operatingPressure': '1000',
    'shellDiameter': '600',
    'testPressure': '1320',
    'hazardLevel': 'Level C',
    'visualInspection': 'PASS',
    'pressureTest': 'PASS',
    'safetyDevices': 'PASS',
    'overallResult': 'PASS',
    'comments': 'Vessel inspected and found to be in satisfactory condition. No defects noted.',
    'recommendations': 'Next inspection due in 12 months.',
    'nextInspectionDue': '2025-03-30',
    'inspectorName': 'Glenn Scatchard',
    'signatureDate': datetime.now().strftime('%Y-%m-%d')
}


def generate_safety_valve_pdf(data, output_path):
    """Generate Safety Valve PDF from scratch with corrected coordinates"""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 100, width, 100, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 55, "SAFETY RELIEF VALVE TEST REPORT")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, height - 80, "Western Air Compliance | Inspection • Testing • Certification")

    # Page 1 - Cover
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 160, "Prepared For:")
    c.setFont("Helvetica", 10)
    c.drawString(155, height - 185, data.get('clientCompany', ''))
    c.drawString(155, height - 210, data.get('clientAddress', ''))
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, height - 330, "Report Details:")
    c.setFont("Helvetica", 10)
    c.drawString(155, height - 355, data.get('reportDate', ''))
    c.drawString(155, height - 380, data.get('jobNumber', ''))
    c.drawString(155, height - 405, data.get('reference', ''))

    # Page 2
    c.showPage()
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 50, width, 50, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - 30, "SAFETY RELIEF VALVE TEST REPORT TO AS 1271:2003")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(175, height - 100, data.get('clientCompany', ''))
    c.drawString(175, height - 125, data.get('clientAddress', ''))
    c.drawString(175, height - 150, data.get('testNumber', ''))
    
    c.drawString(475, height - 100, data.get('site', ''))
    c.drawString(475, height - 125, data.get('contact', ''))
    c.drawString(475, height - 150, data.get('poReference', ''))
    c.drawString(475, height - 175, data.get('testDate', ''))

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, height - 220, "Valve Identification")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(125, height - 245, data.get('valveSize', ''))
    c.drawString(125, height - 270, data.get('manufacturer', ''))
    c.drawString(125, height - 295, data.get('model', ''))
    
    c.drawString(375, height - 245, data.get('dischargeType', ''))
    c.drawString(375, height - 270, data.get('valveSerialNo', ''))
    c.drawString(375, height - 295, data.get('blowdownType', ''))

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.drawString(50, height - 350, "Set Pressure & Tolerance Calculation")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(205, height - 380, data.get('setPressure', '') + ' kPa')
    c.setFont("Helvetica", 10)
    c.drawString(205, height - 415, data.get('lowerTolerance', ''))
    c.drawString(205, height - 450, data.get('upperTolerance', ''))

    # Page 3
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 40, "TEST RESULTS")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(265, height - 130, data.get('avgLiftPressure', '') + ' kPa')
    c.drawString(265, height - 160, data.get('avgReseatPressure', '') + ' kPa')
    c.drawString(265, height - 190, data.get('flowRate', '') + ' scfm')
    c.drawString(265, height - 220, data.get('blowdownPercent', '') + '%')

    c.setFont("Helvetica-Bold", 14)
    c.drawString(195, height - 302, "PASS")

    c.setFont("Helvetica", 9)
    comments = data.get('comments', '')
    y = height - 385
    words = comments.split()
    line = ''
    for word in words:
        if c.stringWidth(line + ' ' + word) < 500:
            line += ' ' + word if line else word
        else:
            c.drawString(55, y, line)
            y -= 12
            line = word
    if line:
        c.drawString(55, y, line)

    c.setFont("Helvetica-Bold", 10)
    c.drawString(135, height - 515, data.get('technicianName', ''))
    c.drawString(405, height - 545, data.get('signatureDate', ''))

    c.save()
    print(f"[OK] Safety Valve PDF generated: {output_path}")


def generate_pressure_vessel_pdf(data, output_path):
    """Generate Pressure Vessel PDF from scratch with corrected coordinates"""
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors

    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Header
    c.setFillColor(colors.HexColor('#2E75B6'))
    c.rect(0, height - 100, width, 100, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 55, "PRESSURE VESSEL INSPECTION REPORT")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, height - 80, "Western Air Compliance | AS/NZS 3788:2024 Compliance")

    # Page 1
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(155, height - 185, data.get('clientCompany', ''))
    c.drawString(155, height - 210, data.get('clientAddress', ''))
    c.drawString(155, height - 355, data.get('reportDate', ''))
    c.drawString(155, height - 380, data.get('jobNumber', ''))

    # Page 2
    c.showPage()
    c.setFont("Helvetica", 10)
    c.drawString(175, height - 125, data.get('clientCompany', ''))
    c.drawString(435, height - 125, data.get('site', ''))
    c.drawString(175, height - 150, data.get('clientAddress', ''))
    c.drawString(435, height - 150, data.get('contact', ''))
    c.drawString(175, height - 175, data.get('manufacturer', ''))
    c.drawString(435, height - 175, data.get('poReference', ''))
    c.drawString(175, height - 200, data.get('model', ''))
    c.drawString(435, height - 200, data.get('assetNo', ''))
    c.drawString(175, height - 225, data.get('serialNo', ''))
    c.drawString(435, height - 225, data.get('testDate', ''))
    c.drawString(175, height - 250, data.get('testNumber', ''))
    c.drawString(435, height - 250, data.get('unitType', ''))

    # Page 3
    c.showPage()
    c.setFont("Helvetica", 10)
    c.drawString(205, height - 125, data.get('vesselType', ''))
    c.drawString(465, height - 125, data.get('tankCapacity', ''))
    c.drawString(205, height - 225, data.get('designPressure', ''))
    c.drawString(465, height - 225, data.get('shellLength', ''))
    c.drawString(205, height - 250, data.get('operatingPressure', ''))
    c.drawString(465, height - 250, data.get('shellDiameter', ''))
    c.drawString(205, height - 300, data.get('hazardLevel', ''))

    c.setFont("Helvetica-Bold", 14)
    c.drawString(195, height - 462, "PASS")

    # Page 4
    c.showPage()
    c.setFont("Helvetica", 9)
    c.drawString(55, height - 135, data.get('comments', '')[:100])
    c.drawString(55, height - 315, data.get('recommendations', '')[:100])
    c.drawString(205, height - 380, data.get('nextInspectionDue', ''))
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(135, height - 515, data.get('inspectorName', ''))
    c.drawString(405, height - 545, data.get('signatureDate', ''))

    c.save()
    print(f"[OK] Pressure Vessel PDF generated: {output_path}")


def main():
    print("=" * 60)
    print("Western Air Compliance - PDF Generation Test")
    print("=" * 60)
    print()

    # Create output directory
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)

    # Generate Safety Valve PDF
    print("Generating Safety Valve PDF...")
    sv_path = os.path.join(output_dir, "TEST_Safety_Valve_Report.pdf")
    try:
        generate_safety_valve_pdf(safety_valve_test_data, sv_path)
        print(f"  File size: {os.path.getsize(sv_path)} bytes")
    except Exception as e:
        print(f"  ERROR: {e}")
    print()

    # Generate Pressure Vessel PDF
    print("Generating Pressure Vessel PDF...")
    pv_path = os.path.join(output_dir, "TEST_Pressure_Vessel_Report.pdf")
    try:
        generate_pressure_vessel_pdf(pressure_vessel_test_data, pv_path)
        print(f"  File size: {os.path.getsize(pv_path)} bytes")
    except Exception as e:
        print(f"  ERROR: {e}")
    print()

    print("=" * 60)
    print("Test complete! PDFs generated in 'test_output/' folder")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Open the PDF files to review the output")
    print("2. Check formatting, layout, and content")
    print("3. Report any issues for fixing")


if __name__ == "__main__":
    main()
