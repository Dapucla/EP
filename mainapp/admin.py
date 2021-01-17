from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .models import Smartphone
from .models import *
from .models import Category, Cart, Customer, NoteBook, Smartphone, Smartwatches, Headphones, TV, CartProduct, Order
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class CategoryAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    pass


class CartProductAdmin(ImportExportModelAdmin):
    pass


class CartAdmin(ImportExportModelAdmin):
    pass


class CustomerAdmin(ImportExportModelAdmin):
    pass


class OrderAdmin(ImportExportModelAdmin):
    pass


class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgray;'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


class NotebookAdmin(ImportExportModelAdmin):

    search_fields = ('title',)
    list_filter = ['price']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(ImportExportModelAdmin):

    search_fields = ('title',)
    list_filter = ['price']
    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartwatchesAdmin(ImportExportModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartwatches'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class HeadphonesAdmin(ImportExportModelAdmin):

    search_fields = ('title',)
    list_filter = ['price']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='headphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TVAdmin(ImportExportModelAdmin):

    search_fields = ('title',)
    list_filter = ['price']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='tv'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)
admin.site.register(NoteBook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Smartwatches, SmartwatchesAdmin)
admin.site.register(Headphones, HeadphonesAdmin)
admin.site.register(TV, TVAdmin)
admin.site.register(CartProduct, CartProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)