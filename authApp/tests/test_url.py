from django.test import SimpleTestCase
from django.urls import reverse, resolve

from authApp.views import *
from django.contrib.auth.views import LogoutView, LoginView



class TestUrls(SimpleTestCase):

    def test_profile_page(self):
        url = reverse("authApp:profile", args=[1])

        self.assertEquals(resolve(url).func.view_class, CustomUserView)

    def test_edit_user_page(self):
        url = reverse("authApp:edit_user", args=[1])

        self.assertEquals(resolve(url).func.view_class, UserUpdateView)

    def test_logout_page(self):
        url = reverse("authApp:logout")

        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_login_page(self):
        url = reverse("authApp:login")

        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_sign_up_page(self):
        url = reverse("authApp:signup")

        self.assertEquals(resolve(url).func, registration_view)