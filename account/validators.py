from django.core.validators import RegexValidator


persian_name_validator = RegexValidator(
    regex=r"^[آ-ی ء چ]+$",
    message="لطفا عبارت خود را به صورت حروف فارسی وارد کنید.",
    code="persian_name_invalid"
)

persian_text_validator = RegexValidator(
    regex=r"^[آ-ی ء چ ، .]+$",
    message="لطفا عبارت خود را به صورت حروف فارسی وارد کنید و می توانید از عبارت های (، .) استفاده کنید.",
    code="persian_text_invalid"
)