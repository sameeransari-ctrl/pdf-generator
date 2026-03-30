# Desktop PDF Application - Quick Start

## 🚀 Get Started in 3 Steps

### Step 1: Install (One-time)
```bash
# Windows
double-click: run_app.bat

# OR run setup
python setup.py
```

### Step 2: Run the Application
```bash
# Windows
double-click: run_app.bat

# Mac/Linux
./run_app.sh

# Or directly
python desktop_pdf_app.py
```

### Step 3: Generate PDF Reports
1. Choose **Safety Valve** or **Pressure Vessel** tab
2. Fill in the form
3. Click **"Generate PDF Report"**
4. Done! ✅

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📝 **Client Word Templates** | Uses the supplied `.docx` files with placeholders |
| 🔧 **Safety Valve** | Automatic ±3% tolerance calculator |
| ⚙️ **Pressure Vessel** | Full AS/NZS 3788:2024 compliance |
| 📄 **PDF Generation** | Creates filled PDFs instantly |
| 💾 **JSON Export** | Save form data for later |
| 🌐 **Offline** | No internet required |
| 💻 **Cross-platform** | Windows, Mac, Linux |

---

## 🖥️ Application Interface

```
┌─────────────────────────────────────────────────────────────┐
│  Western Air Compliance - PDF Report Generator             │
├─────────────────────────────────────────────────────────────┤
│  [🔧 Safety Valve Report]  [⚙️ Pressure Vessel Report]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─ Client Information ─────────────────────────────────┐  │
│  │  Client Name: [________________________]              │  │
│  │  Address:     [________________________]              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─ Set Pressure & Tolerance Calculation ──────────────┐  │
│  │  Set Pressure (kPa): [1000       ] ← Enter this   │  │
│  │                                                      │  │
│  │  Lower Tolerance:    [970.00 kPa  ] ← Auto         │  │
│  │  Upper Tolerance:    [1030.00 kPa ] ← calculated!   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  [Clear Form]  [Generate PDF Report]  [Save as JSON]       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 File Overview

| File | Purpose |
|------|---------|
| `desktop_pdf_app.py` | **Main application** - Run this |
| `run_app.bat` | Windows launcher |
| `run_app.sh` | Mac/Linux launcher |
| `setup.py` | Installation helper |
| `requirements.txt` | Python packages needed |
| `PRODUCTION_SETUP.md` | Full documentation |

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python desktop_pdf_app.py

# First-time setup
python setup.py
```

---

## 🎯 What's New vs HTML Forms

| Feature | HTML Forms | Desktop App |
|---------|------------|-------------|
| Generates PDFs | ❌ No | ✅ **Yes!** |
| Works offline | ✅ Yes | ✅ Yes |
| Auto-calculations | ✅ Yes | ✅ Yes |
| Professional UI | ✅ Yes | ✅ Yes |
| Data validation | ✅ Yes | ✅ Yes |

**Major improvement: the desktop app now generates reports from the client Word templates and exports them to PDF.** 🎉

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.8+ and check "Add to PATH" |
| "Module not found" | Run `pip install -r requirements.txt` |
| App won't start | Run `python setup.py` |
| Tkinter error | Reinstall Python with tcl/tk option |

---

## 📞 Need Help?

1. Check **PRODUCTION_SETUP.md** for detailed guide
2. Review **USER_GUIDE.md** for form instructions
3. Contact your system administrator

---

**Ready to generate professional PDF reports! 🚀**
