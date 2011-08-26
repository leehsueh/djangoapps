from django.contrib import admin
from siteapps_v1.bible_tidbits.models import Tidbit, Tag

class TagAdmin(admin.ModelAdmin):
	search_fields = ['tag', 'category']

admin.site.register(Tidbit)
admin.site.register(Tag, TagAdmin)