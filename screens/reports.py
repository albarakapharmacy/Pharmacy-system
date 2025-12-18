from kivy.uix.screenmanager import Screen
from services.report_service import ReportService

class ReportsScreen(Screen):
    def export_sales(self):
        file = ReportService.sales_report_csv()
        print('Report exported:', file)