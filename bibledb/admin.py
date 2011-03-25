from django.contrib import admin
from siteapps_v1.bibledb.models import Verse, Category, Entry, Tag, FAQ, UIString, StaticContent, Update
from siteapps_v1.bibledb.forms import AdminEntryForm

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category",)}
    list_display = ['category', 'parent', 'created_by']
    
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class EntryAdmin(admin.ModelAdmin):
    form = AdminEntryForm
    fieldsets = [
        ('Linked Verses', {'fields': ['book','chapter', 'startverse', 'endverse']}),
        ('Entry Info', {'fields': ['title','context_notes','notes', 'created_by', 'removed']}),
        ('Categories and Tags', {'fields': ['categories','tags'], 'classes': []}),
    ]
    list_display = ['pub_date','title', 'startverse', 'endverse', 'created_by']
    search_fields = ['categories', 'tags', 'notes', 'created_by']

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Verse)
admin.site.register(Tag, TagAdmin)
admin.site.register(FAQ)
admin.site.register(UIString)
admin.site.register(StaticContent)
admin.site.register(Update)