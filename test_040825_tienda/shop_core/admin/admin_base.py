from django.contrib import admin
from .estado_filter import EstadoFilter, eliminar_soft, restaurar_soft


admin.site.disable_action('delete_selected')

class BaseAdmin(admin.ModelAdmin):
    list_filter = (EstadoFilter,)
    readonly_fields = ('deleted_at', 'created_at', 'updated_at')
    actions = [eliminar_soft, restaurar_soft]

    def delete_model(self, request, obj):
        obj.soft_delete()  # Usa soft delete
    
    def get_queryset(self, request):
        # Usar all_objects para mostrar todos los registros (incluyendo eliminados)
        return self.model.all_objects.get_queryset()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.soft_delete()