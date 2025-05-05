from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Farm, Product, Review, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'saved_farms']
        widgets = {
            'saved_farms': forms.CheckboxSelectMultiple
        }

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'description', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock', 'category', 'image', 'description']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES)
        }

@login_required
def add_review(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'core/add_review.html', {'form': form})