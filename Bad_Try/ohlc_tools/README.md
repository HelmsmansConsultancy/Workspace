# ohlc-tools

Command-line tools for analysing and manipulating OHLC (Open/High/Low/Close) CSV data.

Designed for **Windows / PowerShell 5.1+** with Python 3.10+.

---

## Requirements

| Requirement | Minimum version | Install |
|---|---|---|
| Python | 3.10 | [python.org](https://www.python.org/downloads/) — tick **"Add python.exe to PATH"** |
| PowerShell | 5.1 (built-in on Win 10/11) | Already installed |

Verify your Python install:

```powershell
python --version
pip --version
```

---

## Installation

```powershell
# 1. Unzip / clone the project, then cd into it
cd ohlc_tools

# 2. Allow local scripts to run (one-time, current user only)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 3. Run the bootstrap script — creates .venv and installs everything
.\scripts\bootstrap.ps1

# 4. Activate the virtual environment
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your prompt. You only need to run bootstrap once; for future sessions just activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Commands

| Command | Description |
|---|---|
| `ohlc describe <file>` | Print a summary of an OHLC CSV file |
| `ohlc convert <file>` | Convert between CSV formats / delimiters |
| `ohlc resample <file>` | Resample OHLC data to a different timeframe |

### Examples

```powershell
# Describe a file
ohlc describe data\eurusd_h1.csv

# Resample H1 → H4 and write to a new file
ohlc resample data\eurusd_h1.csv --timeframe H4 --output data\eurusd_h4.csv

# Convert semicolon-delimited to comma-delimited
ohlc convert data\eurusd.csv --delimiter ";" --output data\eurusd_comma.csv
```

Both forward slashes and backslashes work for paths on Windows.

---

## Project layout

```
ohlc_tools\
├── .spyproject\          # Spyder 6 project metadata
├── ohlc_tools\           # Main package
│   ├── __init__.py
│   ├── cli.py            # Root `ohlc` command group
│   ├── commands\         # One module per sub-command
│   │   ├── describe.py
│   │   ├── convert.py
│   │   └── resample.py
│   └── utils\            # Shared helpers
│       ├── csv_reader.py
│       ├── timeframe.py
│       └── display.py
├── tests\                # pytest test suite
├── docs\                 # Documentation
├── scripts\              # PowerShell dev helper scripts
│   ├── bootstrap.ps1     # Create .venv and install deps
│   ├── lint.ps1          # Run ruff + black + mypy
│   └── test.ps1          # Run pytest
├── pyproject.toml        # Packaging, tooling, and test config
├── .editorconfig
├── .gitignore
└── README.md
```

---

## Development

```powershell
# Run the full test suite
.\scripts\test.ps1

# Run a specific test file
.\scripts\test.ps1 -k test_timeframe

# Lint and type-check
.\scripts\lint.ps1

# Format code in-place
black ohlc_tools tests

# Or run tools directly
pytest
ruff check ohlc_tools tests
mypy ohlc_tools
```

---

## Spyder 6

Open the project in Spyder via **Projects → Open Project** and point it at the `ohlc_tools\` folder. Spyder will detect the `.spyproject\` directory and configure the file explorer, linting, and working directory automatically.

Set Spyder's Python interpreter to your `.venv`:
**Tools → Preferences → Python interpreter → Use the following interpreter**
→ browse to `.venv\Scripts\python.exe`

---

## Troubleshooting

**`ohlc` is not recognised after activation**

Re-install in editable mode while the venv is active:
```powershell
pip install -e ".[dev]"
```

**`running scripts is disabled on this system`**

Run once in PowerShell as your normal user (no admin needed):
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Rich colours don't display correctly**

Enable VT100 colour support in Windows Terminal or run:
```powershell
Set-ItemProperty HKCU:\Console VirtualTerminalLevel -Type DWORD 1
```
Or pass `--no-color` to any command:
```powershell
ohlc describe data\eurusd_h1.csv --no-color
```
