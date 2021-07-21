import json
import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "profile_image", "is_superuser", "is_staff"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        MIN_LENGTH, MAX_LENGTH = 3, 20

        if first_name.strip() != "":
            if not (MIN_LENGTH <= len(first_name) <= MAX_LENGTH):
                raise ValidationError(
                    f"نام شما حداقل باید از {MIN_LENGTH} حروف و حداکثر از {MAX_LENGTH} حروف تشکیل شده باشد.",
                    code="first_name_invalid"
                ) 

            # ? if first name not persian alphabet
            pattern = r"^[آ-ی ء چ]+$"
            if re.match(pattern, first_name) is None:
                raise ValidationError(
                    "نام خود را به صورت حروف فارسی وارد کنید.",
                    code="first_name_invalid"
                )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        MIN_LENGTH, MAX_LENGTH = 3, 30

        if last_name.strip() != "":
            if not (MIN_LENGTH <= len(last_name) <= MAX_LENGTH):
                raise ValidationError(
                    f"نام خانوادگی شما حداقل باید از {MIN_LENGTH} حروف و حداکثر از {MAX_LENGTH} حروف تشکیل شده باشد.",
                    code="last_name_invalid"
                ) 

            # ? if last name not persian alphabet
            pattern = r"^[آ-ی ء چ]+$"
            if re.match(pattern, last_name) is None:
                raise ValidationError(
                    "نام خانوادگی خود را به صورت حروف فارسی وارد کنید.",
                    code="last_name_invalid"
                )

        return last_name

    def clean_username(self):
        username = self.cleaned_data["username"]
        old_username = self.user.username
        
        if username.lower() != old_username.lower():
            raise ValidationError(
                "شما فقط می توانید کوچکی و بزرگی حروف نام کاربری خود را تغییر دهید.",
                code="username_invalid"
            )
            
        return username

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