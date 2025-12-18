import csv
from db.database import Database

class ReportService:
    @staticmethod
    def sales_report_csv(filename='sales_report.csv'):
        db = Database()
        rows = db.fetch_all('SELECT * FROM sales')

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Date', 'Total'])
            writer.writerows(rows)

        return filename