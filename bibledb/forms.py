from django import forms
from siteapps_v1.bibledb.models import Verse, Category, Entry, Tag
import re

class BibleVerseForm(forms.ModelForm):
    error_css_class = 'error'
    
    book = forms.ChoiceField(label='Full Book Name', choices=zip(Verse.objects.get_all_books(), Verse.objects.get_all_books()))
    chapter = forms.IntegerField(required=False, min_value=1, max_value=200, label='Chapter', widget=forms.TextInput(attrs={'size':1}))
    startverse = forms.IntegerField(required=False, min_value=1, max_value=200, label='Start Verse', widget=forms.TextInput(attrs={'size':1}))
    endverse = forms.IntegerField(required=False, min_value=1, max_value=200, label='End Verse', widget=forms.TextInput(attrs={'size':1}))
    
    class Meta:
        model = Entry
        fields = ['book','chapter','startverse','endverse']
        #exclude = ['notes','categories','tags', 'context_notes', 'title']
    
    def clean(self):
        keys = self.cleaned_data.keys()
        if 'startverse' in keys and 'endverse' in keys and 'chapter' in keys:
            if self.cleaned_data['endverse']:
                startverse_num = self.cleaned_data['startverse'].verse_ref
            else:
                startverse_num = None
            if self.cleaned_data['endverse']:
                endverse_num = self.cleaned_data['endverse'].verse_ref
            else:
                endverse_num = None
            chp_num = self.cleaned_data['chapter']
        else:
            return self.cleaned_data

        if startverse_num and endverse_num:
            if startverse_num > endverse_num:
                raise forms.ValidationError("Start verse must precede end verse!")
            if startverse_num == endverse_num:
                self.cleaned_data['endverse'] = None
        elif endverse_num:
            raise forms.ValidationError("Start verse must be specified")

        return self.cleaned_data
    
    def clean_book(self):
        """ Check for valid book name """
        book_name = self.cleaned_data['book']
        verse_count = Verse.objects.validate_book(book_name)
        
        if verse_count < 1:
            raise forms.ValidationError("Book %s does not exist!" % (book_name))
        return book_name
        
    def clean_chapter(self):
        """ Check that chapter number is valid """
        field_errors = self._errors.keys()
        chp_num = self.cleaned_data['chapter']
        
        # only proceed if book validation passed; otherwise causes quirky error behavior
        if chp_num and not 'book' in field_errors:
            book_name = self.cleaned_data['book']
            if chp_num:
                chp_count = Verse.objects.validate_chapter(book_name, chp_num)
                if chp_count < 1:
                    raise forms.ValidationError("Chapter %s is not valid" % (chp_num))
        return chp_num
    
    def clean_verse(self, verse_num):
        """ Check that verse num is valid """
        field_errors = self._errors.keys()
        
        # only proceed if no other errors were found in previous fields
        if verse_num and not 'book' in field_errors and not 'chapter' in field_errors:
            book_name = self.clean_book()
            chp_num = self.clean_chapter()
            v = Verse.objects.validate_verse(book_name, chp_num, verse_num)
            if v < 1:
                raise forms.ValidationError("Verse %s is not valid" % (verse_num))
            return Verse.objects.get(book__icontains=book_name, chapter_ref=chp_num, verse_ref=verse_num)
        return None
        
    def clean_startverse(self):
        if 'chapter' in self.cleaned_data.keys() and self.cleaned_data['chapter'] == None:
            if self.cleaned_data['startverse'] == None:
                return None
            else:
                raise forms.ValidationError("Chapter must be specified!")
        return self.clean_verse(self.cleaned_data['startverse'])
        
    def clean_endverse(self):
        if 'chapter' in self.cleaned_data.keys() and self.cleaned_data['chapter'] == None:
            if self.cleaned_data['endverse'] == None:
                return None
            else:
                raise forms.ValidationError("Chapter must be specified!")
        if self.cleaned_data['endverse']:
            return self.clean_verse(self.cleaned_data['endverse'])
        else:
            return None
            
class EntryForm(BibleVerseForm):
    chapter = forms.IntegerField(required=True, min_value=1, max_value=200, label='Chapter', widget=forms.TextInput(attrs={'size':1}))
    startverse = forms.IntegerField(required=True, min_value=1, max_value=200, label='Start Verse', widget=forms.TextInput(attrs={'size':1}))
    endverse = forms.IntegerField(required=False, min_value=1, max_value=200, label='End Verse', widget=forms.TextInput(attrs={'size':1}))
    context_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':4, 'cols':64}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':9, 'cols':64}), label='Reflections')
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    additional_tags = forms.CharField(max_length=256, required=False, label='Tags (Comma separated)')
    
    class Meta:
        model = Entry
        fields = ['book','chapter','startverse','endverse','categories','title','context_notes','notes','removed']
        
    def clean_categories(self):
        """ If multiple categories include uncategorized, remove uncategorized
        If no categories chosen, use uncategorized"""
        cats = self.cleaned_data['categories']
        if len(cats) < 1:
            self.cleaned_data['categories'] = Category.objects.filter(slug__iexact='uncategorized')
        else:
            for cat in cats:
                if cat.slug == 'uncategorized' or cat.slug == 'pending-categorization':
                    self.cleaned_data['categories'] = cats.exclude(slug__iexact=cat.slug)
                    break
        
            # make sure parent categories of subcategories are included
            parent_cats = None
            for cat in cats:
                if cat.parent != None and cat.parent not in cats:
                    if parent_cats == None:
                        parent_cats = Category.objects.filter(id=cat.parent.id)
                    else:
                        parent_cats = parent_cats | Category.objects.filter(id=cat.parent.id)
            if parent_cats:
                self.cleaned_data['categories'] = cats | parent_cats
        return self.cleaned_data['categories']

class AdminEntryForm(EntryForm):
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), required=False)
    
    class Meta:
        model = Entry
    
    def clean(self):
        """keys = self.cleaned_data.keys()
        if 'startverse' in keys and 'endverse' in keys and 'chapter' in keys:
            startverse_num = self.cleaned_data['startverse']
            endverse_num = self.cleaned_data['endverse']
            chp_num = self.cleaned_data['chapter']
        else:
            return self.cleaned_data

        if startverse_num and endverse_num:
            if startverse_num > endverse_num:
                raise forms.ValidationError("Start verse must precede end verse!")
            if startverse_num == endverse_num:
                self.cleaned_data['endverse'] = None
        elif endverse_num:
            raise forms.ValidationError("Start verse must be specified")"""
        
        super(AdminEntryForm, self).clean()
        # these lines no longer necessary because it is done in the clean_verse method in EntryForm Meta
        #self.cleaned_data['startverse'] = Verse.objects.get(book=self.cleaned_data['book'].capitalize(), chapter_ref=chp_num, verse_ref=startverse_num)
        #self.cleaned_data['endverse'] = Verse.objects.get(book=self.cleaned_data['book'].capitalize(), chapter_ref=chp_num, verse_ref=endverse_num)
        return self.cleaned_data
        
class VerseListForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    category = forms.CharField(max_length=64, required=True, label='Verse List Name')
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(category__iexact='Pending Categorization'), required=True, label='Create under', empty_label=None)
    
    class Meta:
        model = Category
        exclude = ['created_by','slug']
    
    def clean(self):
        return self.cleaned_data
        
    def clean_category(self):
        """ Check to see if it exists already """
        qs = Category.objects.filter(category__iexact=self.cleaned_data['category'])
        if len(qs) > 0:
            raise forms.ValidationError("This verse list already exists!")
        else:
            return self.cleaned_data['category']