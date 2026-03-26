
from import_export.resources import ModelResource
from .models import Product, Category

class ProductResource(ModelResource):

    class Meta:
        model = Product


class CategoryResource(ModelResource):

    class Meta:
        model = Category