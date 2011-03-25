from django import forms
from siteapps_v1.ntgreekvocab.models import SimpleCard
from siteapps_v1.ntgreekvocab import greek

class SimpleCardAdminForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'    

    definition = forms.CharField(widget=forms.Textarea(attrs={'rows':1,}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':1,}))
    hints = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':1,'placeholder':'mnemonics for this word'}))
    parsing_info = forms.CharField(required=False, widget=forms.TextInput())
    lesson_number = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = SimpleCard

    def clean(self):
        return self.cleaned_data

    def clean_parsing_info(self):
        """ Check to see if it exists already """
        text = self.cleaned_data['parsing_info'];
        if not text == '':
            words = text.split(',')
            for w in words:
                if not w.strip() in SimpleCard.PARSING_TERMS:
                    raise forms.ValidationError(u'Invalid parsing term "%s"' % w)
        return text

    def clean_lesson_number(self):
        """ must be between 1 and 34"""
        ln = self.cleaned_data['lesson_number']
        if not ln == '':
            if ln == '18A' or ln == '18a' or ln == '18b' or ln == '18B':
                return ln.upper()
            else:
                try:
                    ln = int(ln)
                except ValueError:
                    raise forms.ValidationError(u'Lesson number must be an integer; letters only allowed for 18A and 18B.')
                if ln < 1 or ln > 34:
                    raise forms.ValidationError(u'Lesson number must be between 1 and 34.')
        return str(ln)

    def clean_greek_word(self):
        """ replace accented chars with logos keyboard equivalent unicode"""
        word = self.cleaned_data['greek_word'].strip()
        replacement = greek.replace_accented_characters(word)
        return replacement