from django import forms

from .models import Advert, Comment


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = (
            'title',
            'description',
            'price',
            'phonenumber',
            'category',
            'subcategory',
            'image'
        )
        labels = {'title': 'Название товара',
                  'description': 'Описание товара',
                  'price': 'Цена товара',
                  'phonenumber': 'Номер телефона',
                  'subcategory': 'Подкатегория',
                  'category': 'Категория'
                  }
        help_texts = {
            'title': 'Введите название товара',
            'description': 'Введите описание товара',
            'price': 'Введите цену товара',
            'phonenumber': 'Введите Ваш номер телефона',
            'category': 'Выберите категорию',
            'subategory': 'Выберите подкатегорию'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
