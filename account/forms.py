import json

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from PIL import Image

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(min_length=3, max_length=20, label="نام", required=False)
    last_name = forms.CharField(min_length=3, max_length=30, label="نام خانوادگی", required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "about_me", "profile_image", "is_superuser", "is_staff")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_profile_image(self):
        data = self.cleaned_data["profile_image"]

        if data:
            image = Image.open(data.file)
            height, width = image.size

            if image.format != "JPEG":
                raise ValidationError(
                    "شما فقط می توانید فایلی با نوع JPEG آپلود کنید!",
                    code="extension_invalid"
                )

            if width < 300 or height < 300:
                raise ValidationError(
                    "شما باید فایلی آپلود کنید که حداقل طول و عرض آن ۳۰۰ باشد.",
                    code="size_invalid"
                )
            
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
        and (not self.user.is_superuser or self.request.user.is_admin)) or self.user.is_superuser == data:
            return data
            
        raise ValidationError(
            "شما نمی توانید سطح دسترسی خود را تغییر دهید.",
            code="permission_error"
        )

    def clean_is_staff(self):
        data = self.cleaned_data["is_staff"]
        if ((self.request.user.is_superuser and self.request.user != self.user) \
        and (not self.user.is_superuser or self.request.user.is_admin)) or self.user.is_staff == data:
            return data

        raise ValidationError(
            "شما نمی توانید سطح دسترسی خود را تغییر دهید.",
            code="permission_error"
        )

    def is_valid(self):
        is_data_valid = super().is_valid()

        if is_data_valid:
            content = ""
            if self.request.user == self.user:
                content = "حساب کاربری شما با موفقیت ویرایش شد."
            else:
                content = f"حساب کاربری {self.user.get_name_or_username} با موفقیت آپدیت شد."

            event = {"type": "user_profile_updated", "content": content}
            self.request.session["event"] = json.dumps(event)

        return is_data_valid