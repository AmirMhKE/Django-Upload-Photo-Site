from django.contrib import admin

from .models import Category, Ip, Post

admin.site.site_header = "مدیریت سایت عکس کده"

def make_status_true(modeladmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = "نمایش داده شد."
    else:
        message_bit = "نمایش داده شدند."
    modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))
make_status_true.short_description = "نمایش دسته بندی های انتخاب شده"

def make_status_false(modeladmin, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message_bit = "غیر قابل نمایش شد."
    else:
        message_bit = "غیر قابل نمایش شدند."
    modeladmin.message_user(request, "{} دسته بندی {}".format(rows_updated, message_bit))
make_status_false.short_description = "غیر قابل نمایش کردن دسته بندی های انتخاب شده"

def make_back(modeladmin, request, queryset):
    rows_updated = queryset.update(status="b")
    if rows_updated == 1:
        message_bit = "برگشت داده شد."
    else:
        message_bit = "برگشت داده شدند."
    modeladmin.message_user(request, "{} پست {}".format(rows_updated, message_bit))
make_back.short_description = "برگشت دادن پست های انتخاب شده"

def make_publish(modeladmin, request, queryset):
    rows_updated = queryset.update(status="p")
    if rows_updated == 1:
        message_bit = "منتشر داده شد."
    else:
        message_bit = "منتشر داده شدند."
    modeladmin.message_user(request, "{} پست {}".format(rows_updated, message_bit))
make_publish.short_description = "منتشر دادن پست های انتخاب شده"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    list_display = ["title", "slug", "status", "position"]
    actions = [make_status_true, make_status_false]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "thumbnail_img", "publisher", "category"]
    actions = [make_back, make_publish]

admin.site.register(Ip)
