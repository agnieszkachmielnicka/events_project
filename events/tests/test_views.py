from django.urls import reverse
from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

from authApp.models import CustomUser
from events.models import Event

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse("events:event_list")
        self.create_url = reverse("events:create_event")
        self.login_url = reverse("authApp:login")
        self.create_url = reverse("events:create_event")
        self.edit_url = reverse("events:edit_event", args=[1])
        self.delete_url = reverse("events:delete_event", args=[1])
        self.join_url = reverse("events:join_event", args=[1])
        self.leave_url = reverse("events:leave_event", args=[1])

    def test_event_list_GET(self):

        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')

    def test_create_event_GET_not_logged_in(self):

        response = self.client.get(self.create_url)

        self.assertEquals(response.status_code, 302)

    def test_create_event_GET(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        self.client.login(username='test@test.pl', password="test1993")

        response = self.client.get(self.create_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "events/create_event.html")

    def test_create_event_POST(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        self.client.login(username='test@test.pl', password="test1993")

        response = self.client.post(self.create_url, {
            'title': "event1",
            'description': "description",
            'event_date': "2022-09-23T10:00"
        })

        self.assertEquals(response.status_code, 302)

        event = Event.objects.get(id=1)
        self.assertEquals(event.title, "event1")

    def test_update_event_GET(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test@test.pl', password="test1993")

        response = self.client.get(self.edit_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "events/create_event.html")

    def test_update_event_POST(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test@test.pl', password="test1993")

        response = self.client.post(self.edit_url, {
            'title': "koty",
            'description': "description",
            'event_date': "2022-09-23T10:00"
        })

        event_updated = Event.objects.get(id=1)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(event_updated.title, "koty")

    def test_delete_event_DELETE(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test@test.pl', password="test1993")

        response = self.client.delete(self.delete_url)

        try:
            Event.objects.get(id=1)
            exist = True
        except ObjectDoesNotExist: 
            exist = False

        self.assertEquals(response.status_code, 302)
        self.assertFalse(exist)

    def test_join_event_GET(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        user1 = CustomUser.objects.create(email='test1@test1.pl')
        user1.set_password("test1993")
        user1.save()

        Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test1@test1.pl', password="test1993")

        response = self.client.get(self.join_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "events/join_event.html")

    def test_join_event_POST(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        user1 = CustomUser.objects.create(email='test1@test1.pl')
        user1.set_password("test1993")
        user1.save()

        event1 = Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test1@test1.pl', password="test1993")

        response = self.client.post(self.join_url, {})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(event1.participants.count(), 1)

    def test_leave_event_GET(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        user1 = CustomUser.objects.create(email='test1@test1.pl')
        user1.set_password("test1993")
        user1.save()

        Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test1@test1.pl', password="test1993")

        response = self.client.get(self.leave_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "events/join_event.html")

    def test_leave_event_POST(self):

        user = CustomUser.objects.create(email='test@test.pl')
        user.set_password("test1993")
        user.save()

        user1 = CustomUser.objects.create(email='test1@test1.pl')
        user1.set_password("test1993")
        user1.save()

        event1 = Event.objects.create(owner=user, title="event1",
                            description="description", event_date="2022-09-23 10:00")

        self.client.login(username='test1@test1.pl', password="test1993")

        event1.participants.add(user1)
        event1.save()

        response = self.client.post(self.leave_url, {})

        self.assertEquals(response.status_code, 302)
        self.assertEquals(event1.participants.count(), 0)