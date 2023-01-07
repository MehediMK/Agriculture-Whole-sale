from django import forms
from agro.models import ProductItem,Complain


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductItem
        fields = ('title','price','category','unit','quantity','description','image','post_type')

class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ('subject','description','status')
        