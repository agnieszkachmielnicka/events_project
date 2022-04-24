from django.urls import path
from events import views

app_name = 'events'

urlpatterns = [
    path('', views.ListEvent.as_view(), name='event_list'),
    path('create/', views.CreateEvent.as_view(), name='create_event'),
    path('edit/<pk>', views.EventUpdateView.as_view(), name='edit_event'),
    path('delete/<pk>', views.EventDeleteView.as_view(), name='delete_event'),
    path('join/<pk>', views.EventParticipantUpdateView.as_view(), name='join_event'),
    path('leave/<pk>', views.EventParticipantUpdateView.as_view(), name='leave_event'),
]
