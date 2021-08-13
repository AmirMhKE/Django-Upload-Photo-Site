from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

persian_name_validator = RegexValidator(
    regex=r"^[آ-ی ء چ]+$",
    message="لطفا عبارت خود را به صورت حروف فارسی وارد کنید.",
    code="persian_name_invalid"
)

persian_text_validator = RegexValidator(
    regex=r"^[آ-ی ء چ ، .]+$",
    message=" ".join("لطفا عبارت خود را به صورت حروف فارسی وارد کنید\
     و می توانید از عبارت های (، .) استفاده کنید.".split()),
    code="persian_text_invalid"
)

def image_validation(data):
    if data.format != "JPEG":
        raise ValidationError(
            "شما فقط می توانید فایلی با نوع JPEG آپلود کنید!",
            code="format_invalid"
        )

    if data.width < 300 or data.height < 300:
        raise ValidationError(
            "شما باید فایلی آپلود کنید که حداقل طول و عرض آن ۳۰۰ باشد.",
            code="size_invalid"
        )
