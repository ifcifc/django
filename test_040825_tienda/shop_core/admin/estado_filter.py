from django.utils import timezone
from django.contrib import admin

def eliminar_soft(modeladmin, request, queryset):
    queryset.update(deleted_at = timezone.now())
eliminar_soft.short_description = "Eliminar artículos seleccionados"

def restaurar_soft(modeladmin, request, queryset):
    queryset.update(deleted_at = None)
restaurar_soft.short_description = "Restaurar artículos seleccionados"


class EstadoFilter(admin.SimpleListFilter):
    title = 'Estado del Producto'
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
        return [
            ('todos', 'Todos'),
            ('activos', 'Activos'),
            ('borrados', 'Borrados'),
        ]

    def value(self):
        value = super().value()
        if value is None:
            return 'activos'  # Valor por defecto
        return value

    def choices(self, changelist):
        #Para evitar que me muestre el All en el filtro
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == str(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == 'todos':
            return queryset.all()
        if self.value() == 'activos':
            return queryset.filter(deleted_at__isnull = True)
        if self.value() == 'borrados':
            return queryset.filter(deleted_at__isnull = False)

