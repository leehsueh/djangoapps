from django.forms.widgets import TextInput, MultiWidget
from django.utils.datastructures import MultiValueDict, MergeDict

class MultipleTextInput(TextInput):
    """
    A widget that handles <input type="text"> for fields that have a list
    of values.
    """
    def __init__(self, attrs=None, choices=()):
        super(MultipleTextInput, self).__init__(attrs)
        # choices can be any iterable
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                # An ID attribute was given. Add a numeric index as a suffix
                # so that the inputs don't all have the same ID attribute.
                input_attrs['id'] = '%s_%s' % (id_, i)
            inputs.append(u'<input%s />' % flatatt(input_attrs))
        inputs.append(u'\n<button id="add_cf">Add</button>')
        return mark_safe(u'\n'.join(inputs))

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)