from kivy.uix.screenmanager import Screen
from services.auth_service import AuthService

class LoginScreen(Screen):
    def do_login(self, user, pwd):
        u = AuthService.login(user, pwd)
        if u:
            print('تم الدخول:', u)
        else:
            print('فشل الدخول')
