from django.contrib import admin
from siteapps_v1.bible_tidbits.models import Tidbit, Tag


admin.site.register(Tidbit)
admin.site.register(Tag)