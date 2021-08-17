import json

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()

@register.filter
def en_nums_to_fa_nums(value):
    """
    This function convert english numbers to persian numbers
    """
    result = ""
    shape_nums = {
        "0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴", 
        "5": "۵", "6": "۶", "7": "۷", "8": "۸", "9": "۹"
    }

    for letter in str(value):
        if shape_nums.get(letter):
            result += shape_nums[letter]
        else:
            result += letter

    return result

@register.simple_tag
def first_letter_of_user(user):
    if user.first_name and user.last_name:
        return user.first_name[0] + " " + user.last_name[0]
    return user.username[0]

@register.filter
def js(value):
    return mark_safe(json.dumps(value))

@register.filter
def get_jalali_month(num):
    """
    This function return jalali month with parameter number month
    """
    months = {
        "1": "فروردین", "2": "اردیبهشت", "3": "خرداد", "4": "تیر", "5": "مرداد", "6": "شهریور",
        "7": "مهر", "8": "آبان", "9": "آذر", "10": "دی", "11": "بهمن", "12": "اسفند"
    }
    return months.get(num)

@register.simple_tag
def fws(name, margin_right_or_left=None, margin_number=None, custom_class=None, **attrs):
    """
    This function is shorthand for font awesome
    parmamter name for get font awesome icon name
    paramter margin_right_or_left for choice set margin from right or left
    in bootstrap --> 'l' is left and 'r' is right
    parameter margin_number for set margin number in bootstrap from number 1 to 5 
    parameter custom_class for add html classes to custom style or other things
    and split with , character
    parameter **attrs for set html attributes
    example in html: {% fws "home" "r" "2" title="main page" %}
    """

    if margin_right_or_left is None:
        margin_right_or_left = "l"

    if margin_number is None:
        margin_number = 0

    if custom_class is None:
        custom_class = ""

    attrs_ls = ""
    for key, value in attrs.items():
        attrs_ls += f"{key}='{value}' "

    result = f"""
    <span {attrs_ls.strip()} 
    class='m{margin_right_or_left}-{str(margin_number)} {" ".join(custom_class.split(","))}'>
    <i class='fa fa-{name}'></i></span>
    """

    return format_html(result)

@register.simple_tag
def user_profile_image(user, width=None, height=None, **kwargs):
    """
    This function return user profile image if user has profile image else
    return summary of username or name
    parameter user for get user
    parameter width and height for set user profile image width and height
    and parameter kwargs for other options
    example in html: {% user_profile_image user "3rem" "3rem" 
    profile_tag="a" has_title=True profile_classes="user-profile, text-center" %}
    """

    if width is None:
        width = "100%"

    if height is None:
        height = "100%"

    profile_tag = kwargs.pop("profile_tag", "div")
    no_profile_tag = kwargs.pop("no_profile_tag", "h5")
    no_profile_tag_size = kwargs.pop("no_profile_tag_size", "1.3rem")
    has_title = kwargs.pop("has_title", False)
    has_title_tag = kwargs.pop("has_title_tag", "b")
    profile_classes = kwargs.pop("profile_classes", "")
    title_classes = kwargs.pop("title_classes", "text-center")

    attrs_ls = ""
    # ? if user select tag a put auto href for user public profile
    if profile_tag == "a":
        attrs_ls += f"href='{reverse('account:about', args=(user.username,))}' "

    for key, value in kwargs.items():
        attrs_ls += f"{key}='{value}' "

    result = f"""<{profile_tag} {attrs_ls.strip()} 
    style='width: {width};height: {height};
    {f"background-image: url({user.profile_image.url});" 
    if user.profile_image else ""}' 
    class='profile_image {" ".join(profile_classes.split(","))}'>
    {f'''<{no_profile_tag} style='font-size: {no_profile_tag_size};'>
    {first_letter_of_user(user)}</{no_profile_tag}>'''
    if not user.profile_image else ""}
    {f"<{has_title_tag} class='{title_classes}'>{user.username}</{has_title_tag}>"
    if has_title else ""}
    </{profile_tag}>"""

    return format_html(result)

@register.simple_tag
def set_dashboard_url(url_name, slug=None, **kwargs):
    """
    This function returns the link to that user if the dashboard belongs to 
    that user; otherwise, it returns the link to the owner of that dashboard.
    """
    view_kwargs = kwargs.get("view_kwargs", {}).copy()
    view_kwargs.pop("page", {})
    view_kwargs.pop("slug", {})

    if slug is not None:
        view_kwargs.update({"slug": slug})

    return reverse(f"account:{url_name}", kwargs=view_kwargs)
