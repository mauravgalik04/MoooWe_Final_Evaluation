from django.urls import path
from . import views

urlpatterns = [
    path('' , views.movies_home_page_view , name = 'movies_home_page'),
    path('movies/' , views.movies_movies_view , name = 'movies_movies'),
    path('genres/' , views.movies_genre_view , name = 'movies_genre'),
    path('genres/<str:genre>' , views.all_movie_in_genre_view , name = 'all_movies_in_genre'),
    path('feature_movie/<int:id>/' , views.movies_feature_movie_view , name = 'movies_feature_movie'),
    path('register/' , views.movies_register_view , name = 'movies_register'),
    path('login' , views.movies_login_view , name = 'movies_login'),
    path('logout/' , views.logout_view , name = 'logout'),
    path('profile/' , views.movies_profile_view , name = 'movies_profile'),
    path('addmovie/' , views.movies_add_movie_view , name = 'movies_add_movie'),
    path('update_movie/<int:id>' , views.update_movie_view , name = 'update_movie'),
    path('delete_movie/<int:id>' , views.delete_movie_view , name = 'delete_movie'),
    path('add_to_watchlist/<int:id>' , views.add_to_watchlist_view , name = 'add_to_watchlist'),
    path('remove_from_watchlist/<int:id>' , views.remove_from_watchlist_view , name = 'remove_from_watchlist'),
    path('/add-comment/<int:movie_id>', views.add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>' , views.delete_comment ,name='delete_comment'),
    path('profile/edit/', views.movies_edit_profile_view, name='movies_edit_profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_pic'),
    path('profile/update-cover/', views.update_cover, name='update_cover'),
    path('profile/update-info/', views.update_user_info, name='update_user_info'),
    path('profile/update-quote/', views.update_quote, name='update_quote'),
    path('all_movies', views.all_movies , name = 'all_movies')
]