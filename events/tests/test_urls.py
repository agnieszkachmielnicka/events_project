from django.test import SimpleTestCase
from django.urls import reverse, resolve
from events.views import *

class TestUrls(SimpleTestCase):

    def test_list_event_page(self):

        url = reverse("events:event_list")
        self.assertEquals(resolve(url).func.view_class, ListEvent)

    def test_create_event_page(self):

        url = reverse("events:create_event")
        self.assertEquals(resolve(url).func.view_class, CreateEvent)

    def test_edit_event_page(self):

        url = reverse("events:edit_event", args=[1])
        self.assertEquals(resolve(url).func.view_class, EventUpdateView)

    def test_delete_event_page(self):

        url = reverse("events:delete_event", args=[1])
        self.assertEquals(resolve(url).func.view_class, EventDeleteView)

    def test_join_event_page(self):

        url = reverse("events:join_event", args=[1])
        self.assertEquals(resolve(url).func.view_class, EventParticipantUpdateView)

    def test_leave_event_page(self):

        url = reverse("events:leave_event", args=[1])
        self.assertEquals(resolve(url).func.view_class, EventParticipantUpdateView)