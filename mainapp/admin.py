from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
from .models import *

from PIL import Image

class NotebookAdminForm(ModelForm):

   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '<span style="color:red" font-size:14px>Загружайте изображения с минимальным разрешением {}x{}</span>'.format(
            *self.Product.MIN_RESOLUTION
            )
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)

        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3МВ')
        if img.height < 400 or img.width < 400:
            raise ValidationError('Разрешение зображения меньше минимального')
        if img.height > 900 or img.width > 900:
            raise ValidationError('Разрешение изображения больше максимального')
        return image

class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm
    def formfield_for_foreignkey(self,db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks')) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class SmartphoneAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self,db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones')) 
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)





