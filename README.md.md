# BetterSure – Insurance Q&A (Streamlit + OpenAI)

A fully interactive Q&A web app that answers common insurance questions in plain English using OpenAI's GPT models. The app can also generate branded PDF and CSV outputs for batch processing.

---

## 🚀 Features

- **Interactive Streamlit interface** – ask questions and get concise, plain-English answers.
- **BetterSure brand styling** – consistent colours, typography, and layout.
- **Markdown rendering** – supports **bold**, *italics*, and **Tip:** highlights.
- **Batch mode** – generate 20 pre-defined Q&A pairs into `answers.csv` and a branded `answers.pdf`.
- **PDF Export** – ReportLab-generated document with BetterSure colours and layout.
- **Environment-based API key loading** – uses `.env` locally or Streamlit Secrets in the cloud.

---

## 🧩 File Structure

```
├── bettersure_ai_enablement.py     # Batch Q&A and PDF/CSV generator
├── streamlit_app.py                # Streamlit web UI
├── ask_cli.py                      # Command-line version (no web server)
├── requirements.txt                # Python dependencies
├── runtime.txt                     # (Optional) Python version for deployment
├── .streamlit/config.toml          # Streamlit theme config
├── .gitignore                      # Ignore secrets and temp files
└── README.md                       # This file
```

---

## 🧠 Setup (Local Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/bettersure-qa-app.git
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

4. Run the app locally:
   ```bash
   python -m streamlit run streamlit_app.py
   ```

---

## 🖥️ Deployment (Streamlit Community Cloud)

1. Push your repo to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Click **New app**, select your repo and branch, and set:
   - **Main file path:** `streamlit_app.py`
4. In **App → Settings → Secrets**, add your API key:
   ```bash
   OPENAI_API_KEY = "sk-yourkeyhere"
   ```
5. Click **Deploy**.

Your app will automatically rebuild when you push new commits.

---

## 🎨 Branding (BetterSure Theme)

- **Primary Colour:** `#214B61`
- **Accent Colour:** `#F58220`
- **Secondary Text Colour:** `#6C8CA1`
- **Background:** Light grey `#f9f9f9`

These values are hard-coded in both `streamlit_app.py` and `.streamlit/config.toml` to match the BetterSure brand palette.

---

## 🧾 Batch Generation (PDF + CSV)

Run the following command to generate all 20 Q&A pairs into `answers.csv` and `answers.pdf`:

```bash
python bettersure_ai_enablement.py --make-pdf
```

Both files are saved in the project root.

---

## 💡 CLI Version

For environments where Streamlit cannot run:

```bash
python ask_cli.py
```

This opens an interactive text-based interface in the terminal. Every question and answer is saved in `answers_cli.csv`.

---

## ⚙️ Configuration Files

**.gitignore**
```
.venv/
__pycache__/
.env
answers.csv
answers.pdf
answers_cli.csv
.streamlit/secrets.toml
```

**runtime.txt**
```
python-3.11
```

**.streamlit/config.toml**
```
[theme]
primaryColor="#214B61"
secondaryBackgroundColor="#f9f9f9"
textColor="#222222"
```

---

## 🧰 Requirements

```
openai>=1.40.0
pandas>=2.2.0
reportlab>=4.2.0
streamlit>=1.36.0
python-dotenv>=1.0.1
```

---

## 📄 License

This project is provided for demonstration and educational purposes only.
All brand assets © BetterSure. The author is not affiliated with BetterSure.
