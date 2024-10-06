"""meme_generator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from meme_generator.views import (
    MemeViewSet, RandomMemeViewSet, RatingViewSet, TemplatesViewSet, TopMemesViewSet, SurpriseMeViewSet
)

router = DefaultRouter()
router.register(r"templates", TemplatesViewSet, basename="template")
router.register(r"memes/random", RandomMemeViewSet, basename="random-meme")
router.register(r"memes/surprise-me", SurpriseMeViewSet, basename="surprise-me")
router.register(r"memes/top", TopMemesViewSet, basename="top-memes")
router.register(r"memes/(?P<meme_pk>\d+)/rate", RatingViewSet, basename="rating")
router.register(r"memes", MemeViewSet, basename="meme")


SchemaView = get_schema_view(
    openapi.Info(title="Meme Generator api", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger/", SchemaView.with_ui("swagger", cache_timeout=0), name="swagger_ui"),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
