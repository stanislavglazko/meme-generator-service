from django.utils.html import format_html
from django.contrib import admin
from .models import Meme, MemeTemplate, Rating


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ("id", "template", "top_text", "bottom_text", "created_by", "created_at")
    search_fields = ("top_text", "bottom_text", "created_by__username")
    list_filter = ("created_at", "template")
    readonly_fields = ("created_by", "created_at", "image_url", "image_url_display")

    def image_url_display(self, obj):
        if obj.image_url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.image_url, "Open Image")
        return "-"

    image_url_display.short_description = "Image URL"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MemeTemplate)
class MemeTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image_url", "image", "default_top_text", "default_bottom_text")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "meme", "user", "score", "created_at")
    readonly_fields = ("created_at", )
