# Western Air Compliance - Production Setup Guide
## Option 2: Desktop Application

---

## 📋 Overview

This guide explains how to set up and use the **Desktop PDF Application** - a standalone Windows/Mac application that:

- ✅ **Works completely offline** - No internet required
- ✅ **Generates filled PDFs locally** - No server needed
- ✅ **Uses the original client Word documents** - Placeholder templates are created from the supplied `.docx` files
- ✅ **Automatic calculations** - ±3% tolerance calculator included
- ✅ **Professional UI** - Desktop application interface
- ✅ **Cross-platform** - Works on Windows, Mac, and Linux

---

## 🚀 Quick Start

### For Windows Users

#### Option A: Using the Batch Launcher (Easiest)

1. **Double-click** `run_app.bat`
2. The application will check for dependencies and install if needed
3. The desktop application opens automatically

#### Option B: Using Python Directly

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the application
python desktop_pdf_app.py
```

### For Mac/Linux Users

1. Open Terminal
2. Navigate to the project folder:
   ```bash
   cd /path/to/fillable-pdfs-task
   ```
3. Make the launcher executable and run:
   ```bash
   chmod +x run_app.sh
   ./run_app.sh
   ```

### Using Setup Script

Run the setup script to install all dependencies automatically:

```bash
# Windows
python setup.py

# Mac/Linux
python3 setup.py
```

---

## 📦 Installation Details

### Requirements

- **Python 3.8 or higher**
- **Operating System:** Windows 7+, macOS 10.12+, or Linux
- **RAM:** 2GB minimum (4GB recommended)
- **Disk Space:** 50MB for application + PDF storage

### Python Dependencies

The following packages are automatically installed:

| Package | Purpose | Version |
|---------|---------|---------|
| `reportlab` | PDF generation | ≥4.0.0 |
| `pypdf` | PDF manipulation | ≥4.0.0 |
| `python-docx` | Word template editing | ≥1.1.0 |
| `comtypes` | Word to PDF conversion (Windows) | ≥1.4.0 |
| `Pillow` | Image handling | ≥10.0.0 |
| `tkinter` | GUI (built-in) | - |

### Installing Python (if needed)

**Windows:**
1. Download from [python.org/downloads](https://python.org/downloads)
2. Run installer and **check "Add Python to PATH"**
3. Complete installation

**Mac:**
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-tk
```

---

## 🖥 Using the Desktop Application

### Safety Valve Report

1. Click the **"Safety Valve Report"** tab
2. Fill in the form fields:
   - **Blue fields** = Input fields
   - Enter **Set Pressure (kPa)** → Tolerances calculate automatically!
3. Click **"Generate PDF Report"**
4. Choose save location
5. PDF is generated instantly

### Pressure Vessel Report

1. Click the **"Pressure Vessel Report"** tab
2. Fill in all required fields (marked with *)
3. Select inspection results (PASS/FAIL)
4. Click **"Generate PDF Report"**
5. Choose save location
6. PDF is generated instantly

### Additional Features

- **Clear Form** - Reset all fields to defaults
- **Save as JSON** - Save form data for later editing
- **Auto-calculated fields** - Gray fields calculate automatically
- **Tab navigation** - Use Tab key to move between fields

---

## 📁 File Structure

```
fillable pdfs task/
│
├── desktop_pdf_app.py          # MAIN APPLICATION FILE
├── run_app.bat                 # Windows launcher
├── run_app.sh                  # Mac/Linux launcher
├── setup.py                    # Setup/installation script
├── requirements.txt            # Python dependencies
│
├── client_doc/                          # Client-supplied source Word documents
├── templates/Safety_Valve_Client_Template.docx
├── templates/Pressure_Vessel_Client_Template.docx
│
├── safety_valve_form.html      # Original web form
├── pressure_vessel_form.html   # Original web form
│
├── USER_GUIDE.md               # User documentation
├── README.md                   # Quick start guide
└── PRODUCTION_SETUP.md         # This file
```

---

## ⚙️ Configuration

### Default Values

The application comes pre-configured with common values:

**Safety Valve:**
- Technician: Glenn Scatchard
- Discharge Type: Atmosphere
- Blowdown Type: Non-Adjustable
- Gauge Model: Druck DPI104
- Gauge Serial: 6113016

**Pressure Vessel:**
- Inspector: Glenn Scatchard
- Design Code: AS 1210-3
- Location: Itinerant

### Changing Defaults

Edit `desktop_pdf_app.py` and modify the default values in:
- `build_safety_valve_form()` method
- `build_pressure_vessel_form()` method

---

## 🔧 Troubleshooting

### Application Won't Start

**Problem:** `python is not recognized`
**Solution:**
1. Python is not in PATH
2. Reinstall Python and check "Add Python to PATH"
3. Or use full path: `C:\Python39\python.exe desktop_pdf_app.py`

**Problem:** `ModuleNotFoundError: No module named 'pypdf'`
**Solution:**
```bash
pip install -r requirements.txt
```

**Problem:** `No module named 'tkinter'`
**Solution:**
- Windows: Reinstall Python with "tcl/tk" option
- Mac: `brew install python-tk`
- Linux: `sudo apt-get install python3-tk`

### PDF Generation Issues

**Problem:** "Template not found" warning
**Solution:** Ensure the `client_doc/` source files are present, then run `python create_word_templates.py` to rebuild the placeholder templates.

**Problem:** PDF does not generate but a Word file is created
**Solution:** Install LibreOffice or Microsoft Word. The app fills the client `.docx` template first, then converts that document to PDF.

### Application Looks Wrong

**Problem:** Text is cut off or window is too small
**Solution:** Resize the window or use the scrollbars within each tab.

**Problem:** High DPI screen (4K) display issues
**Solution:** The app should auto-scale, but you may need to adjust Windows DPI settings.

---

## 🎨 Customization

### Changing Colors/Branding

Edit `desktop_pdf_app.py`:

```python
# Header color (line ~85)
self.style.configure('Header.TFrame', background='#2E75B6')

# Button colors (in button creation)
style='Header.TLabel'  # For blue buttons
```

### Adding More Fields

1. Locate the form builder method (`build_safety_valve_form` or `build_pressure_vessel_form`)
2. Add new field using:
   ```python
   self.create_form_row(section_frame, [
       ('fieldName', 'Label Text', 'entry', True)  # required
   ])
   ```
3. Add the field to the PDF drawing method

### Creating an Executable (Optional)

To create a standalone `.exe` file (no Python needed):

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed desktop_pdf_app.py

# Executable will be in dist/ folder
```

---

## 🔒 Data Security

### Local Processing

- ✅ All data stays on your computer
- ✅ No internet connection required
- ✅ No data sent to external servers
- ✅ PDFs generated locally

### Data Storage

- Form data can be saved as JSON files
- PDFs saved to location of your choice
- No automatic cloud backup
- Recommend regular backups of generated reports

---

## 📊 Comparison: Web vs Desktop

| Feature | HTML Forms | Desktop App |
|---------|------------|-------------|
| Internet Required | No | No |
| Generates PDF | ❌ (JSON only) | ✅ Yes |
| Professional UI | ✅ Yes | ✅ Yes |
| Data Validation | ✅ Yes | ✅ Yes |
| Auto-calculations | ✅ Yes | ✅ Yes |
| Save as JSON | ✅ Yes | ✅ Yes |
| Works Offline | ✅ Yes | ✅ Yes |
| Installation | None | Python + 3 packages |

**Winner: Desktop App** - Only option that generates actual PDFs locally!

---

## 🚀 Deployment Options

### Option 1: Developer Mode (Current)
- Install Python
- Install dependencies
- Run with `python desktop_pdf_app.py`
- Best for: Development, testing, updates

### Option 2: Portable Python
- Use portable Python distribution
- Pre-install all dependencies
- Distribute as zip file
- Best for: Internal company use

### Option 3: Executable (Recommended for Production)
- Use PyInstaller to create .exe
- Single file distribution
- No Python installation needed
- Best for: End users, clients

---

## 📝 Backup and Maintenance

### Regular Backups

1. **Generated PDFs** - Store in secure location
2. **JSON Data Files** - Can be re-imported (future feature)
3. **Templates** - Keep copies of the client `.docx` files and generated placeholder templates

### Updates

To update the application:
1. Backup your current version
2. Replace `desktop_pdf_app.py` with new version
3. Run `setup.py` if new dependencies added
4. Test with sample data

---

## 📞 Support

### Common Issues

See **Troubleshooting** section above for common issues and solutions.

### Getting Help

When reporting issues, include:
1. Operating System (Windows 10, macOS 12, etc.)
2. Python version (`python --version`)
3. Error message (screenshot or copy-paste)
4. Steps to reproduce the problem

---

## 🎯 Future Enhancements

Potential improvements for future versions:

- 📊 Report history and database
- 🔐 User authentication
- 📧 Email integration
- 🖨 Direct printing support
- 📱 Mobile companion app
- 🌐 Cloud sync option
- 🎨 Custom branding options

---

## ✅ Production Checklist

Before going live:

- [ ] Install Python 3.8+ on target computers
- [ ] Run `setup.py` to install dependencies
- [ ] Test Safety Valve report generation
- [ ] Test Pressure Vessel report generation
- [ ] Verify PDF output quality
- [ ] Test on each user's computer
- [ ] Create backup procedure
- [ ] Train users on the application
- [ ] Document any customizations

---

## 🎓 Pro Tips

### Tip 1: Keyboard Shortcuts
- **Tab** - Move to next field
- **Shift+Tab** - Move to previous field
- **Enter** - Activate buttons
- **Ctrl+A** - Select all text in field

### Tip 2: Default Dates
Today's date is automatically filled - no need to type!

### Tip 3: Auto-calculation
For Safety Valve: Just enter Set Pressure and watch the magic happen!

### Tip 4: Save Before Generate
Use "Save as JSON" to preserve form data before generating PDF.

### Tip 5: Multiple Reports
Open multiple instances of the application for side-by-side work.

---

**Version:** 2.0 (Desktop Application)
**Last Updated:** 2026-03-30
**For:** Western Air Compliance

---

## Quick Reference

```bash
# Windows - Run Application
run_app.bat

# Mac/Linux - Run Application
./run_app.sh

# All Platforms - Using Python
python desktop_pdf_app.py

# Install Dependencies
pip install -r requirements.txt

# Setup (First Time)
python setup.py
```

**You're ready to go! 🚀**
