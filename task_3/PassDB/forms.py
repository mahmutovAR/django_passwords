from django import forms
from .models import AddPass


class AddPassForm(forms.ModelForm):
    class Meta:
        model = AddPass
        fields = '__all__'


# class AddNewPass(forms.Form):
#     data_file = forms.FileField(label='Open ".json" file with passwords')
#
#
# class PassTitle(forms.Form):
#     # main_titles = ((1, 'Cards'), (2, 'Logins'), (3, 'Notes'))
#     # user_select = forms.ChoiceField(choices=main_titles)
#     selected_title = forms.TypedChoiceField(label='Password title:',
#                                             empty_value=None,
#                                             choices=((1, 'Cards'),
#                                                      (2, 'Logins'),
#                                                      (3, 'Notes')))
