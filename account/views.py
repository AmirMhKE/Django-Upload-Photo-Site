import json

from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import \
    PasswordResetConfirmView as PasswordResetConfirmView_
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import request
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View

from .forms import SignUpForm
from .mixins import CheckRecaptchaMixin
from .tokens import account_activation_token

User = get_user_model()

class LoginView(CheckRecaptchaMixin, View):
    user_not_exist = False
    user_wrong_password = False

    def post(self, request, *args, **kwargs):
        global applicant_path
        applicant_path = request.POST.get("applicant_path")
        authenticate_user = self.authenticate(request)

        # Check user is active
        if authenticate_user:
            if not authenticate_user.is_active:
                dict_obj = {"type": "user_not_active", "content": None}
                request.session["event"] = json.dumps(dict_obj)
                return redirect(applicant_path)
        # ********************
        
        if not self.user_not_exist and not self.user_wrong_password:
            login(request, authenticate_user)
            dict_obj = {"type": "user_login_success", "content": None}
            request.session["event"] = json.dumps(dict_obj)
        else:
            if self.user_not_exist:
                dict_obj = {"type": "user_not_exist", "content": None}
                request.session["event"] = json.dumps(dict_obj)
            elif self.user_wrong_password:
                dict_obj = {"type": "user_wrong_password", "content": None}
                request.session["event"] = json.dumps(dict_obj)

        return redirect(applicant_path)

    def authenticate(self, request):
        req = request.POST
        username_or_email = req.get("username_or_email")
        password = req.get("password")
        
        # Get user with username or email
        try:
            get_user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                get_user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                get_user = None

        if get_user:
            if get_user.check_password(password):
                return get_user
            self.user_wrong_password = True
        else:
            self.user_not_exist = True

class SignUpView(CheckRecaptchaMixin, View):
    def post(self, request, *args, **kwrags):
        global applicant_path
        applicant_path = request.POST.get("applicant_path")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'اکانت خود را در سایت عکس کده فعال کنید.'
            message = render_to_string("account/acc_active_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user)
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            dict_obj = {"type": "email_sended", "content": None}
            request.session["event"] = json.dumps(dict_obj)
            return redirect(applicant_path)
        else:
            content = [item for item in form.errors.values()]
            dict_obj = {"type": "signup_error", "content": content}
            request.session["event"] = json.dumps(dict_obj)

        return redirect(applicant_path)

class ActivateAccount(View):
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            dict_obj = {"type": "activation_success", "content": None}
            request.session["event"] = json.dumps(dict_obj)
        else:
            dict_obj = {"type": "activation_invalid", "content": None}
            request.session["event"] = json.dumps(dict_obj)

        return redirect(applicant_path)

class PasswordResetView(CheckRecaptchaMixin, View):
    def post(self, request, *args, **kwargs):
        global applicant_path
        applicant_path = request.POST.get("applicant_path")
        email = request.POST.get("email")
        authenticate_user = User.objects.filter(email=email)

        if not authenticate_user:
            dict_obj = {"type": "email_not_found", "content": None}
            request.session["event"] = json.dumps(dict_obj)
        else:
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                opts = {
                    'use_https': self.request.is_secure(),
                    'token_generator': PasswordResetTokenGenerator(),
                    'from_email': None,
                    'email_template_name': "account/password_reset_email.html",
                    'subject_template_name': "account/password_reset_subject.txt",
                    'request': request,
                    'html_email_template_name': None,
                    'extra_email_context': None,
                }
                form.save(**opts)
                dict_obj = {"type": "password_reset_email_sended", "content": None}
                request.session["event"] = json.dumps(dict_obj)

        return redirect(applicant_path)

class PasswordResetConfirmView(PasswordResetConfirmView_):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("post_list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ? if token is invalid
        if context["form"] is None:
            dict_obj = {"type": "password_reset_invalid_token", "content": None}
            self.request.session["event"] = json.dumps(dict_obj)

        return context

    def form_valid(self, form):
        dict_obj = {"type": "password_reset_done", "content": None}
        self.request.session["event"] = json.dumps(dict_obj)
        return super().form_valid(form)

    def form_invalid(self, form):
        content = [item for item in form.errors.values()]
        dict_obj = {"type": "password_reset_error", "content": content}
        self.request.session["event"] = json.dumps(dict_obj)
        return super().form_invalid(form)