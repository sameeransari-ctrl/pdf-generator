#!/usr/bin/env python3
"""
Western Air Compliance - Desktop PDF Report Generator
A standalone desktop application for generating filled PDF reports

Features:
- Works completely offline (no internet required)
- Generates professional PDF reports locally
- Automatic ±3% tolerance calculator for Safety Valve reports
- Both Safety Valve and Pressure Vessel report types
- Built with Python tkinter (no additional dependencies for GUI)

Requirements:
- pip install pypdf reportlab
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import json
import os
import sys

from fill_templates import (
    generate_pressure_vessel_pdf as generate_pressure_vessel_template_pdf,
    generate_safety_valve_pdf as generate_safety_valve_template_pdf,
    map_pressure_vessel_form_data,
    map_safety_valve_form_data,
)

# PDF Libraries
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO


class PDFReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Western Air Compliance - PDF Report Generator")
        self.root.geometry("1100x850")
        self.root.minsize(1000, 750)

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color Palette
        self.primary_blue = '#2E75B6'
        self.light_blue = '#E7F3FF'
        self.bg_color = '#F8F9FA'
        
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Header.TFrame', background=self.primary_blue)
        self.style.configure('Header.TLabel', background=self.primary_blue, foreground='white', font=('Segoe UI', 18, 'bold'))
        self.style.configure('Section.TLabelframe', background=self.bg_color, font=('Segoe UI', 11, 'bold'))
        self.style.configure('Section.TLabelframe.Label', background=self.bg_color, foreground=self.primary_blue)
        self.style.configure('TLabel', background=self.bg_color, font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Primary.TButton', foreground='white', background=self.primary_blue)
        
        # Main container
        self.main_container = ttk.Frame(root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        self.create_header()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create tabs
        self.safety_valve_tab = ttk.Frame(self.notebook)
        self.pressure_vessel_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.safety_valve_tab, text=" 🔧  Safety Valve Report ")
        self.notebook.add(self.pressure_vessel_tab, text=" ⚙️  Pressure Vessel Report ")

        # Build forms
        self.build_safety_valve_form()
        self.build_pressure_vessel_form()

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.main_container, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, font=('Segoe UI', 9))
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(0, 10))

    def create_header(self):
        """Create application header"""
        header = ttk.Frame(self.main_container, style='Header.TFrame')
        header.pack(fill=tk.X)

        title = ttk.Label(header, text="WESTERN AIR COMPLIANCE",
                         style='Header.TLabel')
        title.pack(pady=(20, 5))

        subtitle = ttk.Label(header, text="OFFLINE PDF REPORT GENERATOR",
                            background=self.primary_blue, foreground='white', font=('Segoe UI', 10, 'bold'))
        subtitle.pack(pady=(0, 20))

    def build_safety_valve_form(self):
        """Build the Safety Valve report form"""
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(self.safety_valve_tab)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.sv_canvas = tk.Canvas(canvas_frame, yscrollcommand=scrollbar.set, highlightthickness=0, background=self.bg_color)
        self.sv_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.sv_canvas.yview)

        # Frame for form content
        form_frame = ttk.Frame(self.sv_canvas)
        self.sv_canvas.create_window((0, 0), window=form_frame, anchor=tk.NW, width=1050)

        # Store variables
        self.sv_vars = {}

        # Client Information Section
        client_frame = ttk.LabelFrame(form_frame, text="Client Information", padding=15, style='Section.TLabelframe')
        client_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_form_row(client_frame, [
            ('clientCompany', 'Client / Company Name *', 'entry', True),
            ('clientAddress', 'Address *', 'entry', True)
        ])
        self.create_form_row(client_frame, [
            ('reportDate', 'Report Date *', 'date', True),
            ('jobNumber', 'Job Number *', 'entry', True)
        ])
        self.create_form_row(client_frame, [
            ('reference', 'Reference', 'entry', False),
            ('testNumber', 'Test Number *', 'entry', True)
        ])
        self.create_form_row(client_frame, [
            ('site', 'Site', 'entry', False),
            ('contact', 'Contact', 'entry', False)
        ])
        self.create_form_row(client_frame, [
            ('poReference', 'PO / Reference No', 'entry', False),
            ('testDate', 'Test Date *', 'date', True)
        ])

        # Valve Identification Section
        valve_frame = ttk.LabelFrame(form_frame, text="Valve Identification", padding=15, style='Section.TLabelframe')
        valve_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_form_row(valve_frame, [
            ('valveSize', 'Valve Size *', 'entry', True),
            ('manufacturer', 'Manufacturer *', 'entry', True)
        ])
        self.create_form_row(valve_frame, [
            ('model', 'Model *', 'entry', True),
            ('dischargeType', 'Discharge Type', 'entry', False, 'Atmosphere')
        ])
        self.create_form_row(valve_frame, [
            ('valveSerialNo', 'Valve Serial No *', 'entry', True),
            ('blowdownType', 'Blowdown Type', 'entry', False, 'Non-Adjustable')
        ])

        # Set Pressure & Tolerance Section
        pressure_frame = ttk.LabelFrame(form_frame, text="Set Pressure & Tolerance Calculation", padding=15, style='Section.TLabelframe')
        pressure_frame.pack(fill=tk.X, padx=20, pady=10)

        # Info label
        info_label = ttk.Label(pressure_frame,
            text="📊 Automatic Tolerance Calculator: Enter Set Pressure and tolerances calculate automatically (+/- 3%)",
            font=('Segoe UI', 9, 'italic'), foreground=self.primary_blue)
        info_label.pack(anchor=tk.W, pady=(0, 10))

        self.create_form_row(pressure_frame, [
            ('setPressure', 'Set Pressure (kPa) *', 'number', True)
        ])

        # Bind calculation
        self.sv_vars['setPressure'].trace_add('write', self.calculate_tolerance)

        self.create_form_row(pressure_frame, [
            ('lowerTolerance', 'Lower Tolerance (-3%)', 'calc', False),
            ('upperTolerance', 'Upper Tolerance (+3%)', 'calc', False)
        ])

        # Gauge Details Section
        gauge_frame = ttk.LabelFrame(form_frame, text="Gauge Details", padding=15, style='Section.TLabelframe')
        gauge_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_form_row(gauge_frame, [
            ('testGaugeId', 'Test Gauge ID', 'entry', False, 'N/A'),
            ('gaugeModel', 'Gauge Model', 'entry', False, 'Druck DPI104')
        ])
        self.create_form_row(gauge_frame, [
            ('gaugeSerialNo', 'Gauge Serial No', 'entry', False, '6113016'),
            ('recalibrationDue', 'Recalibration Due', 'date', False)
        ])

        # Test Results Section
        results_frame = ttk.LabelFrame(form_frame, text="Test Results", padding=15, style='Section.TLabelframe')
        results_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_form_row(results_frame, [
            ('avgLiftPressure', 'Average Final Lift Pressure (kPa)', 'number', False),
            ('avgReseatPressure', 'Average Final Reseat Pressure (kPa)', 'number', False)
        ])
        self.create_form_row(results_frame, [
            ('flowRate', 'Flow Rate (scfm)', 'number', False),
            ('blowdownPercent', 'Blowdown %', 'number', False)
        ])

        # Test Pass/Fail
        self.create_radio_row_sv(results_frame, 'leakTest', 'Leak Test', ['PASS', 'FAIL'], default='PASS')
        self.create_radio_row_sv(results_frame, 'setPressureTest', 'Set Pressure Test', ['PASS', 'FAIL'], default='PASS')
        self.create_radio_row_sv(results_frame, 'blowdownTest', 'Blowdown % Test', ['PASS', 'FAIL'], default='PASS')
        self.create_radio_row_sv(results_frame, 'overallResult', 'Overall Result', ['PASS', 'FAIL'], default='PASS')

        # Comments Section
        comments_frame = ttk.LabelFrame(form_frame, text="Comments & Deviations", padding=15, style='Section.TLabelframe')
        comments_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_text_area(comments_frame, 'comments', 'Comments',
            'Valve has been tested and found to be within the +/- 3% required tolerance of the marked set pressure')

        # Signature Section
        sig_frame = ttk.LabelFrame(form_frame, text="Technician Declaration", padding=15, style='Section.TLabelframe')
        sig_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_form_row(sig_frame, [
            ('technicianName', 'Technician Name', 'entry', False, 'Glenn Scatchard'),
            ('signatureDate', 'Signature Date', 'date', False)
        ])

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, padx=20, pady=25)

        ttk.Button(btn_frame, text="Clear Form", command=self.clear_safety_valve).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate PDF Report", command=self.generate_safety_valve_pdf, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save as JSON", command=self.save_safety_valve_json).pack(side=tk.LEFT, padx=5)

        # Set default dates
        self.set_default_dates(['reportDate', 'testDate', 'signatureDate'])

        # Update scroll region
        form_frame.update_idletasks()
        self.sv_canvas.config(scrollregion=self.sv_canvas.bbox('all'))

    def build_pressure_vessel_form(self):
        """Build the Pressure Vessel report form"""
        # Create canvas with scrollbar
        canvas_frame = ttk.Frame(self.pressure_vessel_tab)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(canvas_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.pv_canvas = tk.Canvas(canvas_frame, yscrollcommand=scrollbar.set, highlightthickness=0, background=self.bg_color)
        self.pv_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.pv_canvas.yview)

        # Frame for form content
        form_frame = ttk.Frame(self.pv_canvas)
        self.pv_canvas.create_window((0, 0), window=form_frame, anchor=tk.NW, width=1050)

        # Store variables
        self.pv_vars = {}

        # Client Information Section
        client_frame = ttk.LabelFrame(form_frame, text="Client & Equipment Details", padding=15, style='Section.TLabelframe')
        client_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_pv_form_row(client_frame, [
            ('clientCompany', 'Client / Company Name *', 'entry', True),
            ('site', 'Site', 'entry', False)
        ])
        self.create_pv_form_row(client_frame, [
            ('clientAddress', 'Address *', 'entry', True),
            ('contact', 'Contact', 'entry', False)
        ])
        self.create_pv_form_row(client_frame, [
            ('manufacturer', 'Manufacturer *', 'entry', True),
            ('poReference', 'PO / Reference No', 'entry', False)
        ])
        self.create_pv_form_row(client_frame, [
            ('model', 'Model *', 'entry', True),
            ('assetNo', 'Asset No', 'entry', False)
        ])
        self.create_pv_form_row(client_frame, [
            ('serialNo', 'Serial No *', 'entry', True),
            ('testDate', 'Test Date *', 'date', True)
        ])
        self.create_pv_form_row(client_frame, [
            ('testNumber', 'Test Number *', 'entry', True),
            ('unitType', 'Unit Type', 'entry', False)
        ])
        self.create_pv_form_row(client_frame, [
            ('reportDate', 'Report Date *', 'date', True),
            ('jobNumber', 'Job Number *', 'entry', True)
        ])

        # Vessel Details Section
        vessel_frame = ttk.LabelFrame(form_frame, text="Vessel Details", padding=15, style='Section.TLabelframe')
        vessel_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_pv_form_row(vessel_frame, [
            ('vesselManufacturer', 'Manufacturer', 'entry', False),
            ('vesselSerialNo', 'Serial No', 'entry', False)
        ])
        self.create_pv_form_row(vessel_frame, [
            ('manufacturedDate', 'Manufactured Date', 'date', False),
            ('designCode', 'Design Code', 'entry', False, 'AS 1210-3')
        ])
        self.create_pv_form_row(vessel_frame, [
            ('location', 'Location', 'entry', False, 'Itinerant'),
            ('corrosionAllowance', 'Corrosion Allowance (mm)', 'number', False)
        ])

        # Design Information Section
        design_frame = ttk.LabelFrame(form_frame, text="Pressure Vessel Design Information", padding=15, style='Section.TLabelframe')
        design_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_pv_form_row(design_frame, [
            ('vesselType', 'Type', 'entry', False),
            ('tankCapacity', 'Tank Capacity', 'entry', False)
        ])
        self.create_pv_form_row(design_frame, [
            ('designRegNo', 'Design Registration No', 'entry', False),
            ('hydrostaticTestDate', 'Hydrostatic Test Date', 'date', False)
        ])
        self.create_pv_form_row(design_frame, [
            ('worksafeRegNo', 'WorkSafe Registration No', 'entry', False),
            ('designTemp', 'Design Temperature (°C)', 'number', False)
        ])
        self.create_pv_form_row(design_frame, [
            ('commissioningDate', 'Commissioning Date', 'date', False),
            ('ambientTemp', 'Ambient Air Temperature (°C)', 'number', False)
        ])
        self.create_pv_form_row(design_frame, [
            ('designPressure', 'Design Pressure (kPa) *', 'number', True),
            ('shellLength', 'Shell Length (mm)', 'number', False)
        ])
        self.create_pv_form_row(design_frame, [
            ('operatingPressure', 'Operating Pressure (kPa) *', 'number', True),
            ('shellDiameter', 'Shell Diameter (mm)', 'number', False)
        ])
        self.create_pv_form_row(design_frame, [
            ('testPressure', 'Test Pressure (kPa)', 'number', False),
            ('hazardLevel', 'Hazard Level (AS/NZS 3788:2024)', 'combo', False, ['', 'Level A', 'Level B', 'Level C', 'Level D', 'Level E'])
        ])

        # Inspection Results Section
        inspect_frame = ttk.LabelFrame(form_frame, text="Inspection Results", padding=15, style='Section.TLabelframe')
        inspect_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_radio_row(inspect_frame, 'visualInspection', 'Visual Inspection', ['PASS', 'FAIL'], default='PASS')
        self.create_radio_row(inspect_frame, 'pressureTest', 'Pressure Test', ['PASS', 'FAIL'], default='PASS')
        self.create_radio_row(inspect_frame, 'safetyDevices', 'Safety Devices', ['PASS', 'FAIL'], default='PASS')
        self.create_radio_row(inspect_frame, 'overallResult', 'Overall Result', ['PASS', 'FAIL'], default='PASS')

        # Detailed Inspection Data Section
        detail_frame = ttk.LabelFrame(form_frame, text="Detailed Inspection Data", padding=15, style='Section.TLabelframe')
        detail_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_pv_form_row(detail_frame, [
            ('inspectionType', 'Inspection Type', 'combo', False,
             ['', 'External In-Service Inspection', 'Internal In-Service Inspection', 'Commissioning / Initial Inspection'])
        ])
        self.create_pv_form_row(detail_frame, [
            ('lhsLidSpec', 'LHS/Lid Spec (mm)', 'entry', False),
            ('lhsLidActual', 'LHS/Lid Actual (mm)', 'entry', False)
        ])
        self.create_pv_form_row(detail_frame, [
            ('rhsBaseSpec', 'RHS/Base Spec (mm)', 'entry', False),
            ('rhsBaseActual', 'RHS/Base Actual (mm)', 'entry', False)
        ])
        self.create_pv_form_row(detail_frame, [
            ('shellSpec', 'Shell Spec (mm)', 'entry', False),
            ('shellActual', 'Shell Actual (mm)', 'entry', False)
        ])
        self.create_pv_form_row(detail_frame, [
            ('externalSurfaceCondition', 'External Surface Condition', 'combo', False, ['', 'Good', 'Fair', 'Poor']),
            ('externalSurfaceComments', 'External Surface Comments', 'entry', False, 'Satisfactory')
        ])
        self.create_pv_form_row(detail_frame, [
            ('internalSurfaceCondition', 'Internal Surface Condition', 'combo', False, ['', 'Good', 'Fair', 'Poor']),
            ('internalSurfaceComments', 'Internal Surface Comments', 'entry', False, 'Satisfactory')
        ])
        self.create_pv_form_row(detail_frame, [
            ('corrosionObserved', 'Corrosion / Pitting Observed', 'combo', False, ['', 'Yes', 'No']),
            ('corrosionLocation', 'Corrosion Location', 'entry', False)
        ])
        self.create_pv_form_row(detail_frame, [
            ('dentsDeformation', 'Dents / Deformation', 'combo', False, ['', 'Yes', 'No']),
            ('dentsDetails', 'Dents Details', 'entry', False)
        ])
        self.create_pv_form_row(detail_frame, [
            ('pressureGaugeWorking', 'Pressure Gauge Working', 'entry', False, 'Not Observed'),
            ('paintCoatingCondition', 'Paint / Coating Condition', 'combo', False, ['', 'Good', 'Fair', 'Poor'])
        ])
        self.create_pv_form_row(detail_frame, [
            ('baseMountsCondition', 'Base / Mounts / Supports', 'combo', False, ['', 'Good', 'Fair', 'Poor']),
            ('baseMountsComments', 'Base / Mounts Comments', 'entry', False, 'Satisfactory')
        ])
        self.create_pv_form_row(detail_frame, [
            ('nameplateStatus', 'Nameplate Status', 'combo', False, ['', 'Present', 'Missing', 'Not Legible']),
            ('drainValveOperation', 'Drain Valve Operation', 'combo', False, ['', 'OK', 'Not Working', 'N/A'])
        ])
        self.create_pv_form_row(detail_frame, [
            ('safetyValveFitted', 'Safety Valve Fitted', 'combo', False, ['', 'Yes', 'No']),
            ('safetyValveReportNo', 'Safety Valve Report No', 'entry', False)
        ])
        self.create_pv_text_area(detail_frame, 'safetyValveDetails', 'Safety Valve Details', '')
        self.create_pv_form_row(detail_frame, [
            ('overallVesselCondition', 'Overall Vessel Condition', 'combo', False,
             ['', 'Good', 'Fair', 'Requires Monitoring', 'Unsafe / Remove from Service']),
            ('designReportsSighted', 'Design Reports Sighted', 'entry', False)
        ])
        self.create_pv_text_area(detail_frame, 'associatedDocumentation', 'Associated Documentation', '')

        # Comments Section
        comments_frame = ttk.LabelFrame(form_frame, text="Comments & Recommendations", padding=15, style='Section.TLabelframe')
        comments_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_pv_text_area(comments_frame, 'comments', 'Inspection Comments & Observations', '')
        self.create_pv_text_area(comments_frame, 'recommendations', 'Recommendations', '')

        self.create_pv_form_row(comments_frame, [
            ('nextInspectionDue', 'Next Inspection Due', 'date', False)
        ])

        # Signature Section
        sig_frame = ttk.LabelFrame(form_frame, text="Inspector Declaration", padding=15, style='Section.TLabelframe')
        sig_frame.pack(fill=tk.X, padx=20, pady=10)

        self.create_pv_form_row(sig_frame, [
            ('inspectorName', 'Inspector Name', 'entry', False, 'Glenn Scatchard'),
            ('signatureDate', 'Signature Date', 'date', False)
        ])

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.pack(fill=tk.X, padx=20, pady=25)

        ttk.Button(btn_frame, text="Clear Form", command=self.clear_pressure_vessel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate PDF Report", command=self.generate_pressure_vessel_pdf, style='Primary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Save as JSON", command=self.save_pressure_vessel_json).pack(side=tk.LEFT, padx=5)

        # Set default dates
        self.set_pv_default_dates(['reportDate', 'testDate', 'signatureDate'])

        # Update scroll region
        form_frame.update_idletasks()
        self.pv_canvas.config(scrollregion=self.pv_canvas.bbox('all'))

    def create_form_row(self, parent, fields):
        """Create a row of form fields for Safety Valve form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        for i, (name, label, field_type, required, *default) in enumerate(fields):
            container = ttk.Frame(frame)
            container.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            
            # Label
            lbl = ttk.Label(container, text=label, anchor=tk.W)
            lbl.pack(fill=tk.X)

            # Field
            if field_type == 'entry':
                var = tk.StringVar(value=default[0] if default else '')
                entry = ttk.Entry(container, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                self.sv_vars[name] = var
            elif field_type == 'date':
                var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
                entry = ttk.Entry(container, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                self.sv_vars[name] = var
            elif field_type == 'number':
                var = tk.StringVar()
                entry = ttk.Entry(container, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                self.sv_vars[name] = var
            elif field_type == 'calc':
                var = tk.StringVar(value='Auto-calculated')
                entry = ttk.Entry(container, textvariable=var, state='readonly')
                entry.pack(fill=tk.X, pady=(2, 0))
                self.sv_vars[name] = var

    def create_pv_form_row(self, parent, fields):
        """Create a row of form fields for Pressure Vessel form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)

        for i, (name, label, field_type, required, *default) in enumerate(fields):
            container = ttk.Frame(frame)
            container.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            
            # Label
            lbl = ttk.Label(container, text=label, anchor=tk.W)
            lbl.pack(fill=tk.X)

            # Field
            if field_type == 'entry':
                var = tk.StringVar(value=default[0] if default else '')
                entry = ttk.Entry(container, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                self.pv_vars[name] = var
            elif field_type == 'date':
                var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
                entry = ttk.Entry(container, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                self.pv_vars[name] = var
            elif field_type == 'number':
                var = tk.StringVar()
                entry = ttk.Entry(container, textvariable=var)
                entry.pack(fill=tk.X, pady=(2, 0))
                self.pv_vars[name] = var
            elif field_type == 'combo':
                var = tk.StringVar(value=default[0][0] if default else '')
                combo = ttk.Combobox(container, textvariable=var, values=default[0] if default else [])
                combo.pack(fill=tk.X, pady=(2, 0))
                self.pv_vars[name] = var

    def create_text_area(self, parent, name, label, default=''):
        """Create a text area for Safety Valve form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=3)

        lbl = ttk.Label(frame, text=label, anchor=tk.W)
        lbl.pack(anchor=tk.W, padx=10)

        text_widget = tk.Text(frame, height=4, width=80, wrap=tk.WORD, font=('Segoe UI', 10))
        text_widget.pack(fill=tk.X, padx=10, pady=5)
        text_widget.insert('1.0', default)

        self.sv_vars[name] = text_widget

    def create_pv_text_area(self, parent, name, label, default=''):
        """Create a text area for Pressure Vessel form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=3)

        lbl = ttk.Label(frame, text=label, anchor=tk.W)
        lbl.pack(anchor=tk.W, padx=10)

        text_widget = tk.Text(frame, height=3, width=80, wrap=tk.WORD, font=('Segoe UI', 10))
        text_widget.pack(fill=tk.X, padx=10, pady=5)
        text_widget.insert('1.0', default)

        self.pv_vars[name] = text_widget

    def create_radio_row(self, parent, name, label, options, default=None):
        """Create radio button row for Pressure Vessel form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=8)

        lbl = ttk.Label(frame, text=label, width=25, anchor=tk.W)
        lbl.pack(side=tk.LEFT, padx=10)

        var = tk.StringVar(value=default if default else '')
        self.pv_vars[name] = var

        for option in options:
            rb = ttk.Radiobutton(frame, text=option, variable=var, value=option)
            rb.pack(side=tk.LEFT, padx=15)

    def create_radio_row_sv(self, parent, name, label, options, default=None):
        """Create radio button row for Safety Valve form"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=8)

        lbl = ttk.Label(frame, text=label, width=25, anchor=tk.W)
        lbl.pack(side=tk.LEFT, padx=10)

        var = tk.StringVar(value=default if default else '')
        self.sv_vars[name] = var

        for option in options:
            rb = ttk.Radiobutton(frame, text=option, variable=var, value=option)
            rb.pack(side=tk.LEFT, padx=15)

    def calculate_tolerance(self, *args):
        """Calculate ±3% tolerance for Safety Valve"""
        try:
            val_str = self.sv_vars['setPressure'].get().strip()
            if not val_str:
                self.sv_vars['lowerTolerance'].set('Auto-calculated')
                self.sv_vars['upperTolerance'].set('Auto-calculated')
                return
                
            set_pressure = float(val_str)
            if set_pressure > 0:
                lower = set_pressure * 0.97
                upper = set_pressure * 1.03
                self.sv_vars['lowerTolerance'].set(f"{lower:.2f} kPa")
                self.sv_vars['upperTolerance'].set(f"{upper:.2f} kPa")
            else:
                self.sv_vars['lowerTolerance'].set('Auto-calculated')
                self.sv_vars['upperTolerance'].set('Auto-calculated')
        except ValueError:
            self.sv_vars['lowerTolerance'].set('Auto-calculated')
            self.sv_vars['upperTolerance'].set('Auto-calculated')

    def set_default_dates(self, date_fields):
        """Set default dates for Safety Valve form"""
        today = datetime.now().strftime('%Y-%m-%d')
        for field in date_fields:
            if field in self.sv_vars:
                self.sv_vars[field].set(today)

    def set_pv_default_dates(self, date_fields):
        """Set default dates for Pressure Vessel form"""
        today = datetime.now().strftime('%Y-%m-%d')
        for field in date_fields:
            if field in self.pv_vars:
                self.pv_vars[field].set(today)

    def clear_safety_valve(self):
        """Clear Safety Valve form"""
        if messagebox.askyesno("Confirm", "Clear all Safety Valve form data?"):
            for name, var in self.sv_vars.items():
                if isinstance(var, tk.Text):
                    if name == 'comments':
                        var.delete('1.0', tk.END)
                        var.insert('1.0', 'Valve has been tested and found to be within the +/- 3% required tolerance of the marked set pressure')
                    else:
                        var.delete('1.0', tk.END)
                elif 'Tolerance' in name:
                    var.set('Auto-calculated')
                elif 'Date' in name:
                    var.set(datetime.now().strftime('%Y-%m-%d'))
                elif name in ['dischargeType']:
                    var.set('Atmosphere')
                elif name in ['blowdownType']:
                    var.set('Non-Adjustable')
                elif name in ['technicianName']:
                    var.set('Glenn Scatchard')
                elif name in ['testGaugeId']:
                    var.set('N/A')
                elif name in ['gaugeModel']:
                    var.set('Druck DPI104')
                elif name in ['gaugeSerialNo']:
                    var.set('6113016')
                elif name in ['leakTest', 'setPressureTest', 'blowdownTest', 'overallResult']:
                    var.set('PASS')
                else:
                    var.set('')

    def clear_pressure_vessel(self):
        """Clear Pressure Vessel form"""
        if messagebox.askyesno("Confirm", "Clear all Pressure Vessel form data?"):
            for name, var in self.pv_vars.items():
                if isinstance(var, tk.Text):
                    var.delete('1.0', tk.END)
                elif 'Date' in name:
                    var.set(datetime.now().strftime('%Y-%m-%d'))
                elif name in ['designCode']:
                    var.set('AS 1210-3')
                elif name in ['location']:
                    var.set('Itinerant')
                elif name in ['inspectorName']:
                    var.set('Glenn Scatchard')
                elif name in ['pressureGaugeWorking']:
                    var.set('Not Observed')
                elif name in ['externalSurfaceComments', 'internalSurfaceComments', 'baseMountsComments']:
                    var.set('Satisfactory')
                elif name in ['overallResult', 'visualInspection', 'pressureTest', 'safetyDevices']:
                    var.set('PASS')
                else:
                    var.set('')

    def get_safety_valve_data(self):
        """Collect Safety Valve form data"""
        data = {}
        for name, var in self.sv_vars.items():
            if isinstance(var, tk.Text):
                data[name] = var.get('1.0', tk.END).strip()
            else:
                data[name] = var.get()
        return data

    def get_pressure_vessel_data(self):
        """Collect Pressure Vessel form data"""
        data = {}
        for name, var in self.pv_vars.items():
            if isinstance(var, tk.Text):
                data[name] = var.get('1.0', tk.END).strip()
            else:
                data[name] = var.get()
        return data

    def generate_safety_valve_pdf(self):
        """Generate filled Safety Valve PDF"""
        data = self.get_safety_valve_data()

        # Validate required fields
        required = ['clientCompany', 'clientAddress', 'reportDate', 'jobNumber', 'testNumber', 'testDate',
                   'valveSize', 'manufacturer', 'model', 'valveSerialNo', 'setPressure']
        missing = [f for f in required if not data.get(f)]
        if missing:
            messagebox.showerror("Validation Error", f"Please fill in required fields:\n{', '.join(missing)}")
            return

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Safety_Valve_Report_{data['jobNumber']}"
        )
        if not filename:
            return

        try:
            actual_output = self.create_safety_valve_pdf(data, filename)
            self.status_var.set(f"Report saved: {os.path.basename(actual_output)}")
            messagebox.showinfo("Success", f"Report generated successfully!\n\nSaved to:\n{actual_output}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF:\n{str(e)}")

    def generate_pressure_vessel_pdf(self):
        """Generate filled Pressure Vessel PDF"""
        data = self.get_pressure_vessel_data()

        # Validate required fields
        required = ['clientCompany', 'clientAddress', 'manufacturer', 'model', 'serialNo',
                   'testDate', 'testNumber', 'reportDate', 'jobNumber', 'designPressure', 'operatingPressure']
        missing = [f for f in required if not data.get(f)]
        if missing:
            messagebox.showerror("Validation Error", f"Please fill in required fields:\n{', '.join(missing)}")
            return

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Pressure_Vessel_Report_{data['jobNumber']}"
        )
        if not filename:
            return

        try:
            actual_output = self.create_pressure_vessel_pdf(data, filename)
            self.status_var.set(f"Report saved: {os.path.basename(actual_output)}")
            messagebox.showinfo("Success", f"Report generated successfully!\n\nSaved to:\n{actual_output}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF:\n{str(e)}")

    def save_safety_valve_json(self):
        """Save Safety Valve data as JSON"""
        data = self.get_safety_valve_data()
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"SafetyValveReport_{data.get('jobNumber', 'data')}"
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.status_var.set(f"JSON saved: {os.path.basename(filename)}")

    def save_pressure_vessel_json(self):
        """Save Pressure Vessel data as JSON"""
        data = self.get_pressure_vessel_data()
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"PressureVesselReport_{data.get('jobNumber', 'data')}"
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.status_var.set(f"JSON saved: {os.path.basename(filename)}")

    def create_safety_valve_pdf(self, data, output_path):
        """Create report from the client Word template and return the saved path."""
        template_data = map_safety_valve_form_data(data)
        return generate_safety_valve_template_pdf(template_data, output_path)

    def create_pressure_vessel_pdf(self, data, output_path):
        """Create report from the client Word template and return the saved path."""
        template_data = map_pressure_vessel_form_data(data)
        return generate_pressure_vessel_template_pdf(template_data, output_path)

    def fill_pdf_template(self, template_path, output_path, data, form_type):
        """Fill an existing PDF template with data"""
        from pypdf import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        from io import BytesIO

        reader = PdfReader(template_path)
        writer = PdfWriter()

        # Create overlay with data
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        width, height = letter

        # Map data to coordinates
        if form_type == 'safety_valve':
            self.draw_safety_valve_data(c, data, width, height)
        else:
            self.draw_pressure_vessel_data(c, data, width, height)

        c.save()
        packet.seek(0)

        # Merge overlay with template
        from pypdf import PdfReader as OverlayReader
        overlay = OverlayReader(packet)

        for i, page in enumerate(reader.pages):
            if i < len(overlay.pages):
                page.merge_page(overlay.pages[i])
            writer.add_page(page)

        # Save output
        with open(output_path, 'wb') as f:
            writer.write(f)

    def draw_safety_valve_data(self, c, data, width, height):
        """Draw Safety Valve data on PDF canvas with corrected coordinates"""
        c.setFont("Helvetica", 10)

        # Page 1 - Cover
        c.drawString(155, height - 185, data.get('clientCompany', ''))
        c.drawString(155, height - 210, data.get('clientAddress', ''))
        c.drawString(155, height - 355, data.get('reportDate', ''))
        c.drawString(155, height - 380, data.get('jobNumber', ''))
        c.drawString(155, height - 405, data.get('reference', ''))

        # Page 2 - Main report
        c.showPage()
        c.setFont("Helvetica", 10)

        # Client info section
        c.drawString(175, height - 100, data.get('clientCompany', ''))
        c.drawString(175, height - 125, data.get('clientAddress', ''))
        c.drawString(175, height - 150, data.get('testNumber', ''))
        
        c.drawString(475, height - 100, data.get('site', ''))
        c.drawString(475, height - 125, data.get('contact', ''))
        c.drawString(475, height - 150, data.get('poReference', ''))
        c.drawString(475, height - 175, data.get('testDate', ''))

        # Valve details
        c.drawString(125, height - 245, data.get('valveSize', ''))
        c.drawString(125, height - 270, data.get('manufacturer', ''))
        c.drawString(125, height - 295, data.get('model', ''))
        
        c.drawString(375, height - 245, data.get('dischargeType', ''))
        c.drawString(375, height - 270, data.get('valveSerialNo', ''))
        c.drawString(375, height - 295, data.get('blowdownType', ''))

        # Set Pressure and Tolerances
        c.setFont("Helvetica-Bold", 10)
        c.drawString(205, height - 380, data.get('setPressure', '') + ' kPa')
        c.setFont("Helvetica", 10)
        c.drawString(205, height - 415, data.get('lowerTolerance', ''))
        c.drawString(205, height - 450, data.get('upperTolerance', ''))

        # Gauge details
        c.drawString(145, height - 525, data.get('testGaugeId', ''))
        c.drawString(355, height - 525, data.get('gaugeModel', ''))
        c.drawString(145, height - 545, data.get('gaugeSerialNo', ''))
        c.drawString(385, height - 545, data.get('recalibrationDue', ''))

        # Page 3 - Test Results
        c.showPage()
        c.setFont("Helvetica", 10)

        # Results
        c.drawString(265, height - 130, data.get('avgLiftPressure', '') + ' kPa' if data.get('avgLiftPressure') else '')
        c.drawString(265, height - 160, data.get('avgReseatPressure', '') + ' kPa' if data.get('avgReseatPressure') else '')
        c.drawString(265, height - 190, data.get('flowRate', '') + ' scfm' if data.get('flowRate') else '')
        c.drawString(265, height - 220, data.get('blowdownPercent', '') + '%' if data.get('blowdownPercent') else '')

        # Checkboxes PASS/FAIL logic
        def draw_check(x, y):
            c.setFont("ZapfDingbats", 12)
            c.drawString(x + 1, y + 2, "4") # Checkmark
            c.setFont("Helvetica", 10)

        # Pass boxes for tests
        if data.get('leakTest') == 'PASS': draw_check(100, height - 270 + 2)
        if data.get('setPressureTest') == 'PASS': draw_check(250, height - 270 + 2)
        if data.get('blowdownTest') == 'PASS': draw_check(450, height - 270 + 2)

        # Overall Result
        if data.get('overallResult') == 'PASS':
            c.setFont("Helvetica-Bold", 14)
            c.drawString(195, height - 302, "PASS")

        # Comments
        comments = data.get('comments', '')
        y_comments = height - 385
        c.setFont("Helvetica", 9)
        words = comments.split()
        line = ''
        for word in words:
            if c.stringWidth(line + ' ' + word) < 500:
                line += ' ' + word if line else word
            else:
                c.drawString(55, y_comments, line)
                y_comments -= 12
                line = word
        if line:
            c.drawString(55, y_comments, line)

        # Signature
        c.setFont("Helvetica-Bold", 10)
        c.drawString(135, height - 515, data.get('technicianName', ''))
        c.drawString(405, height - 545, data.get('signatureDate', ''))

    def draw_pressure_vessel_data(self, c, data, width, height):
        """Draw Pressure Vessel data on PDF canvas with corrected coordinates"""
        c.setFont("Helvetica", 10)

        # Page 1 - Cover
        c.drawString(155, height - 185, data.get('clientCompany', ''))
        c.drawString(155, height - 210, data.get('clientAddress', ''))
        c.drawString(155, height - 355, data.get('reportDate', ''))
        c.drawString(155, height - 380, data.get('jobNumber', ''))
        c.drawString(155, height - 405, data.get('reference', ''))

        # Page 2 - Main report
        c.showPage()
        c.setFont("Helvetica", 10)

        # Equipment details
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

        # Vessel details
        c.drawString(175, height - 315, data.get('vesselManufacturer', ''))
        c.drawString(435, height - 315, data.get('vesselSerialNo', ''))
        c.drawString(175, height - 340, data.get('manufacturedDate', ''))
        c.drawString(435, height - 340, data.get('designCode', ''))
        c.drawString(175, height - 365, data.get('location', ''))
        c.drawString(435, height - 365, data.get('corrosionAllowance', ''))

        # Page 3 - Design Info & Results
        c.showPage()
        c.setFont("Helvetica", 10)

        # Design info
        c.drawString(205, height - 125, data.get('vesselType', ''))
        c.drawString(465, height - 125, data.get('tankCapacity', ''))
        c.drawString(205, height - 150, data.get('designRegNo', ''))
        c.drawString(465, height - 150, data.get('hydrostaticTestDate', ''))
        c.drawString(205, height - 175, data.get('worksafeRegNo', ''))
        c.drawString(465, height - 175, data.get('designTemp', ''))
        c.drawString(205, height - 200, data.get('commissioningDate', ''))
        c.drawString(465, height - 200, data.get('ambientTemp', ''))
        c.drawString(205, height - 225, data.get('designPressure', ''))
        c.drawString(465, height - 225, data.get('shellLength', ''))
        c.drawString(205, height - 250, data.get('operatingPressure', ''))
        c.drawString(465, height - 250, data.get('shellDiameter', ''))
        c.drawString(205, height - 275, data.get('testPressure', ''))
        c.drawString(205, height - 300, data.get('hazardLevel', ''))

        # Results Checkboxes PASS/FAIL logic
        def draw_check(x, y):
            c.setFont("ZapfDingbats", 12)
            c.drawString(x + 1, y + 2, "4")
            c.setFont("Helvetica", 10)

        y_res = [height - 375, height - 400, height - 425]
        fields = ['visualInspection', 'pressureTest', 'safetyDevices']
        for y, field in zip(y_res, fields):
            val = data.get(field)
            if val == 'PASS': draw_check(170, y + 2)
            elif val == 'FAIL': draw_check(240, y + 2)

        # Overall Result
        if data.get('overallResult') == 'PASS':
            c.setFont("Helvetica-Bold", 14)
            c.drawString(195, height - 462, "PASS")

        # Page 4 - Comments
        c.showPage()
        c.setFont("Helvetica", 9)
        
        # Wrapped Comments
        def draw_wrapped(text, x, y, max_w):
            words = text.split()
            line = ''
            curr_y = y
            for word in words:
                if c.stringWidth(line + ' ' + word) < max_w:
                    line += ' ' + word if line else word
                else:
                    c.drawString(x, curr_y, line)
                    curr_y -= 12
                    line = word
            if line:
                c.drawString(x, curr_y, line)

        draw_wrapped(data.get('comments', ''), 55, height - 135, 500)
        draw_wrapped(data.get('recommendations', ''), 55, height - 315, 500)
        
        c.setFont("Helvetica-Bold", 10)
        c.drawString(205, height - 380, data.get('nextInspectionDue', ''))
        
        # Signature
        c.drawString(135, height - 515, data.get('inspectorName', ''))
        c.drawString(405, height - 545, data.get('signatureDate', ''))

    def generate_safety_valve_from_scratch(self, data, output_path):
        """Generate Safety Valve PDF matching client template exactly"""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        from reportlab.lib.units import inch

        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # ============================================================
        # PAGE 1 - COVER PAGE
        # ============================================================

        # Blue Header
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.rect(0, height - 120, width, 120, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width/2, height - 70, "SAFETY RELIEF VALVE TEST REPORT")

        # Prepared For Section
        y = height - 170
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Prepared For:")

        y -= 30
        c.setFont("Helvetica", 11)
        c.drawString(50, y, "Client / Company:")
        c.drawString(180, y, data.get('clientCompany', ''))

        y -= 25
        c.drawString(50, y, "Address:")
        c.drawString(180, y, data.get('clientAddress', ''))

        # Prepared By Section
        y -= 50
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Prepared By:")

        y -= 25
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Western Air Compliance")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Technician: Glenn Scatchard")
        y -= 18
        c.drawString(50, y, "Email: info@westernaircompliance.com.au")
        y -= 18
        c.drawString(50, y, "Website: www.westernaircompliance.com.au")
        y -= 18
        c.drawString(50, y, "Phone : 0459 851 411")

        # Report Details
        y -= 50
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Report Date:")
        c.drawString(150, y, data.get('reportDate', ''))

        y -= 22
        c.drawString(50, y, "Job Number:")
        c.drawString(150, y, data.get('jobNumber', ''))

        y -= 22
        c.drawString(50, y, "Reference:")
        c.drawString(150, y, data.get('reference', ''))

        # Confidentiality Notice
        y -= 60
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Confidentiality Notice")

        y -= 20
        c.setFont("Helvetica", 9)
        notice = ("This report has been prepared exclusively for the client specified above. It contains information "
                   "relating to the inspection, testing, and assessment of pressure equipment and associated "
                   "components. No part of this report may be reproduced, distributed, or used without written "
                   "permission from Western Air Compliance.")

        # Wrap text
        words = notice.split()
        line = ''
        for word in words:
            test_line = line + ' ' + word if line else word
            if c.stringWidth(test_line, "Helvetica", 9) < 500:
                line = test_line
            else:
                c.drawString(50, y, line)
                y -= 14
                line = word
        if line:
            c.drawString(50, y, line)

        c.showPage()

        # ============================================================
        # PAGE 2 - MAIN REPORT
        # ============================================================

        # Company Header
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.rect(0, height - 70, width, 70, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 35, "WESTERN AIR COMPLIANCE")
        c.setFont("Helvetica", 9)
        c.drawString(50, height - 55, "Inspection | Testing | Certification")
        c.drawString(50, height - 70, "Servicing Perth Metro & Regional Western Australia    ABN - 36 280 464 689")

        # Report Title
        y = height - 100
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "SAFETY RELIEF VALVE TEST REPORT TO AS 1271:2003")

        # Client Information Section
        y -= 30
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Client / Company:")
        c.drawString(180, y, data.get('clientCompany', ''))

        y -= 18
        c.drawString(50, y, "Address:")
        c.drawString(180, y, data.get('clientAddress', ''))

        y -= 18
        c.drawString(50, y, "Test Number:")
        c.drawString(180, y, data.get('testNumber', ''))

        y -= 18
        c.drawString(50, y, "Site Contact:")
        c.drawString(180, y, data.get('contact', ''))

        y -= 18
        c.drawString(50, y, "PO / Reference No:")
        c.drawString(180, y, data.get('poReference', ''))

        y -= 18
        c.drawString(50, y, "Test Date:")
        c.drawString(180, y, data.get('testDate', ''))

        # Valve Identification Section
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Valve Identification")
        c.setFillColor(colors.black)

        y -= 22
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Size:")
        c.drawString(150, y, data.get('valveSize', ''))

        y -= 18
        c.drawString(50, y, "Manufacturer:")
        c.drawString(150, y, data.get('manufacturer', ''))

        y -= 18
        c.drawString(50, y, "Model:")
        c.drawString(150, y, data.get('model', ''))

        y -= 18
        c.drawString(50, y, "Discharge Type:")
        c.drawString(150, y, data.get('dischargeType', 'Atmosphere'))

        y -= 18
        c.drawString(50, y, "Set Pressure (kPa):")
        c.drawString(150, y, data.get('setPressure', ''))

        y -= 18
        c.drawString(50, y, "Valve Serial No:")
        c.drawString(150, y, data.get('valveSerialNo', ''))

        y -= 18
        c.drawString(50, y, "Blowdown Type:")
        c.drawString(150, y, data.get('blowdownType', 'Non-Adjustable'))

        # Acceptance Criteria & Gauge Details
        y -= 35
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Acceptance Criteria & Gauge Details - Standard: AS 1271-2003")
        c.setFillColor(colors.black)

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Test Gauge ID:")
        c.drawString(180, y, data.get('testGaugeId', 'N/A'))

        y -= 18
        c.drawString(50, y, "Gauge Model:")
        c.drawString(180, y, data.get('gaugeModel', 'Druck DPI104'))

        y -= 18
        c.drawString(50, y, "Gauge Serial No:")
        c.drawString(180, y, data.get('gaugeSerialNo', '6113016'))

        y -= 18
        c.drawString(50, y, "Certification No:")
        c.drawString(180, y, "N/A")

        y -= 18
        c.drawString(50, y, "Recalibration Due:")
        c.drawString(180, y, data.get('recalibrationDue', ''))

        y -= 18
        c.drawString(50, y, "Test Medium:")
        c.drawString(180, y, "Nitrogen")

        # Final Test Results
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Final Test Results")
        c.setFillColor(colors.black)

        y -= 22
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Average Final Lift Pressure (kPa):")
        c.drawString(280, y, data.get('avgLiftPressure', ''))

        y -= 18
        c.drawString(50, y, "Average Final Reseat Pressure (kPa):")
        c.drawString(280, y, data.get('avgReseatPressure', ''))

        y -= 18
        c.drawString(50, y, "Flow Rate (scfm):")
        c.drawString(280, y, data.get('flowRate', ''))

        y -= 18
        c.drawString(50, y, "Blowdown %:")
        c.drawString(280, y, data.get('blowdownPercent', ''))

        y -= 18
        c.drawString(50, y, "Allowable Blowdown %:")
        c.drawString(280, y, "<15")

        # PASS/FAIL Results
        y -= 22
        c.drawString(50, y, "Leak Test:")
        self._draw_pass_fail(c, 150, y, "PASS")

        y -= 20
        c.drawString(50, y, "Set Pressure Test:")
        self._draw_pass_fail(c, 150, y, "PASS")

        y -= 20
        c.drawString(50, y, "Blowdown %:")
        self._draw_pass_fail(c, 150, y, "PASS")

        y -= 20
        c.drawString(50, y, "Overall Result:")
        self._draw_pass_fail(c, 150, y, "PASS")

        # Comments & Deviations
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Comments & Deviations")
        c.setFillColor(colors.black)

        y -= 20
        c.setFont("Helvetica", 10)
        comments = data.get('comments', '')
        words = comments.split()
        line = ''
        for word in words:
            test_line = line + ' ' + word if line else word
            if c.stringWidth(test_line, "Helvetica", 10) < 480:
                line = test_line
            else:
                c.drawString(50, y, line)
                y -= 16
                line = word
        if line:
            c.drawString(50, y, line)

        # Technician Declaration
        y = 120
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Technician Declaration")
        c.setFillColor(colors.black)

        y -= 20
        c.setFont("Helvetica", 9)
        c.drawString(50, y, "I certify that the safety valve detailed above has been inspected and tested in accordance with AS 1271:2003,")
        y -= 14
        c.drawString(50, y, "and that the results recorded are true and correct at the time of inspection.")

        y -= 25
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Technician:")
        c.drawString(130, y, data.get('technicianName', 'Glenn Scatchard'))

        y -= 20
        c.drawString(50, y, "Signature:")
        c.drawString(130, y, "_______________________")

        y -= 20
        c.drawString(50, y, "Date:")
        c.drawString(130, y, data.get('signatureDate', ''))

        c.save()

    def _draw_pass_fail(self, c, x, y, result):
        """Helper to draw PASS/FAIL boxes"""
        from reportlab.lib import colors

        # Draw PASS box
        if result == "PASS":
            c.setFillColor(colors.green)
            c.rect(x, y - 3, 50, 16, fill=True, stroke=True)
            c.setFillColor(colors.white)
        else:
            c.setFillColor(colors.white)
            c.rect(x, y - 3, 50, 16, fill=True, stroke=True)
            c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(x + 25, y, "PASS")

        # Draw FAIL box
        if result == "FAIL":
            c.setFillColor(colors.red)
            c.rect(x + 55, y - 3, 50, 16, fill=True, stroke=True)
            c.setFillColor(colors.white)
        else:
            c.setFillColor(colors.white)
            c.rect(x + 55, y - 3, 50, 16, fill=True, stroke=True)
            c.setFillColor(colors.black)
        c.drawCentredString(x + 80, y, "FAIL")

    def generate_pressure_vessel_from_scratch(self, data, output_path):
        """Generate Pressure Vessel PDF matching client template exactly (3 pages)"""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors

        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # ============================================================
        # PAGE 1 - COVER PAGE
        # ============================================================

        # Blue Header
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.rect(0, height - 120, width, 120, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(width/2, height - 70, "PRESSURE VESSEL INSPECTION REPORT")

        # Prepared For Section
        y = height - 170
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Prepared For:")

        y -= 30
        c.setFont("Helvetica", 11)
        c.drawString(50, y, "Client / Company:")
        c.drawString(180, y, data.get('clientCompany', ''))

        y -= 25
        c.drawString(50, y, "Address:")
        c.drawString(180, y, data.get('clientAddress', ''))

        # Prepared By Section
        y -= 50
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Prepared By:")

        y -= 25
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Western Air Compliance")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Technician: Glenn Scatchard")
        y -= 18
        c.drawString(50, y, "Email: info@westernaircompliance.com.au")
        y -= 18
        c.drawString(50, y, "Website: www.westernaircompliance.com.au")
        y -= 18
        c.drawString(50, y, "Phone : 0459 851 411")

        # Report Details
        y -= 50
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Report Date:")
        c.drawString(150, y, data.get('reportDate', ''))

        y -= 22
        c.drawString(50, y, "Job Number:")
        c.drawString(150, y, data.get('jobNumber', ''))

        y -= 22
        c.drawString(50, y, "Reference:")
        c.drawString(150, y, data.get('reference', ''))

        # Confidentiality Notice
        y -= 60
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Confidentiality Notice")

        y -= 20
        c.setFont("Helvetica", 9)
        notice = ("This report has been prepared exclusively for the client specified above. It contains information "
                   "relating to the inspection, testing, and assessment of pressure equipment and associated "
                   "components. No part of this report may be reproduced, distributed, or used without written "
                   "permission from Western Air Compliance.")

        words = notice.split()
        line = ''
        for word in words:
            test_line = line + ' ' + word if line else word
            if c.stringWidth(test_line, "Helvetica", 9) < 500:
                line = test_line
            else:
                c.drawString(50, y, line)
                y -= 14
                line = word
        if line:
            c.drawString(50, y, line)

        c.showPage()

        # ============================================================
        # PAGE 2 - MAIN REPORT (Client Info, Vessel Details, Design Info)
        # ============================================================

        # Company Header
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.rect(0, height - 70, width, 70, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 35, "WESTERN AIR COMPLIANCE")
        c.setFont("Helvetica", 9)
        c.drawString(50, height - 55, "Inspection | Testing | Certification")
        c.drawString(50, height - 70, "Servicing Perth Metro & Regional Western Australia    ABN - 36 280 464 689")

        # Report Title
        y = height - 100
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "PRESSURE VESSEL INSPECTION REPORT TO AS/NZS 3788:2024")

        # Client Information
        y -= 30
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Client / Company:")
        c.drawString(180, y, data.get('clientCompany', ''))

        y -= 18
        c.drawString(50, y, "Address:")
        c.drawString(180, y, data.get('clientAddress', ''))

        y -= 18
        c.drawString(50, y, "Manufacturer:")
        c.drawString(180, y, data.get('manufacturer', ''))

        y -= 18
        c.drawString(50, y, "Model:")
        c.drawString(180, y, data.get('model', ''))

        y -= 18
        c.drawString(50, y, "Serial No:")
        c.drawString(180, y, data.get('serialNo', ''))

        y -= 18
        c.drawString(50, y, "Test Number:")
        c.drawString(180, y, data.get('testNumber', ''))

        y -= 18
        c.drawString(50, y, "Site Contact:")
        c.drawString(180, y, data.get('contact', ''))

        y -= 18
        c.drawString(50, y, "PO / Reference No:")
        c.drawString(180, y, data.get('poReference', ''))

        y -= 18
        c.drawString(50, y, "Asset No:")
        c.drawString(180, y, data.get('assetNo', ''))

        y -= 18
        c.drawString(50, y, "Test Date:")
        c.drawString(180, y, data.get('testDate', ''))

        y -= 18
        c.drawString(50, y, "Unit Type:")
        c.drawString(180, y, data.get('unitType', ''))

        # Vessel Details
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Vessel Details")
        c.setFillColor(colors.black)

        y -= 22
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Manufacturer:")
        c.drawString(180, y, data.get('vesselManufacturer', ''))

        y -= 18
        c.drawString(50, y, "Manufactured Date:")
        c.drawString(180, y, data.get('manufacturedDate', ''))

        y -= 18
        c.drawString(50, y, "Location:")
        c.drawString(180, y, data.get('location', 'Itinerant'))

        y -= 18
        c.drawString(50, y, "Serial No:")
        c.drawString(180, y, data.get('vesselSerialNo', ''))

        y -= 18
        c.drawString(50, y, "Design Code:")
        c.drawString(180, y, data.get('designCode', 'AS1210-3'))

        y -= 18
        c.drawString(50, y, "Corrosion Allowance (mm):")
        c.drawString(180, y, data.get('corrosionAllowance', ''))

        # Design Information
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Pressure Vessel Design Information")
        c.setFillColor(colors.black)

        y -= 22
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Type:")
        c.drawString(180, y, data.get('vesselType', ''))

        y -= 18
        c.drawString(50, y, "Design Registration No:")
        c.drawString(180, y, data.get('designRegNo', ''))

        y -= 18
        c.drawString(50, y, "WorkSafe Registration No:")
        c.drawString(180, y, data.get('worksafeRegNo', ''))

        y -= 18
        c.drawString(50, y, "Commissioning Date:")
        c.drawString(180, y, data.get('commissioningDate', ''))

        y -= 18
        c.drawString(50, y, "Design Pressure (Kpa):")
        c.drawString(180, y, data.get('designPressure', ''))

        y -= 18
        c.drawString(50, y, "Operating Pressure (Kpa):")
        c.drawString(180, y, data.get('operatingPressure', ''))

        y -= 18
        c.drawString(50, y, "Test Pressure (Kpa):")
        c.drawString(180, y, data.get('testPressure', ''))

        y -= 18
        c.drawString(50, y, "Hazard Level (as per AS/NZS 3788:2024):")
        c.drawString(280, y, data.get('hazardLevel', ''))

        y -= 18
        c.drawString(50, y, "Tank Capacity:")
        c.drawString(180, y, data.get('tankCapacity', ''))

        y -= 18
        c.drawString(50, y, "Hydrostatic Test Date:")
        c.drawString(180, y, data.get('hydrostaticTestDate', ''))

        y -= 18
        c.drawString(50, y, "Design Temperature (Degrees):")
        c.drawString(180, y, data.get('designTemp', ''))

        y -= 18
        c.drawString(50, y, "Ambient Air Temperature (Degrees):")
        c.drawString(180, y, data.get('ambientTemp', ''))

        y -= 18
        c.drawString(50, y, "Shell Length (mm):")
        c.drawString(180, y, data.get('shellLength', ''))

        y -= 18
        c.drawString(50, y, "Shell Diameter (mm):")
        c.drawString(180, y, data.get('shellDiameter', ''))

        # Compliance Standards
        y -= 35
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Compliance Standards & Inspection Criteria")
        c.setFillColor(colors.black)

        y -= 22
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Inspection carried out in accordance with:")

        y -= 18
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "AS/NZS 3788:2024 - Pressure Equipment: In-Service Inspection")
        y -= 16
        c.drawString(70, y, "AS/NZS 1200 - Pressure Equipment (General Requirements)")
        y -= 16
        c.drawString(70, y, "AS 1210 - Pressure Vessels")

        c.showPage()

        # ============================================================
        # PAGE 3 - INSPECTION FINDINGS
        # ============================================================

        # Company Header (repeated)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.rect(0, height - 70, width, 70, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 35, "WESTERN AIR COMPLIANCE")
        c.setFont("Helvetica", 9)
        c.drawString(50, height - 55, "Inspection | Testing | Certification")
        c.drawString(50, height - 70, "Servicing Perth Metro & Regional Western Australia    ABN - 36 280 464 689")

        # Inspection Findings
        y = height - 100
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Inspection Findings")

        # External Surface Condition
        y -= 30
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "External Surface Condition:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Good    [  ] Fair    [  ] Poor")

        y -= 18
        c.drawString(50, y, "Comments:")
        c.drawString(120, y, "Satisfactory")

        # Internal Surface Condition
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Internal Surface Condition (if applicable):")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Good    [  ] Fair    [  ] Poor")

        y -= 18
        c.drawString(50, y, "Comments:")
        c.drawString(120, y, "Satisfactory")

        # Corrosion / Pitting
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Corrosion / Pitting Observed:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Yes    [ X ] No")

        # Pressure Gauge Working
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Pressure Gauge Working:")
        c.drawString(200, y, "Not Observed")

        # Paint / Coating Condition
        y -= 25
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Paint / Coating Condition:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Good    [  ] Fair    [  ] Poor")

        # Base / Mounts / Supports
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Base / Mounts / Supports:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Good    [  ] Fair    [  ] Poor")

        y -= 18
        c.drawString(50, y, "Comments:")
        c.drawString(120, y, "Satisfactory")

        # Nameplate
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Nameplate:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Present    [  ] Missing    [  ] Not Legible")

        # Drain Valve
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Drain Valve Operation:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] OK    [  ] Not Working    [  ] N/A")

        # Safety Valve Fitted
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Safety Valve Fitted:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Yes    [  ] No")

        y -= 18
        c.drawString(50, y, "See Report No:")

        # Assessment & Compliance
        y -= 35
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Assessment & Compliance")

        y -= 30
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Overall Vessel Condition:")

        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(70, y, "[  ] Good    [  ] Fair    [  ] Requires Monitoring    [  ] Unsafe / Remove from Service")

        # Compliance with Standard
        y -= 30
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Compliance with AS/NZS 3788:2024:")
        c.drawString(250, y, "PASS")

        y -= 20
        c.drawString(50, y, "Documentation:")

        y -= 18
        c.drawString(50, y, "Design Reports Sighted:")

        y -= 18
        c.drawString(50, y, "Next Scheduled Inspection Due:")
        c.drawString(250, y, data.get('nextInspectionDue', ''))

        y -= 18
        c.drawString(50, y, "Associated Documentation:")

        # Overall Result
        y -= 30
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, "Overall Result:")
        overall = data.get('overallResult', 'PASS')
        self._draw_pass_fail(c, 150, y, overall)

        # Comments
        y -= 40
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Comments & Deviations")
        c.setFillColor(colors.black)

        y -= 20
        c.setFont("Helvetica", 10)
        comments = data.get('comments', 'No obvious visual defects at the time of inspection, the vessel is suitable for continued use in this application')
        words = comments.split()
        line = ''
        for word in words:
            test_line = line + ' ' + word if line else word
            if c.stringWidth(test_line, "Helvetica", 10) < 480:
                line = test_line
            else:
                c.drawString(50, y, line)
                y -= 16
                line = word
        if line:
            c.drawString(50, y, line)

        # Technician Declaration
        y = 130
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.HexColor('#2E75B6'))
        c.drawString(50, y, "Technician Declaration")
        c.setFillColor(colors.black)

        y -= 20
        c.setFont("Helvetica", 9)
        c.drawString(50, y, "I certify that the pressure vessel detailed above has been inspected and tested in accordance with")
        y -= 14
        c.drawString(50, y, "AS/NZS 3788:2024, and that the results recorded are true and correct at the time of inspection.")

        y -= 25
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Technician:")
        c.drawString(130, y, data.get('inspectorName', 'Glenn Scatchard'))

        y -= 20
        c.drawString(50, y, "Signature")
        c.drawString(130, y, "_______________________")

        y -= 20
        c.drawString(50, y, "Date:")
        c.drawString(130, y, data.get('signatureDate', ''))

        c.save()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PDFReportApp(root)

    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
