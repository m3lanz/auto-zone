from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from .const import *
from .forms import *
from .utils import delete_selected_images


class HomeView(ListView):
    model = Car
    template_name = 'cardealership/index.html'
    context_object_name = 'cars'
    extra_context = {'title': 'Homepage'}
    ordering = ['-added_at']
    paginate_by = 3

    def get_queryset(self):
        queryset = Car.objects.all()

        brand = self.request.GET.get('brand')
        transmission = self.request.GET.get('transmission')
        fuel_types = self.request.GET.getlist(
            'fuel_type')  # отправляем списком, чтобы пользователь мог выбрать сразу несколько типов
        body_types = self.request.GET.getlist('body_type')
        sort = self.request.GET.get('sort')
        query = self.request.GET.get('q') or ''

        if sort:
            queryset = queryset.order_by(sort)

        if brand:
            queryset = queryset.filter(brand__name=brand)  # привязанное поле к модели Brand

        if transmission:
            queryset = queryset.filter(transmission=transmission)

        if fuel_types:
            queryset = queryset.filter(fuel_type__in=fuel_types)  # если тип топлива есть в списке

        if body_types:
            queryset = queryset.filter(body_type__in=body_types)  # тоже самое

        if query:

            for word in query.split():
                queryset = queryset.filter(
                    Q(brand__name__icontains=word) |
                    Q(model__icontains=word)
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['brands'] = Brand.objects.all()

        context['selected_brand'] = self.request.GET.get('brand')
        context['selected_transmission'] = self.request.GET.get('transmission')

        context['fuel_types'] = FUEL_TYPES
        context['body_types'] = BODY_TYPES

        context["selected_fuel_types"] = self.request.GET.getlist("fuel_type")
        context['selected_body_types'] = self.request.GET.getlist("body_type")

        context['selected_sort'] = self.request.GET.get('sort')

        if self.request.user.is_authenticated:
            favorite_ids = set(Favorite.objects.filter(user=self.request.user).values_list('car_id', flat=True))
        else:
            favorite_ids = set()

        context['favorite_ids'] = favorite_ids

        return context


class CarDetailView(DetailView):
    model = Car
    template_name = 'cardealership/car_detail.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object

        context['specs'] = {
            'Transmission': car.transmission,
            'Released at': car.release_date,
            'Color': car.colors_available,
            'Fuel Type': car.fuel_type,
            'Horsepower': car.horsepower,
            'Body Type': car.body_type,
            'Mileage': f'{car.mileage} km'
        }

        context['comment_form'] = CommentForm()

        if self.request.user.is_authenticated:
            context['is_active'] = Favorite.objects.filter(
                car=car, user=self.request.user
            ).exists()
        else:
            context['is_active'] = False

        return context


class LoginUserView(LoginView):
    template_name = 'cardealership/login.html'
    authentication_form = LoginUserForm


class LogoutUserView(LogoutView):
    pass


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = RegisterUserForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                profile = ProfileUser.objects.create(user=user)
                profile.save()
                login(request, user)
                return redirect('main')
        else:
            form = RegisterUserForm()

        context = {
            'title': 'Registration',
            'form': form
        }

        return render(request, 'cardealership/register.html', context)


def profile_user_view(request, username):
    if request.user.is_authenticated:
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            profile = ProfileUser.objects.get(user=user)
            listings = Car.objects.filter(seller__username=user.username)
            context = {
                'title': f"{user.username}'s profile",
                'profile_user': user,
                'profile': profile,
                'user_form': EditUserForm(instance=request.user),
                'profile_form': EditProfileForm(instance=request.user.profile),
                'password_change': PasswordChangeForm(request.user),
                'user_listings': listings,
            }

            return render(request, 'cardealership/profile_page.html', context)

        else:
            return redirect('main')

    else:
        return redirect('login')


def edit_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        user_form = EditUserForm(data=request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.user.username)
    elif request.method == 'GET':
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    return render(request, 'cardealership/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def edit_password_user(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        password_form = ChangeUserPasswordForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect('profile', username=request.user.username)
    else:
        password_form = ChangeUserPasswordForm(request.user)

    return render(request, 'cardealership/edit_password.html', {
        'password_form': password_form
    })


# class CreateListingView(LoginRequiredMixin, CreateView):
#     model = Car
#     form_class = CreateListingForm
#     image_form = CreateImageListingForm
#     template_name = 'cardealership/create_listing.html'
#
#     def form_valid(self, form):
#         form.instance.seller = self.request.user
#         response = super().form_valid(form)
#
#         for image in self.request.FILES.getlist('images'):
#             CarImage.objects.create(car=self.object, image=image)
#
#         return response
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         context['creation_form'] = self.form_class()
#         context['image_form'] = self.image_form
#
#         return context


@login_required  # декоратор, отвечающий за авторизацию
def create_listing_view(request):
    if request.method == 'POST':
        listing_form = CreateListingForm(request.POST)
        image_form = CreateImageListingForm(request.POST, request.FILES)

        if listing_form.is_valid() and image_form.is_valid():
            car = listing_form.save(commit=False)
            car.seller = User.objects.get(username=request.user.username)
            car.save()

            images = image_form.cleaned_data['image']

            for pic in images:
                CarImage.objects.create(car=car, image=pic)

            return redirect('profile', username=request.user.username)

    else:
        listing_form = CreateListingForm()
        image_form = CreateImageListingForm()

    return render(request, 'cardealership/create_listing.html', {
        'listing_form': listing_form,
        'image_form': image_form
    })


class DeleteListingView(LoginRequiredMixin, DeleteView):
    model = Car

    def get_queryset(self):
        return Car.objects.filter(seller=self.request.user)  # проверка на то, является ли пользователь продавцом

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})


class CreateCommentView(CreateView, LoginRequiredMixin):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        listing = get_object_or_404(Car, pk=self.kwargs['pk'])
        author = self.request.user
        comment = form.save(commit=False)
        comment.listing = listing
        comment.author = author

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.listing.pk})


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.listing.pk})


class UpdateCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'pk': self.object.listing.pk})


@login_required(login_url='login')
def favorite_listing_view(request):
    favorites = Favorite.objects.filter(user=request.user)

    context = {
        'favorites': favorites
    }

    return render(request, 'cardealership/favorite_page.html', context)


@login_required(login_url='login')
@require_POST
def add_to_favorites(request, pk):
    car = get_object_or_404(Car, pk=pk)
    next_url = request.POST.get('next')

    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        favorite = Favorite.objects.filter(car=car, user=request.user)

        if favorite.exists():
            favorite.delete()
        else:
            Favorite.objects.create(user=request.user, car=car)

        return redirect(next_url)

    else:
        return redirect('car_detail', pk=pk)


@login_required(login_url='login')
def edit_listing_view(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if car.seller != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        listing_form = CreateListingForm(request.POST, instance=car)
        image_form = EditImageListingForm(request.POST, request.FILES)

        context = {
            'listing_form': listing_form,
            'images': car.images.all(),
            'image_form': image_form
        }
        if listing_form.is_valid() and image_form.is_valid():
            listing_form.save()
            delete_selected_images(car=car, image_ids=request.POST.getlist('delete_images'))
            images = image_form.cleaned_data['image']

            for pic in images:
                CarImage.objects.create(car=car, image=pic)

            return redirect('car_detail', pk=pk)
        else:
            return render(request, 'cardealership/edit_listing.html', context)

    elif request.method == 'GET':
        listing_form = CreateListingForm(instance=car)
        image_form = EditImageListingForm()

        context = {
            'listing_form': listing_form,
            'images': car.images.all(),
            'image_form': image_form
        }

        return render(request, 'cardealership/edit_listing.html', context)
