from django.urls import include, path

urlpatterns = [
    path('', include("history.urls")),
    path('wizard/', include("setup.urls")),
    path('rest/', include("api.urls")),
]
