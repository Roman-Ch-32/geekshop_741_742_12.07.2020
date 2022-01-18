from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView

from adminapp.forms import ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm, UserProfilerForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test


def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context)


def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'update_form': user_form
    }

    return render(request, 'adminapp/user_update.html', context)


def user_update(request, pk):
    title = "пользователи/обновление"
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = UserProfilerForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid:
            edit_form.save()
            return HttpResponseRedirect(reverse("admin_staff:users"))
    else:
        edit_form = UserProfilerForm(instance=user)

    context = {
        "title": title,
        "update_form": edit_form
    }

    return render(request, "adminapp/user_update.html", context)


def user_delete(request, pk):
    title = "удаление"

    user = get_object_or_404(ShopUser, pk=pk)

    context = {
        'title': title,
        'user_delete': user
    }

    if request.method == "POST":
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse("admin_staff:users"))
        
    return render(request, "adminapp/user_update.html", context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


def category_create(request):
    title = "админка/создание категории"

    categories_list = ProductCategory.objects.all()
    new_category = ProductCategoryEditForm(request.POST, request.FILES)
    
    context = {
        "title": title,
        "categories_list": categories_list,
        "new_category": new_category,
    }

    if request.method == 'POST':
        if new_category.is_valid:
            new_category.save()
            return HttpResponseRedirect(reverse("admin_staff:categories"))
        else:
            return HttpResponseRedirect(reverse(("admin_staff:create")))
    
    return render(request, "adminapp/create.html", context)


def category_update(request, pk):
    title = "категории обновление"

    category = get_object_or_404(ProductCategory, pk=pk)
    category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=category)

    context = {
        "title": title,
        "category": category,
        "category_form": category_form,
    }

    if request.method == "POST":
        if category_form.is_valid:
            category.save()
            return HttpResponseRedirect(reverse("admin_staff.categories"))
        else:
            return HttpResponseRedirect(reverse(("admin_staff:create")))

    return render(request, 'adminapp/create.html', context)


def category_delete(request, pk):
    title = "удаление"
    category = get_object_or_404(ProductCategory, pk=pk)
    categories_list = ProductCategory.objects.all()
    context = {
        "title": title,
        "category": category,
        'objects': categories_list,
    }
    if request.method == "POST":
        if category.is_active is True:
            category.is_active = False
            category.save()
            return HttpResponseRedirect(reverse("admin_staff.categories"))
        else:
            return HttpResponseRedirect(reverse("admin_staff.categories"))

    return render(request, 'adminapp/categories.html', context)


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    title = 'продукты/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'update_form': product_form,
        'category': category,
    }
    return render(request, 'adminapp/product_update.html', context)


def product_read(request, pk):
    title = 'продукты/подробнее'
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'product': product,
    }
    return render(request, 'adminapp/product_read.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get(self, request, *args, **kwargs):
        print(request)


def product_update(request, pk):
    title = 'продукты/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category,
    }
    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        product.is_active = False if product.is_active else True
        product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))
