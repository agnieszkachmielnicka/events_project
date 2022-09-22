from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from authApp.models import CustomUser

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_profile_GET_no_user(self):
        profile_url = reverse("authApp:profile", args=[1])

        response = self.client.get(profile_url)

        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, "authApp/profile.html")

    def test_profile_GET(self):
        profile_url = reverse("authApp:profile", args=[1])

        user = CustomUser.objects.create(email='kot@kot.pl')
        user.set_password("adastra1993")
        user.save()

        self.client.login(username='kot@kot.pl', password="adastra1993")

        response = self.client.get(profile_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "authApp/profile.html")

    def test_signup_GET(self):
        signup_url = reverse("authApp:signup")

        response = self.client.get(signup_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "authApp/signup.html")

    def test_signup_POST(self):
        signup_url = reverse("authApp:signup")

        response = self.client.post(signup_url, {
            'email': 'test@test.pl',
            'password1': 'test1993',
            'password2': 'test1993'
        })

        try:
            CustomUser.objects.get(id=1)
            exist = True
        except ObjectDoesNotExist:
            exist = False

        self.assertEquals(response.status_code, 200)
        self.assertTrue(exist)

    def test_login_GET(self):
        login_url = reverse("authApp:login")

        response = self.client.get(login_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "authApp/login.html")

    def test_login_POST(self):
        login_url = reverse("authApp:login")

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        response = self.client.post(login_url, {
            'username': 'test@test.pl',
            'password': 'test1993',
        })

        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertEquals(response.status_code, 302)

    def test_logout_GET(self):
        logout_url = reverse("authApp:logout")

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        self.client.login(username="test@test.pl", password="test1993")

        response = self.client.get(logout_url)

        self.assertFalse(True if '_auth_user_id' in self.client.session else False)
        self.assertEquals(response.status_code, 302)

    def test_user_update_GET_no_user(self):
        update_url = reverse("authApp:edit_user", args=[1])

        response = self.client.get(update_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, "authApp/edit_user.html")

    def test_user_update_GET(self):
        update_url = reverse("authApp:edit_user", args=[1])

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        self.client.login(username="test@test.pl", password="test1993")

        response = self.client.get(update_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "authApp/edit_user.html")

    def test_user_update_POST(self):
        update_url = reverse("authApp:edit_user", args=[1])

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        self.client.login(username="test@test.pl", password="test1993")

        response = self.client.post(update_url, {
            'email': 'test1@test1.pl'
        })

        user_updated = CustomUser.objects.get(id=1)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(user_updated.email, "test1@test1.pl")

