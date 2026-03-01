# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/anujraghav252/H-to-WW-NanoAOD-analysis.git
cd H-to-WW-NanoAOD-analysis
```

## 2. Set Up the Environment

### Option A — pip (virtual environment)

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
pip install -r requirements.txt
```

### Option B — Conda

```bash
conda env create -f environment.yml
conda activate <env-name>
```

## 3. Verify the Installation

```bash
python scripts/test_uproot.py
```