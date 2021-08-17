import json

from app.models import Post
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .validators import (check_number_uploaded_images, check_similar_images,
                         image_validation)

User = get_user_model()

_INP_DEFAULT_OPTIONS = {
    "autocomplete": "off",
    "autocapitalize": "off",
    "spellcheck": "false"
}

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(min_length=3, max_length=20, label="نام", required=False)
    first_name.widget = forms.TextInput(attrs=_INP_DEFAULT_OPTIONS)
    first_name.help_text = \
    "نام شما باید با حروف فارسی باشد و حداقل از ۳ حرف و حداکثر از ۲۰ حرف تشکیل شده باشد."
    last_name = forms.CharField(min_length=3, max_length=30, label="نام خانوادگی", required=False)
    last_name.widget = forms.TextInput(attrs=_INP_DEFAULT_OPTIONS)
    last_name.help_text = \
    "نام خانوادگی شما باید با حروف فارسی باشد و حداقل از ۳ حرف و حداکثر از ۳۰ حرف تشکیل شده باشد."

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "about_me", 
        "profile_image", "is_superuser", "is_staff")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["initial"] = self.initial["first_name"]
        self.fields["last_name"].widget.attrs["initial"] = self.initial["last_name"]

        self.fields["username"].widget.attrs.update({**_INP_DEFAULT_OPTIONS, 
        "initial": self.initial["username"]})
        self.fields["username"].help_text = \
        "شما فقط می توانید کوچکی و بزرگی حروف نام کاربری خود را تغییر دهید."

        self.fields["about_me"].widget.attrs["initial"] = self.initial["about_me"]
        self.fields["about_me"].help_text = \
        "درباره من باید با حروف فارسی باشد و می توانید از علامت های (، .) استفاده کنید."

        keys = ("initial", "checked")
        
        value = json.dumps(self.initial["is_superuser"])
        self.fields["is_superuser"].widget.attrs.update({}.fromkeys(keys, value))
        self.fields["is_superuser"].label = "دسترسی ابر کاربر"
        
        value = json.dumps(self.initial["is_staff"])
        self.fields["is_staff"].widget.attrs.update({}.fromkeys(keys, value))
        self.fields["is_staff"].label = "دسترسی به پنل ادمین"

    def clean_profile_image(self):
        data = self.cleaned_data["profile_image"]
        if data and hasattr(data, "image"):
            image_validation(data.image)
        return data

    def clean_username(self):
        username = self.cleaned_data["username"]
        old_username = self.user.username
        
        if username.lower() != old_username.lower():
            raise ValidationError(
                "شما فقط می توانید کوچکی و بزرگی حروف نام کاربری خود را تغییر دهید.",
                code="username_invalid"
            )
            
        return username

    def check_full_name(self):
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")

        if first_name or last_name:
            if not (first_name and last_name):
                raise ValidationError(
                    "لطفا دو فیلد نام و نام خانوادگی را با یکدیگر وارد کنید.",
                    code="full_name_invalid"
                )

    def clean_first_name(self):
        date = self.cleaned_data["first_name"]
        self.check_full_name()
        return date

    def clean_is_superuser(self):
        data = self.cleaned_data["is_superuser"]
        if ((self.request.user.is_superuser and self.request.user != self.user) \
        and (not self.user.is_superuser or self.request.user.is_admin)) \
        or self.user.is_superuser == data:
            return data
            
        raise ValidationError(
            "شما نمی توانید سطح دسترسی خود را تغییر دهید.",
            code="permission_error"
        )

    def clean_is_staff(self):
        data = self.cleaned_data["is_staff"]
        if ((self.request.user.is_superuser and self.request.user != self.user) \
        and (not self.user.is_superuser or self.request.user.is_admin)) or \
        self.user.is_staff == data:
            return data

        raise ValidationError(
            "شما نمی توانید سطح دسترسی خود را تغییر دهید.",
            code="permission_error"
        )
        
class PostForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.FileInput, label="انتخاب عکس")

    class Meta:
        model = Post
        fields = ("title", "img", "category")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.post_id = kwargs.pop("id", None)
        super().__init__(*args, **kwargs)

        try:
            self.fields["title"].widget.attrs["initial"] = self.initial["title"]
            self.fields["category"].widget.attrs["initial"] = self.initial["category"]
        except KeyError: 
            pass

    def clean_img(self):
        data = self.cleaned_data["img"]
        if data and hasattr(data, "image"):
            image_validation(data)
            check_similar_images(Post, data, self.post_id)       
            check_number_uploaded_images(Post, self.user)     
        return data
