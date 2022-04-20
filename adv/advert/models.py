from django.contrib.auth import get_user_model
from django.db import models

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
    super_category = models.ForeignKey(
        'SuperCategory',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Категория'
    )


class SuperCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return '%s - %s' % (self.super_category.name, self.name)

    class Meta:
        proxy = True
        ordering = ('super_category__order', 'super_category__name', 'order',
                    'name')
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Advert(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        default=0,
        max_digits=19,
        decimal_places=2,
        verbose_name='Цена'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='adverts',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    category = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        verbose_name='Подкатегория',
        related_name='subcategory_adverts'
    )
    main_category = models.ForeignKey(
        SuperCategory,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='category_adverts'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='media/',
        blank=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
