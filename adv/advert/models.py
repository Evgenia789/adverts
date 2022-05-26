from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from core.models import CreatedModel

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    order = models.SmallIntegerField(
        default=0,
        db_index=True,
        verbose_name='Порядок'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=20, db_index=True, unique=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    order = models.SmallIntegerField(
        default=0,
        db_index=True,
        verbose_name='Порядок'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='subcategory',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('category__order', 'category__name', 'order',
                    'name')

    def __str__(self):
        return '%s - %s' % (self.category.name, self.name)


class Advert(CreatedModel):
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(
        default=0,
        verbose_name='Цена'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='adverts',
        verbose_name='Автор'
    )
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phonenumber = models.CharField(validators=[phoneNumberRegex], max_length=12)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='category_adverts'
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        related_name='subcategory_adverts'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='media/',
        blank=True
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Comment(CreatedModel):
    advert = models.ForeignKey(
        Advert,
        on_delete=models.CASCADE,
        related_name='comments',
        max_length=200,
        verbose_name='Текст объявления'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        max_length=200,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст вопроса о товаре',
                            help_text="Задайте вопрос о товаре продавцу",
                            )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Вопрос о товаре'
        verbose_name_plural = 'Вопросы о товаре'
