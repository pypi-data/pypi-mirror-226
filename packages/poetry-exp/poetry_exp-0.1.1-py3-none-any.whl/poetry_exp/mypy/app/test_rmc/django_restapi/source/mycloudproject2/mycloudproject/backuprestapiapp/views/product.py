
from backuprestapiapp.models.product import Product
from backuprestapiapp.serializers.product import ProductSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

# .local/share/umake/ide/pycharm/bin/pycharm.sh
# Create your views here.


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JSONResponse(serializer.data)
