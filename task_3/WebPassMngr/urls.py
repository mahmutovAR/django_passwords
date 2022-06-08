from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from PassDB import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    re_path(r'^cards/$', views.CardListView.as_view(), name='cards'),
    re_path(r'^cards/(?P<pk>\d+)$', views.CardDetailView.as_view(), name='cards_detail'),
    re_path(r'^logins/$', views.LoginListView.as_view(), name='logins'),
    re_path(r'^logins/(?P<pk>\d+)$', views.LoginDetailView.as_view(), name='logins_detail'),
    re_path(r'^notes/$', views.NoteListView.as_view(), name='notes'),
    re_path(r'^notes/(?P<pk>\d+)$', views.NoteDetailView.as_view(), name='notes_detail'),
    path('all_pass_db/', views.PassDbListView.as_view(), name='pass_db'),
    path('add_data/', views.add_data, name='add_pass'),
    path('all_pass_db/edit_data/<int:id>/', views.edit_data, name='edit_data'),
    path('all_pass_db/delete_data/<int:id>/', views.delete_data, name='delete_data'),
    path('all_pass_db/load_pass/<int:id>/', views.load_pass, name='load_pass'),
    path('all_pass_db/clear_pass/', views.clear_pass, name='clear_pass'),
    path('search_pass/', views.search_pass, name='search_pass'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
