from django.forms import ModelForm
from .models import Category, Listing

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'price', 'image']