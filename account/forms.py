import json

from app.models import Post
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings

from .validators import image_validation

User = get_user_model()

image_types = list(map(lambda format: "image/" + format.lower(), 
settings.VALID_IMAGE_FORMATS))

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
        "profile_image", "is_superuser", "is_active")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        try:
            self.fields["profile_image"].widget.attrs["accept"] = ", ".join(image_types)

            self.fields["first_name"].widget.attrs["initial"] = self.initial["first_name"]
            self.fields["last_name"].widget.attrs["initial"] = self.initial["last_name"]

            self.fields["username"].widget.attrs.update({**_INP_DEFAULT_OPTIONS, 
            "initial": self.initial["username"]})
            self.fields["username"].help_text = \
            "شما فقط می توانید کوچکی و بزرگی حروف نام کاربری خود را تغییر دهید."

            self.fields["about_me"].widget.attrs["initial"] = self.initial["about_me"] or ""
            self.fields["about_me"].help_text = \
            "درباره من باید با حروف فارسی باشد و می توانید از علامت های (، .) استفاده کنید."
        except KeyError:
            pass

        # ? Set user levels
        self.set_user_level_front("is_superuser", "دسترسی ابر کاربر")
        self.set_user_level_front("is_active", "فعال بودن کاربر")

    def set_user_level_front(self, level_name, label_name):
        # ? This function show initial data if form invalid
        try:
            value = self.initial[level_name]
            self.fields[level_name].widget.attrs["initial"] = json.dumps(value)

            if value:
                self.fields[level_name].widget.attrs["checked"] = json.dumps(True)
            else:
                self.fields.pop("checked", {})

            self.fields[level_name].label = label_name
        except KeyError:
            pass

    def clean_profile_image(self):
        data = self.cleaned_data["profile_image"]
        if data and hasattr(data, "image"):
            image_validation(data.image)
        return data

    def clean_username(self):
        username = self.cleaned_data["username"]
        old_username = self.instance.username
        
        if username.lower() != old_username.lower():
            raise ValidationError(
                "شما فقط می توانید کوچکی و بزرگی حروف نام کاربری خود را تغییر دهید.",
                code="username_invalid"
            )
            
        return username

    def check_full_name(self):
        first_name = self.data["first_name"]
        last_name = self.data["last_name"]

        # ? first name and last name can be empty or both full
        if first_name or last_name:
            if not (first_name and last_name):
                raise ValidationError(
                    "لطفا دو فیلد نام و نام خانوادگی را با یکدیگر وارد کنید.",
                    code="full_name_invalid"
                )

    def clean_first_name(self):
        data = self.cleaned_data["first_name"]
        self.check_full_name()
        return data

    def clean_is_superuser(self):
        data = self.cleaned_data["is_superuser"]
        return self.change_user_level("is_superuser", data)

    def clean_is_active(self):
        data = self.cleaned_data["is_active"]
        return self.change_user_level("is_active", data)

    def change_user_level(self, level_name, data):
        # ? This function change permissions of user
        request_user_is_admin = self.request.user.is_admin
        user_level = getattr(self.instance, level_name)

        if (request_user_is_admin and self.instance != self.request.user 
        and not self.instance.is_admin) or user_level == data:
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
        super().__init__(*args, **kwargs)
        
        self.fields["img"].widget.attrs["accept"] = ", ".join(image_types)
        self.fields["title"].widget.attrs.update({**_INP_DEFAULT_OPTIONS})

        try:
            self.fields["title"].widget.attrs["initial"] = self.initial["title"]
            self.fields["category"].widget.attrs["initial"] = self.initial["category"]
        except KeyError: 
            pass

    def clean_img(self):
        data = self.cleaned_data["img"]
        if data and hasattr(data, "image"):
            image_validation(data.image)
        return data
