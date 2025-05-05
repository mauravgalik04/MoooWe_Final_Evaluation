from django.urls import path
from . import views
urlpatterns = [
    path('' , views.booking_home_view , name = "booking_home"),
    path('theatre_dashboard/' , views.theater_dashboard_view , name = "theatre_dashboard"),
    path('theatre_register/' , views.register_theatre_view , name = 'theatre_registration'),
    path('update_theatre/<int:id>' , views.update_theatre_view , name = 'update_theatre'),
    path('delete_theatre/<int:id>' , views.delete_theatre_view , name = 'delete_theatre'),
    path('add_show/<int:id>' , views.add_show_view , name='add_show'),
    path('manage_shows/<int:id>', views.manage_show_view , name='manage_shows'),
    path('update_show/<int:id>' , views.update_show_view , name='update_show'),
    path('delete_show/<int:id>' , views.delete_show_view , name = 'delete_show'),
    path('book_show/<int:theatre_id>' , views.book_show , name='book_show')
]