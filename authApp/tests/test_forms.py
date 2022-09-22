from django.test import TestCase

from authApp.forms import RegisterForm, CustomUserChangeForm

class TestForms(TestCase):

    def test_register_form(self):

        form = RegisterForm(data={
            "email": "test@test.pl",
            "password1": "test1993",
            "password2": "test1993"
        })

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        
        form = RegisterForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_edit_form(self):
        
        form = CustomUserChangeForm(data={
            "email": "test@test.pl"
        })

        self.assertTrue(form.is_valid())

    def test_edit_form_no_data(self):
        
        form = CustomUserChangeForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
