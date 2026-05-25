
# Student Performance Analyzer

A comprehensive, real-time analytics and predictive machine learning dashboard built with **Python**, **Streamlit**, and **Scikit-Learn**. 

This application empowers educators to upload student data, instantly generate performance insights, segment students based on engagement behaviors, and predict future outcomes using advanced machine learning models.

## 🚀 Key Highlights
- **Dynamic File Uploads:** Seamlessly ingest CSV/Excel files into a Pandas DataFrame.
- **Interactive UI:** Built using Streamlit's modern `st.navigation` framework.
- **Predictive ML:** Train multiple classification models (Random Forest, Logistic Regression, Decision Tree, KNN) on the fly to predict Pass/Fail probabilities.
- **Risk Simulator:** A "What-If" sandbox for prescriptive analytics.
- **Unsupervised Learning:** Automatically segments students into behavioral clusters using K-Means.
- **Automated Reporting:** Generate and export PDF reports using `fpdf`.

## 🛠️ Tech Stack
- **Frontend & Routing:** Streamlit (Python)
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn
- **Data Visualization:** Plotly, Seaborn, Matplotlib
- **PDF Generation:** FPDF
- **Package Management:** `uv`

## 📦 Installation & Setup

This project uses [`uv`](https://github.com/astral-sh/uv), an extremely fast Python package and project manager written in Rust.

**0. Install `uv` (If you don't have it installed):**
The simplest way is via pip:
```bash
pip install uv
```
*(Alternatively, you can use the standalone installers:)*
- **Windows:** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

1. **Clone the Repository** (or navigate to your project directory).
2. **Initialize a Virtual Environment:**
   ```bash
   uv venv
   ```
3. **Activate the Virtual Environment:**
   - **Windows:**
     ```powershell
     .\.venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```
4. **Install Dependencies:**
   ```bash
   uv add numpy pandas streamlit scikit-learn matplotlib seaborn plotly fpdf
   ```
5. **Generate Sample Data** (if you don't have your own CSV):
   ```bash
   uv run python data_generator.py
   ```
   *This will create a `sample_students.csv` file with 200 synthesized student records.*
6. **Run the Application:**
   ```bash
   uv run streamlit run app.py
   ```
7. **Access the Dashboard** by navigating to `http://localhost:8501` in your browser.

## 📂 Project Structure
```
analyst/
│
├── app.py                      # Main Streamlit entry point and routing
├── data_generator.py           # Script to synthesize student datasets
├── pyproject.toml              # uv project configuration
├── sample_students.csv         # Generated dataset
│
├── utils/
│   └── data_processing.py      # Pandas data cleaning and KPI calculation logic
│
├── ml_models/
│   └── trainer.py              # Scikit-learn training, prediction, and clustering logic
│
└── pages/
    ├── 1_Dashboard.py          # Real-time KPIs and general data visualizations
    ├── 2_Student_Profiles.py   # Individual student search, radar charts, and AI feedback
    ├── 3_Machine_Learning.py   # ML Model training, accuracy charts, and risk simulation
    └── 4_Reports.py            # PDF and CSV export functionality
```

## 📝 Usage Guide
1. Launch the app and view the **Dashboard**.
2. On the left sidebar, upload a dataset or click **Load Default Sample Data**.
3. Explore the top-level KPIs (Class Average, Pass Rate).
4. Navigate to **Student Profiles** to search for specific students and view their attendance vs. marks gauge charts.
5. Go to **Machine Learning**, click `Train Models Now`, and explore feature importance and behavioral clustering. Use the **Risk Detection Simulator** to see how changing study habits affects outcomes.
6. Finally, visit the **Reports** tab to download a generated PDF of the class's performance.

---
*Developed for Interview Demonstrations & Advanced Analytics Portfolios.*
