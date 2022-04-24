from django.contrib import admin
from events.models import Event

class EventAdmin(admin.ModelAdmin):
    exclude = ('owner',)
    readonly_fields = ('owner',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)