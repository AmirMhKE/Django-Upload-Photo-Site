from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
import re

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        MIN_LENGTH = 5
        MAX_LENGTH = 32

        username = self.cleaned_data["username"]
        pattern = r"^[a-zA-Z]+([._]?[a-zA-Z0-9]+)*$"
        regex = re.match(pattern=pattern, string=username)

        if not (regex and MIN_LENGTH <= len(username) <= MAX_LENGTH):
            raise forms.ValidationError(
                "نام کاربری باید حداقل ۵ حرف و حداکثر ۳۲ حرف باشد و با حروف کوچک یا بزرگ انگلیسی شروع شود و بعد از آن می توانید از اعداد یا نقطه یا زیر خط استفاده کنید و همچنین نام کاربری باید با حروف انگلیسی کوچک یا بزرگ و یا اعداد تمام شود.",
                code="username_error"
            )

        return username