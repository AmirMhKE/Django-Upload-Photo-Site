from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from extensions.utils import compare_similarities_two_images
from PIL import Image

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
    """
    This function is for image validation and prevents the upload 
    of low quality images to some extent.
    """
    formats = settings.VALID_IMAGE_FORMATS
    min_width = settings.MIN_IMAGE_WIDTH
    min_height = settings.MIN_IMAGE_HEIGHT

    if data.format not in formats:
        raise ValidationError(
            "شما فقط می توانید فایلی با نوع {} آپلود کنید."
            .format(" یا ".join(formats)),
            code="format_invalid"
        )

    if data.width < min_width or data.height < min_height:
        raise ValidationError(
            "شما باید فایلی آپلود کنید که حداقل طول آن {} و عرض آن {} باشد."
            .format(min_width, min_height),
            code="size_invalid"
        )

def check_similar_images(model, data, instance_pk=None):
    """
    model Post getted from out file because
    code 'from app.model import Post' has error occurred. 
    """
    query = model.objects.values_list("img")
    if instance_pk is not None:
        query = query.exclude(pk=instance_pk)

    check_images = (
        compare_similarities_two_images(Image.open(data), 
        Image.open(settings.MEDIA_ROOT / img_path[0]))
        for img_path in query.iterator()
    )

    if any([*check_images]):
        raise ValidationError(
            "عکسی مشابه عکس شما در سایت وجود دارد.",
            code="similar_image_error"
        )

def check_number_uploaded_images(model, user):
    """
    This function limits the user to uploading too many images 
    and the user can not upload a large number of images per day.
    """
    if not user.is_superuser:
        max_count = settings.MAX_IMAGE_UPLOAD_COUNT
        now_time = timezone.now().date()
        query = model.objects.filter(publisher=user, created__date=now_time)

        if query.count() >= max_count:
            raise ValidationError(
                "شما نمی توانید در هر روز بیشتر از {} عکس آپلود کنید."
                .format(max_count),
                code="max_image_uploaded"
            )
