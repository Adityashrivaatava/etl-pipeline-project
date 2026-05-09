# 🚀 ETL Pipeline Project

An automated Python ETL (Extract, Transform, Load) pipeline that 
processes HR employee data with data quality reporting, 
daily scheduling, and Excel export.

---

## 📌 Features

- ✅ Extract data from CSV files using Pandas
- ✅ Transform & clean data (remove duplicates, nulls, standardize columns)
- ✅ Load cleaned data into SQLite database
- ✅ Generate Data Quality Report with quality score
- ✅ Auto-schedule pipeline to run daily at 9:00 AM
- ✅ Export cleaned data to Excel with 3 sheets:
  - Cleaned Data
  - Department Summary
  - Attrition Summary

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data extraction & transformation |
| SQLite | Database storage |
| OpenPyXL | Excel report generation |
| Schedule | Automated daily scheduling |
| Logging | Pipeline activity tracking |

---

## 📁 Project Structure

etl-pipeline-project/
├── data/
│   └── employee.csv        ← Input dataset
├── output/
│   ├── employees.db        ← SQLite database
│   └── HR_Report.xlsx      ← Excel report
├── logs/
│   ├── etl.log             ← Pipeline logs
│   └── quality_report.txt  ← Data quality report
└── etl_pipeline.py         ← Main pipeline script
---

## ⚙️ How to Run

**1. Clone the repository**
git clone https://github.com/Adityashrivaatava/etl-pipeline-project.git
cd etl-pipeline-project

**2. Install required libraries**
pip install pandas openpyxl schedule

**3. Add your dataset**
- Place your CSV file inside the `data/` folder
- Name it `employee.csv`

**4. Run the pipeline**
python etl_pipeline.py
---

## 📊 Sample Output
🚀 Starting ETL Pipeline...
✅ Extracted 1470 rows
✅ Transformed: 1470 clean rows
✅ Loaded 1470 rows into database
========================================
DATA QUALITY REPORT
Total Rows Extracted     : 1470
Duplicate Rows Removed   : 0
Null Values Found        : 0
Total Rows Removed       : 0
Clean Rows Remaining     : 1470
Data Quality Score       : 100.0%
✅ Quality report saved to logs/quality_report.txt
✅ Excel report saved to output/HR_Report_2026-05-09.xlsx
🎉 Pipeline completed successfully!

---

## 📂 Dataset

Dataset used: **IBM HR Analytics Employee Attrition & Performance**
Source: [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

---

## 👨‍💻 Author

**Aditya Shrivastava**
- GitHub: [@Adityashrivaatava](https://github.com/Adityashrivaatava)

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
