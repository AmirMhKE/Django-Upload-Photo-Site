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

class CategoryAdmin(admin.ModelAdmin):
    list_filter = ["status"]
    list_display = ["title", "slug", "status", "position"]
    actions = [make_status_true, make_status_false]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
admin.site.register(Ip)
