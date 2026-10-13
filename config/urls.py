from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("homepage.urls")),
    path("", include("accounts.urls")),
    path("", include("tracking.urls")),
]

handler404 = "homepage.views.page_not_found"
