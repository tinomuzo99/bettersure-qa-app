# BetterSure – Insurance Q&A (Streamlit)

Plain-English answers to common insurance questions. Generates CSV and a branded PDF.
Built with OpenAI + Streamlit + ReportLab.

## Setup (Local Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/tinomuzo99/bettersure-qa-app.git
   cd bettersure-qa-app
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # On Windows
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=sk-yourkeyhere
   ```

---


## Run Options

You can use the project in **two ways**:

### Option A — Batch generator (CSV + PDF)
Runs 20 pre-defined questions, saves `answers.csv`, and builds a branded `answers.pdf`.

```bash
python bettersure_ai_enablement.py --make-pdf
```

**Script:** `bettersure_ai_enablement.py`
- Uses OpenAI to answer the questions in `QUESTIONS`.
- Converts Markdown (**bold**, *italics*, and `**Tip:**`) to PDF-friendly formatting.
- Auto-paginates and prints progress (e.g., `Answering Q1/20`, `Adding content to PDF page 2…`).


### Option B — Streamlit mini‑UI (interactive)
Ask questions interactively in a browser.

```bash
python -m streamlit run streamlit_app.py
```

---

## Live Streamlit App

You can access the deployed **Streamlit version** of this project here:
[BetterSure Q&A App on Streamlit](https://bettersure-app-app-jsmzcrhfnqxtvssvnvrs2u.streamlit.app/)

This hosted version lets you ask insurance-related questions interactively using the BetterSure branding and colour scheme — no setup required.

---
