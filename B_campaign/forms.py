from django import forms
from vailodb_b.models import Form_Section, Form_Field, Form_FieldChoice

def create_dynamic_form(form_id):
    form_fields = []
    try:
        form = Form.objects.get(pk=form_id)
        sections = form.sections.all()
        for section in sections:
            section_title = section.name
            fields = section.form_fields.all()
            for field in fields:
                field_type = field.field_type
                field_label = field.label
                field_options = None
                if field_type in ('radio', 'select', 'checkbox'):
                    field_options = [
                        (choice.choice_text, choice.choice_text)
                        for choice in field.form_fieldchoice_set.all()
                    ]
                field_obj = {
                    'label': field_label,
                    'required': False,  # Adjust as needed
                }
                if field_type == 'text':
                    field_obj['widget'] = forms.TextInput()
                elif field_type == 'password':
                    field_obj['widget'] = forms.PasswordInput()
                elif field_type == 'number':
                    field_obj['widget'] = forms.NumberInput()
                elif field_type == 'email':
                    field_obj['widget'] = forms.EmailInput()
                elif field_type == 'phone':
                    field_obj['widget'] = forms.TextInput()  # Adjust for phone formatting
                elif field_type == 'radio':
                    field_obj['widget'] = forms.RadioSelect(choices=field_options)
                elif field_type == 'checkbox':
                    field_obj['widget'] = forms.CheckboxInput()
                elif field_type == 'select':
                    field_obj['widget'] = forms.Select(choices=field_options)
                form_fields.append(forms.CharField(**field_obj))
    except Form.DoesNotExist:
        # Handle form not found case (e.g., raise an error or display a message)
        pass
    return type('DynamicForm', (forms.Form,), {'fields': form_fields})
