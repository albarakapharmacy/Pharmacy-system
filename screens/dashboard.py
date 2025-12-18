from kivy.uix.screenmanager import Screen
from services.ai_service import AIService

class DashboardScreen(Screen):
    def load_ai(self):
        suggestions = AIService.suggest_reorder()
        for s in suggestions:
            print('اقترح شراء:', s)