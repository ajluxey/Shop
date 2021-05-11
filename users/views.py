from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from .forms import CustomUser, CustomUserCreationForm

# Create your views here.


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('catalog')
    success_message = 'Welcome to the CUM zone'

    def get_success_url(self):
        url = self.get_redirect_url()
        return self.success_url if not url else url


class LogoutUser(LogoutView):
    next_page = reverse_lazy('catalog')


# TODO: если уже автоизован, то запретить заходить на вход
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
