from django.contrib import admin

from .models import Advert, Category, Comment, SubCategory


class AdvertAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'category', 'created')
    list_filter = ('created', 'price', 'category',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('name', 'category')
    prepopulated_fields = {"slug": ("name", )}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {"slug": ("name", )}


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'advert',
        'author',
        'text',
        'created'
    )
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Advert, AdvertAdmin)
