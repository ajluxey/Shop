from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .forms import CustomUser, CustomUserCreationForm, CustomUserAuthForm, CustomUserSafetyChangeForm
from order.models import Order

# Create your views here.


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = CustomUserAuthForm
    success_url = reverse_lazy('catalog')
    success_message = 'Welcome to the CUM zone'

    def get_success_url(self):
        url = self.get_redirect_url()
        return self.success_url if not url else url


class LogoutUser(LogoutView):
    next_page = reverse_lazy('catalog')


class RegisterUser(CreateView):
    model = CustomUser
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)
        return form_valid


class UserProfile(View):
    def get(self, request, user_id):
        if request.user.id != user_id and not request.user.is_superuser and not request.user.groups.filter(name='Manager').exists():
            return HttpResponseForbidden()
        user = get_object_or_404(CustomUser, id=user_id)
        orders = Order.objects.filter(user=user.id).all()[:10]
        return render(request, 'users/profile.html', context={'user': user, 'orders': orders})


class ProfileChange(View):
    def get(self, request, user_id):
        if request.user.id != user_id:
            return HttpResponseForbidden()
        user = get_object_or_404(CustomUser, id=user_id)
        bound_form = CustomUserSafetyChangeForm(instance=user)
        return render(request, 'users/profile_update.html', context={'form': bound_form})

    def post(self, request, user_id):
        if request.user.id != user_id:
            return HttpResponseForbidden()
        user = get_object_or_404(CustomUser, id=user_id)
        bound_form = CustomUserSafetyChangeForm(request.POST, instance=user)
        if bound_form.is_valid():
            user = bound_form.save()
            return redirect(user)
        return render(request, 'shop/item_add.html', context={'form': bound_form})

