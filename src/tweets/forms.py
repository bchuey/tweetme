from django import forms

from .models import Tweet

class TweetModelForm(forms.ModelForm):
    # add new fields here
    content = forms.CharField(label='',
                        widget=forms.Textarea(attrs={'placeholder':'Your tweet', 'class':'form-control'})
            )
    class Meta:
        model = Tweet
        # have to be explicit
        # with fields you want
        fields = [
            'content',
        ]

    # validations
    # clean_<field name>

    def clean_content(self, *args, **kwargs):
        content = self.cleaned_data.get('content')
        if content == 'abc':
            raise forms.ValidationError("Can not be abc")
        return content
