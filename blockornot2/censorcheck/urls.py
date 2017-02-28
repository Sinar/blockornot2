from django.conf.urls import url

from censorcheck import views


urlpatterns = [
            url(r'^detail/', views.DetailView.as_view(), name='detail'),
            url(r'', views.SearchView.as_view(), name='search'),
        ]

