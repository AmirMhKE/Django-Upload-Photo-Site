import json
import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "profile_image"]

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

    def is_valid(self):
        event = {"type": "user_profile_updated", "content": None}
        self.request.session["event"] = json.dumps(event)
        return super().is_valid()
