from django import forms

from .models import Advert, SubCategory, SuperCategory


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(
        queryset=SuperCategory.objects.all(),
        empty_label=None,
        label='Категория',
        required=True
    )

    class Meta:
        model = SubCategory
        fields = '__all__'


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = (
            'title',
            'description',
            'price',
            'category',
            'main_category',
            'image'
        )
        labels = {'title': 'Название товара',
                  'description': 'Описание товара',
                  'price': 'Цена товара',
                  'category': 'Подкатегория',
                  'main_category': 'Категория'
                  }
        help_texts = {
            'title': 'Введите название товара',
            'description': 'Введите описание товара',
            'price': 'Введите цену товара',
            'main_category': 'Выберите категорию',
            'category': 'Выберите подкатегорию'
        }
