import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def en_nums_to_fa_nums(value):
    result = ""
    shape_nums = {
        "0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴", 
        "5": "۵", "6": "۶", "7": "۷", "8": "۸", "9": "۹"
    }

    for s in str(value):
        if shape_nums.get(s):
            result += shape_nums[s]
        else:
            result += s

    return result

@register.filter
def first_letter_to_upper(value):
    return value[0].upper()

@register.filter
def js(value):
    return mark_safe(json.dumps(value))

@register.filter
def get_jalali_month(num):
    months = {
        "1": "فروردین", "2": "اردیبهشت", "3": "خرداد", "4": "تیر", "5": "مرداد", "6": "شهریور",
        "7": "مهر", "8": "آبان", "9": "آذر", "10": "دی", "11": "بهمن", "12": "اسفند"
    }
    return months.get(num)