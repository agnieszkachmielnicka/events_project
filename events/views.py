from django.http import HttpResponseRedirect
from events.models import Event
from django.views import generic
from django.urls import reverse_lazy
from events.forms import EventForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ListEvent(generic.ListView):
    model = Event
    queryset = Event.objects.select_related('owner').prefetch_related('participants').all().order_by('event_date')
    paginate_by = 3

class CreateEvent(LoginRequiredMixin, generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create_event.html'
    login_url = '/account/login/'

    def get_success_url(self):
        return reverse_lazy('events:event_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/create_event.html'
    login_url = '/account/login/'

    def get_success_url(self):
        return reverse_lazy('events:event_list')

class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Event
    success_url = '/'
    login_url = '/account/login/'

class EventParticipantUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Event
    queryset = Event.objects.prefetch_related('participants').all()
    fields = ('participants',)
    template_name = 'events/join_event.html'
    login_url = '/account/login/'

    def get_success_url(self):
        return reverse_lazy('events:event_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        if ('join' in self.request.path):
            obj.participants.add(self.request.user)
        elif ('leave' in self.request.path):
            obj.participants.remove(self.request.user)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())