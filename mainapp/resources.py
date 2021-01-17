from import_export import resources
from .models import Smartphone


class SmartphoneResource(resources.ModelResource):
    class Meta:
        model = Smartphone