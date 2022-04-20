from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from users.forms import User

from .forms import AdvertForm
from .models import Advert, SubCategory, SuperCategory


def index(request):
    categories = SuperCategory.objects.all()
    subcategories = SubCategory.objects.all()
    adverts = Advert.objects.all()
    paginator = Paginator(adverts, settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'categories': categories,
        'subcategories': subcategories,
        'page_obj': page_obj,
    }
    return render(request, 'advert/index.html', context)


def category_adverts(request, slug):
    category = get_object_or_404(SuperCategory, slug=slug)
    subcategories = SubCategory.objects.filter(super_category__isnull=False)
    adverts = Advert.objects.filter(main_category=category)
    paginator = Paginator(adverts, settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'subcategories': subcategories,
        'page_obj': page_obj
    }
    return render(request, 'advert/category_adverts.html', context)


def subcategory_list(request, category, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    subcategories = SubCategory.objects.filter(super_category__isnull=False)
    category = get_object_or_404(SuperCategory, slug=category)
    adverts = Advert.objects.filter(category=subcategory)
    paginator = Paginator(adverts, settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'adverts': adverts,
        'category': category,
        'subcategories': subcategories,
        'subcategory': subcategory,
        'page_obj': page_obj
    }
    return render(request, 'advert/subcategory_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    paginator = Paginator(author.adverts.all(), settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = SuperCategory.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
      'page_obj': page_obj,
      'categories': categories,
      'subcategories': subcategories,
    }
    return render(request, 'advert/profile.html', context)


def advert_detail(request, category, subcategory, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    subcategories = SubCategory.objects.filter(super_category__isnull=False)
    context = {
        'advert': advert,
        'subcategories': subcategories
    }
    return render(request, 'advert/advert_detail.html', context)


@login_required
def advert_create(request):
    is_edit = True
    form = AdvertForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('advert:profile', request.user.username)
    return render(
        request,
        'advert/create_advert.html',
        context={
            'form': form,
            'is_edit': is_edit
        }
    )


@login_required
def advert_edit(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    is_edit = False
    if advert.author != request.user:
        return redirect(
            'advert:advert_detail',
            category=advert.main_category.slug,
            subcategory=advert.category.slug,
            advert_id=advert.id
        )
    form = AdvertForm(
        request.POST or None,
        files=request.FILES or None,
        instance=advert
    )
    if form.is_valid():
        form.save()
        return redirect(
            'advert:advert_detail',
            category=advert.main_category.slug,
            subcategory=advert.category.slug,
            advert_id=advert.id
        )
    return render(
        request,
        'advert/create_advert.html',
        context={
            'form': form,
            'is_edit': is_edit,
            'advert': advert
        }
    )


def search(request):
    categories = SuperCategory.objects.all()
    subcategories = SubCategory.objects.all()
    results = []
    query = request.GET.get('q', '')
    if query:
        qset = Q(title__icontains=query)
        results = Advert.objects.filter(qset).distinct()
    context = {
        'query': query,
        'results': results,
        'categories': categories,
        'subcategories': subcategories
        }
    return render(
        request,
        'advert/search.html',
        context
        )
