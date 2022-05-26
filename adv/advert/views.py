from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import User

from .forms import AdvertForm, CommentForm
from .models import Advert, Category, Comment, SubCategory


def index(request):
    categories = Category.objects.all()
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
    category = get_object_or_404(Category, slug=slug)
    subcategories = SubCategory.objects.filter(category=category)
    adverts = Advert.objects.filter(category=category)
    paginator = Paginator(adverts, settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'subcategories': subcategories,
        'page_obj': page_obj,
        'const': False
    }
    return render(request, 'advert/category_adverts.html', context)


def subcategory_list(request, category, slug):
    subcategory = get_object_or_404(SubCategory, slug=slug)
    subcategories = SubCategory.objects.all()
    category = get_object_or_404(Category, slug=category)
    adverts = Advert.objects.filter(subcategory=subcategory)
    paginator = Paginator(adverts, settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'adverts': adverts,
        'category': category,
        'subcategories': subcategories,
        'subcategory': subcategory,
        'page_obj': page_obj,
        'const': True
    }
    return render(request, 'advert/subcategory_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    paginator = Paginator(author.adverts.all(), settings.PAGE_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    context = {
      'author': author,
      'page_obj': page_obj,
      'categories': categories,
      'subcategories': subcategories,
    }
    return render(request, 'advert/profile.html', context)


def advert_detail(request, category, subcategory, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    form = CommentForm()
    comments = advert.comments.all()
    category = get_object_or_404(Category, slug=category)
    subcategory = advert.subcategory
    subcategories = SubCategory.objects.filter(category=advert.category)
    context = {
        'advert': advert,
        'category': category,
        'subcategory': subcategory,
        'subcategories': subcategories,
        'const': True,
        'form': form,
        'comments': comments
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
            category=advert.category.slug,
            subcategory=advert.subcategory.slug,
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
            category=advert.category.slug,
            subcategory=advert.subcategory.slug,
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


@login_required
def advert_delete(request, username, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    if request.user == advert.author:
        advert.delete()
        return redirect('advert:profile', username=username)
    return redirect(
            'advert:advert_detail',
            category=advert.category.slug,
            subcategory=advert.subcategory.slug,
            advert_id=advert.id
        )


@login_required
def add_comment(request, category, subcategory, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.advert = advert
        comment.save()
    return redirect(
            'advert:advert_detail',
            category=advert.category.slug,
            subcategory=advert.subcategory.slug,
            advert_id=advert.id
        )


@login_required
def delete_comment(request, category, subcategory, advert_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    advert = get_object_or_404(Advert, id=advert_id)
    if request.user == comment.author:
        comment.delete()
    return redirect(
            'advert:advert_detail',
            category=advert.category.slug,
            subcategory=advert.subcategory.slug,
            advert_id=advert.id
        )


def search(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    results = []
    query = request.GET.get('q', '')
    if query:
        qset = Q(title__icontains=query)
        results = Advert.objects.filter(qset).distinct()
        paginator = Paginator(results, settings.PAGE_COUNT)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    context = {
        'query': query,
        'results': results,
        'categories': categories,
        'subcategories': subcategories,
        'page_obj': page_obj
        }
    return render(
        request,
        'advert/search.html',
        context
        )
