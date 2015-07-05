from __future__ import absolute_import
from braces import views
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from .forms import LoginForm
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

class HomePageView(generic.TemplateView):
    template_name = 'home.html'
	
	
class SignUpView(views.AnonymousRequiredMixin,views.FormValidMessageMixin,CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    model = User
    form_valid_message="you've registered successfully.Now go on login to access your account."
    template_name = 'accounts/signup.html'

	
class LoginView(views.AnonymousRequiredMixin,views.FormValidMessageMixin,FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    form_valid_message="You're now logged in.Go on have fun."
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)
			
class LogOutView(views.LoginRequiredMixin,views.MessageMixin,RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("You've been logged out. Come back soon!")
        return super(LogOutView, self).get(request, *args, **kwargs)