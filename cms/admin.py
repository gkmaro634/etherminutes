from django.contrib import admin
from cms.models import Minutes

# Register your models here.


class MinutesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
admin.site.register(Minutes, MinutesAdmin)
