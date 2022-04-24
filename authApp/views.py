from django.shortcuts import render
from django.views import generic
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.mixins import LoginRequiredMixin
from authApp.forms import RegisterForm, CustomUserChangeForm
from authApp.models import CustomUser
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.urls import reverse


class CustomUserView(generic.DetailView):
    model = CustomUser
    form = CustomUserChangeForm()
    template_name = "authApp/profile.html"

def registration_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user.set_password(password)
            user.email = email
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your events app account.'
            message = render_to_string('authApp/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[email])
            email.content_subtype = 'html' 
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegisterForm()

    return render(request, 'authApp/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authApp/email_activated.html')
    else:
        return HttpResponse('Activation link is invalid!')

class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'authApp/edit_user.html'
    login_url = '/account/login/'

    def get_success_url(self):
        return reverse('events:event_list')