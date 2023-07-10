from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Publisher,Review,Book


class InstanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper=FormHelper()
        # post is default 
        if kwargs.get("instance"):
            button_title='Save'
        else:
            button_title="Create"
            
        self.helper.add_input(Submit("submit",button_title))
        

class BookMediaForm(InstanceForm):
    
    class Meta:
        model = Book
        fields = ("cover", "sample")


class ReviewForm(InstanceForm):
    rating=forms.IntegerField(min_value=0,max_value=5)
    class Meta:
        model=Review
        exclude = ['date_edited','book','creator']
        widgets={}
        

class PublisherForm(InstanceForm):
    class Meta:
        model=Publisher
        fields="__all__"
        
class SearchForm(forms.Form):
    # Using Django crispy forms
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.add_input(Submit("search", "Search"))
    search = forms.CharField(min_length=3,required=False)
    search_in = forms.ChoiceField(
        choices=(('title', 'Title'),
                ('contributor', 'Contributor')),
        required=False)
