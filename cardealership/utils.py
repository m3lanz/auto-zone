
from django.shortcuts import get_object_or_404
from .models import CarImage

def delete_selected_images(car, image_ids):
    queryset = CarImage.objects.filter(pk__in=image_ids, car=car)
    queryset.delete()