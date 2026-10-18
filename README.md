# DataDoctor 🩺

A modern Streamlit web application that detects data quality issues, cleans datasets, and exports reliable results. Upload a CSV or Excel file and let DataDoctor handle the rest.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white)

## Features

### Data Cleaning

- **Trim whitespace** — strips leading/trailing spaces from text columns
- **Collapse multiple spaces** — reduces consecutive spaces inside text to a single space
- **Remove duplicate rows** — drops exact duplicate records
- **Standardize column names** — lowercases and replaces spaces with underscores
- **Drop sparse columns** — removes columns exceeding a configurable missing-value threshold
- **Fill missing values** — median, mean, or most-frequent-value strategies
- **Normalize categories** — unifies inconsistent capitalization variants
- **Outlier detection (IQR)** — flags or removes statistical outliers in numeric columns

### Validation

- **Auto type detection** — heuristically detects Number, Date, Email, Phone, URL, and Category columns
- **Type-specific validation** — checks values against expected formats and flags mismatches
- **Domain rules** — flags negative ages, out-of-range scores/marks, invalid emails, phone numbers, and URLs
- **Detailed issue report** — row-level log of every detected problem with downloadable CSV

### UI / UX

- **Dark / Light theme** — toggle in the sidebar with smooth CSS transitions
- **Modern elegant design** — soft shadows, rounded cards, teal accent, styled components
- **Sidebar-driven workflow** — upload, configure, and review without page clutter
- **Column statistics** — per-column dtype, null count, unique values, and numeric summaries
- **Before & After comparison** — tabbed view of original vs. cleaned data
- **Multiple export formats** — download cleaned data as CSV or Excel, plus validation report and change log

## Getting Started

### Prerequisites

- Python 3.9 or higher

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/DataDoctor.git
   cd DataDoctor
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run app.py
   ```

4. Open the URL shown in the terminal (usually `http://localhost:8501`).

## Usage

1. **Upload** a `.csv` or `.xlsx` file via the sidebar.
2. **Configure** cleaning options, missing-value strategy, and validation rules in the sidebar expanders.
3. **Review** the original dataset overview, column statistics, and validation report in the main area.
4. **Compare** the before-and-after data in the tabbed view.
5. **Download** the cleaned dataset (CSV or Excel), validation report, or change log.

## Project Structure

```
DataDoctor/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

## Dependencies

| Package    | Purpose                        |
| ---------- | ------------------------------ |
| streamlit  | Web application framework      |
| pandas     | Data manipulation and analysis |
| openpyxl   | Excel file read/write support  |

## License

This project is open source and available under the [MIT License](LICENSE).
=======
# DataDoctor
DataDoctor is a Python-based data cleaning and validation app built with Pandas and Streamlit. It detects missing values, duplicates, invalid data types, incorrect emails and dates, and helps clean datasets with downloadable reports.

