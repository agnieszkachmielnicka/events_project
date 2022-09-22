from django.test import SimpleTestCase

from events.forms import EventForm

class TestForms(SimpleTestCase):

    def test_event_create_form_valid_data(self):

        form = EventForm(data={
            'title': "koty",
            'description': "description",
            'event_date': "2022-09-23T10:00"
        })

        self.assertTrue(form.is_valid())

    def test_event_create_form_no_data(self):

        form = EventForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)