import pandas as pd
import sqlite3
import logging
import os
import schedule
import time
import openpyxl

# Setup logging
os.makedirs('logs', exist_ok=True)
os.makedirs('output', exist_ok=True)

logging.basicConfig(
    filename='logs/etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# EXTRACT
def extract(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Extracted {len(df)} rows")
        print(f"✅ Extracted {len(df)} rows")
        return df
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        raise

# TRANSFORM
def transform(df):
    try:
        original_rows = len(df)
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        df.columns = [col.strip().lower().replace(' ', '_') 
                      for col in df.columns]
        logging.info(f"Removed {original_rows - len(df)} bad rows")
        print(f"✅ Transformed: {len(df)} clean rows")
        return df
    except Exception as e:
        logging.error(f"Transform failed: {e}")
        raise
def generate_quality_report(original_df, cleaned_df):
    try:
        total_rows = len(original_df)
        cleaned_rows = len(cleaned_df)
        removed_rows = total_rows - cleaned_rows
        duplicate_rows = original_df.duplicated().sum()
        null_values = original_df.isnull().sum().sum()
        clean_percentage = round((cleaned_rows / total_rows) * 100, 2)

        report = f"""
========================================
        DATA QUALITY REPORT
========================================
Total Rows Extracted     : {total_rows}
Duplicate Rows Removed   : {duplicate_rows}
Null Values Found        : {null_values}
Total Rows Removed       : {removed_rows}
Clean Rows Remaining     : {cleaned_rows}
Data Quality Score       : {clean_percentage}%
========================================
        """

        print(report)

        # Save report to file
        with open('logs/quality_report.txt', 'w') as f:
            f.write(report)

        logging.info(f"Quality report generated. Score: {clean_percentage}%")
        print("✅ Quality report saved to logs/quality_report.txt")

    except Exception as e:
        logging.error(f"Report generation failed: {e}")
        raise
def export_to_excel(df):
    try:
        from datetime import datetime
        
        # Create filename with today's date
        date_today = datetime.now().strftime("%Y-%m-%d")
        file_name = f'output/HR_Report_{date_today}.xlsx'
        
        # Create Excel writer
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            
            # Sheet 1 - Full cleaned data
            df.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            # Sheet 2 - Department summary
            dept_summary = df.groupby('department').agg(
                Total_Employees=('department', 'count'),
                Avg_Age=('age', 'mean'),
                Avg_Monthly_Income=('monthlyincome', 'mean')
            ).round(2)
            dept_summary.to_excel(writer, sheet_name='Department Summary')
            
            # Sheet 3 - Attrition summary
            attrition_summary = df['attrition'].value_counts().reset_index()
            attrition_summary.columns = ['Attrition', 'Count']
            attrition_summary.to_excel(writer, sheet_name='Attrition Summary', index=False)

        logging.info(f"Excel report exported: {file_name}")
        print(f"✅ Excel report saved to {file_name}")

    except Exception as e:
        logging.error(f"Excel export failed: {e}")
        raise
# LOAD
def load(df, db_path, table_name='employees'):
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, 
                  if_exists='replace', index=False)
        conn.close()
        logging.info(f"Loaded {len(df)} rows into {table_name}")
        print(f"✅ Loaded {len(df)} rows into database")
    except Exception as e:
        logging.error(f"Load failed: {e}")
        raise

def run_pipeline():
    print("\n🚀 Starting ETL Pipeline...")
    original_df = extract('data/employee.csv')
    cleaned_df = transform(original_df.copy())
    load(cleaned_df, 'output/employees.db')
    generate_quality_report(original_df, cleaned_df)
    export_to_excel(cleaned_df)
    print("🎉 Pipeline completed successfully!")
# RUN
if __name__ == "__main__":
    print("⏰ Scheduler started - Pipeline will run every day at 9:00 AM")
    print("▶ Running pipeline once now for testing...")
    
    # Run once immediately for testing
    run_pipeline()
    
    # Schedule to run every day at 9:00 AM
    schedule.every().day.at("09:00").do(run_pipeline)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)