from django.contrib import admin

from .forms import SubCategoryForm
from .models import Advert, SubCategory, SuperCategory


class AdvertAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'category', 'pub_date')
    list_filter = ('pub_date', 'price', 'category',)


class SubCategoryInline(admin.TabularInline):
    model = SubCategory


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm


admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Advert, AdvertAdmin)
