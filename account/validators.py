from django.conf import settings
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

def image_validation(image):
    """
    This function is for image validation and prevents the upload 
    of low quality images to some extent.
    """
    formats = settings.VALID_IMAGE_FORMATS
    min_width = settings.MIN_IMAGE_WIDTH
    min_height = settings.MIN_IMAGE_HEIGHT

    if image.format not in formats:
        raise ValidationError(
            "شما فقط می توانید فایلی با نوع {} آپلود کنید."
            .format(" یا ".join(formats)),
            code="format_invalid"
        )

    if image.width < min_width or image.height < min_height:
        raise ValidationError(
            "شما باید فایلی آپلود کنید که حداقل طول آن {} و عرض آن {} باشد."
            .format(min_width, min_height),
            code="size_invalid"
        )
