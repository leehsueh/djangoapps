from django.contrib import admin
from siteapps_v1.ntgreekvocab.models import SimpleCard
from siteapps_v1.ntgreekvocab.forms import SimpleCardAdminForm

class SimpleCardAdmin(admin.ModelAdmin):
    form = SimpleCardAdminForm
    fieldsets = [
        ('Greek Word', {'fields': ['greek_word','part_of_speech', 'definition']}),
        ('More Information', {'fields': ['lesson_number', 'hints', 'parsing_info','notes'], 'classes': ['collapse',]}),
        ('Related Cards', {'fields': ['related_cards']})
    ]
    list_display = ['id', '__unicode__', 'definition', 'lesson_number']
    list_display_links = ['id', '__unicode__',]
    search_fields = ['greek_word', 'definition', 'parsing_info', 'notes']

admin.site.register(SimpleCard, SimpleCardAdmin)