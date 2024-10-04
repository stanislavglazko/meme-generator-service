from django.contrib import admin
from .models import Meme, MemeTemplate, Rating


@admin.register(Meme)
class MemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'top_text', 'bottom_text', 'created_by', 'created_at')
    search_fields = ('top_text', 'bottom_text', 'created_by__username')
    list_filter = ('created_at', 'template')
    readonly_fields = ('created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(MemeTemplate)
class MemeTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_url', 'default_top_text', 'default_bottom_text')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'meme', 'user', 'score', 'created_at')
    readonly_fields = ('created_at', )
