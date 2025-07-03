from django.contrib import admin
from .models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'click_count', 'owner', 'created_at')
    list_filter = ('owner',)
    search_fields = ('original_url', 'short_code')

    readonly_fields = ('owner',)

    def get_fields(self, request, obj=None):
        fields = ('original_url', 'short_code', 'click_count', 'owner')

        if obj is None:
            fields = ('original_url', 'short_code', 'click_count')

        return fields

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
