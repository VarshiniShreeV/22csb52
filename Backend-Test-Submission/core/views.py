# shortener/views.py
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseGone, HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURL
from .serializers import ShortURLCreateSerializer


@api_view(['POST'])
def create_shorturl(request):
    serializer = ShortURLCreateSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        short_url = request.build_absolute_uri(f"/{obj.shortcode}/")
        return Response({
            "short_url": short_url,
            "shortcode": obj.shortcode,
            "expires_at": obj.expires_at,
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_shortinfo(request, shortcode):
    obj = get_object_or_404(ShortURL, shortcode=shortcode)
    return Response({
        "original_url": obj.original_url,
        "short_url": request.build_absolute_uri(f"/{obj.shortcode}/"),
        "created_at": obj.created_at,
        "expires_at": obj.expires_at,
        "is_expired": obj.is_expired
    })


def redirect_short(request, shortcode):
    obj = get_object_or_404(ShortURL, shortcode=shortcode)
    if obj.is_expired:
        return HttpResponse("This shortlink has expired.", status=410)
    return HttpResponseRedirect(obj.original_url)
