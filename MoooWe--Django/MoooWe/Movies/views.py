import os
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from Movies.models import Movie, AppUser, Comment
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
import requests
api = 'http://127.0.0.1:5000/movies'
# Create your views here.


# Home Page view function :
def movies_home_page_view(request):
    movies = Movie.objects.all()
    data = {"movies": movies}
    return render(request, "movies_home_page.html", context=data)

#checking api view
def all_movies(request):
    response = requests.get(api)
    if response.status_code != 200:
        all_movies = []
    else:
        payload = response.json()
        all_movies = payload.get("movies", [])

    query = request.GET.get("searchbar", "").strip().lower()
    if query:
        filtered = [
            m for m in all_movies
            if query in m["name"].lower()
        ]
    else:
        filtered = all_movies

    return render(request, "all_movies.html", {"movies": filtered})


def movies_movies_view(request):
    response = requests.get(api)
    if response.status_code != 200:
        all_movies = []
    else:
        payload = response.json()
        all_movies = payload.get("movies", [])

    query = request.GET.get("searchbar", "").strip().lower()
    if query:
        filtered = [
            m for m in all_movies
            if query in m["name"].lower()
        ]
    else:
        filtered = all_movies

    return render(request, "all_movies.html", {"movies": filtered})


def movies_genre_view(request):
    genres = [
        "Action",
        "Adventure",
        "Biography",
        "Romance",
        "Comedy",
        "Drama",
        "Thriller",
        "Sci-Fi",
        "Crime",
        "Horror",
        "Other",
    ]
    response = requests.get(api)
    if response.status_code != 200:
        all_movies = []
    else:
        payload = response.json()
        all_movies = payload.get("movies", [])
    data = {"genres": genres, "movies": all_movies}
    return render(request, "movies_genre.html", context=data)


def all_movie_in_genre_view(request, genre):
    movies = Movie.objects.filter(genre=genre)
    data = {"movies": movies, "genre": genre}
    return render(request, "movie_all_movie_in_genre.html", context=data)


@login_required
def movies_feature_movie_view(request, id):

    resp = requests.get(f"{api}/{id}")
    if resp.status_code != 200:
        messages.error(request, "Movie not found!")
        return redirect("movies_movies")  

    movie = resp.json() 
    comments = Comment.objects.filter(movie_id=id)
    return render(request, "movies_feature_movie.html", {
        "movie": movie,
        "comments": comments,
    })



# for registering a user :
def movies_register_view(request):
    User = get_user_model()
    if request.method == "POST":
        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        phone = request.POST.get("phone").strip()
        address = request.POST.get("address").strip()
        gender = request.POST.get("gender").strip()
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password != cpassword:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            try:
                validate_password(password)
                User.objects.create_user(
                    email=email,
                    name=name,
                    phone=phone,
                    address=address,
                    gender=gender,
                    password=password,
                )
                messages.success(request, "Registration successful! You can now login.")
                print("Redirecting to login...")
                return redirect("movies_login")
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
            except Exception as e:  # Catch any other error.
                messages.error(
                    request, f"An unexpected error occurred: {e}"
                )  # provide the error to the user.
                print(f"An unexpected error occurred: {e}")
    return render(request, "movies_register.html")


# for the user to log in:
def movies_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        selected_role = request.POST.get("role")

        user = authenticate(request, email=email, password=password)

        if user:
            if (selected_role == "admin" and user.is_superuser) or (
                selected_role == "user" and not user.is_superuser
            ):
                login(request, user)
                messages.success(request , "Logged in successfully.")
                return redirect("movies_home_page")
            else:
                messages.error(
                    request, "Role mismatch. Please select the correct role."
                )
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "movies_login.html")


# for logging out :
@login_required
def logout_view(request):
    logout(request)
    messages.success(request , "Logged out, seeyaaa!!")
    return redirect("movies_home_page")


@login_required
def add_to_watchlist_view(request, id):
    response = requests.get(f"{api}/{id}")
    if response.status_code != 200:
        messages.error(request, "Movie not found.")
        return redirect("movies_movies")
    movie_data = response.json()
    patch_response = requests.patch(f"{api}/{id}", json={"watchlist": 1})  
    if patch_response.status_code in [200, 204]: 
        messages.success(request, f"{movie_data['name']} added to watchlist.")
    else:
        messages.error(request, f"Failed to update watchlist for {movie_data['name']}.")
    
    return redirect("movies_movies")

@login_required
def remove_from_watchlist_view(request, id):
    response = requests.get(f"{api}/{id}")
    if response.status_code != 200:
        messages.error(request, "Movie not found.")
        return redirect("movies_movies")
    movie_data = response.json()
    patch_response = requests.patch(f"{api}/{id}", json={"watchlist": 0})  
    if patch_response.status_code in [200, 204]: 
        messages.success(request, f"{movie_data['name']} removed from to watchlist.")
    else:
        messages.error(request, f"Failed to update watchlist for {movie_data['name']}.")
    
    return redirect("movies_movies")




def movies_add_movie_view(request):
    if request.method == "POST":
        name = request.POST.get("movie-name")
        release_year = request.POST.get("release-year")
        genre = request.POST.get("genre")
        story = request.POST.get("movie-description")
        cast = request.POST.get("movie-cast")
        imdb_rating = request.POST.get("imdb-rating")
        poster = request.FILES.get("poster")
        landscape = request.FILES.get("landscape")

        upload_path = os.path.join(settings.BASE_DIR, "Movies/static", "posters")
        os.makedirs(upload_path, exist_ok=True)

        fs = FileSystemStorage(location=upload_path)
        saved_poster = fs.save(poster.name, poster)
        saved_landscape = fs.save(landscape.name, landscape)

        try: 
            response = requests.post(api, json={
                "name" : name,
                "release_year":release_year,
                "genre" :genre,
                "imdb_rating":imdb_rating,
                "description" :story,
                "cast":cast,
                "poster" : saved_poster,
                "landscape":saved_landscape
            })
            if response.status_code == 201:
                messages.success(request, "Movie added successfully.")
            else:
                messages.error(request, f"Failed to add movie. Error: {response.text}")
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Request failed: {str(e)}")
    return render(request, "movies_add_movie.html")



def update_movie_view(request, id):
    response = requests.get(api+f"/{id}")
    movie_data = response.json()
    if request.method == "POST":
        patch_response = requests.patch(api+f"/{id}" , json={
            "movie":request.POST.get("movie-name"),
            "release_year": request.POST.get("release-year"),
            "genre" : request.POST.get("genre"),
            "description" : request.POST.get("movie-description"),
            "cast"  : request.POST.get("movie-cast"),
            "imdb_rating" : request.POST.get("imdb-rating"),
        })
        if patch_response.status_code in [200,204]:
            messages.success(request, "Movie updated successfully.")
            return redirect("movies_movies")
    data = {"movie": movie_data}
    return render(request, "movies_update_movie.html", context=data)


def delete_movie_view(request, id):
    requests.delete(api+f"/{id}")
    messages.success(request, "Movie deleted successfully.")
    return redirect("movies_movies")


@login_required
def add_comment(request, movie_id):
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        movie = get_object_or_404(Movie, pk=movie_id)

        if comment_text:
            Comment.objects.create(
                user=request.user,
                comment=comment_text,
                movie_id=movie,
            )
            messages.success(request, "Comment added successfully.")
        return redirect("movies_feature_movie", id=movie.id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        if comment.user == request.user:
            movie_id = comment.movie_id.id
            comment.delete()
            messages.success(request, "Comment deleted successfully.")
            return redirect("movies_feature_movie", id=movie_id)
        else:
            messages.error(request , "Can't delete this comment.")
            return redirect("movies_feature_movie", id=comment.movie_id.id)


@login_required
def movies_edit_profile_view(request):
    if request.method == "POST":
        try:
            user = request.user

            # Update user information
            user.name = request.POST.get("full_name", user.name)
            user.phone = request.POST.get("phone", user.phone)
            user.gender = request.POST.get("gender", user.gender)

            # Handle profile picture upload
            if "profile_picture" in request.FILES:
                user.image = request.FILES.get('profile_picture')

            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("movies_profile")
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
            return redirect("movies_edit_profile")
    return render(request, "movies_edit_profile.html")


@login_required
def update_profile_picture(request):
    if request.method == "POST" and request.FILES.get("profile_picture"):
        try:
            user = request.user
            user.image = request.FILES.get('profile_picture')
            user.save()
            messages.success(request, "Profile picture updated successfully!")
        except Exception as e:
            messages.error(request, "Error updating profile picture. Please try again.")
    return redirect("movies_profile")


@login_required
def update_user_info(request):
    if request.method == "POST":
        try:
            user = request.user
            user.name = request.POST.get("full_name", user.name)
            user.phone = request.POST.get("phone", user.phone)
            user.gender = request.POST.get("gender", user.gender)
            user.age = request.POST.get("age", user.age)
            user.save()
            messages.success(request, "Profile information updated successfully!")
        except Exception as e:
            messages.error(
                request, "Error updating profile information. Please try again."
            )
    return redirect("movies_profile")


@login_required
def movies_profile_view(request):
    try:
        comments = Comment.objects.filter(user = request.user.id)
        user = request.user
        user_profile = {
            "full_name": user.name if hasattr(user, "name") else "",
            "email": user.email,
            "phone": user.phone if hasattr(user, "phone") else "",
            "address": user.address if hasattr(user, "address") else "",
            "gender": user.gender if hasattr(user, "gender") else "",
            "profile_picture": user.image if hasattr(user, "image") else None,
            "cover_image": user.cover_image if hasattr(user, "cover_image") else None,
            "quote": (
                user.quote if hasattr(user, "quote") else "Welcome to your profile!"
            ),
            "age": user.age if hasattr(user, "age") else None,
        }

        data = {"user": user, "user_profile": user_profile , "comments" : comments}
        return render(request, "movies_profile.html", context=data)
    except Exception as e:
        print(f"Error in profile view: {str(e)}")  
        messages.error(
            request, f"An error occurred while loading your profile: {str(e)}"
        )
        return redirect("movies_home_page")


@login_required
def update_cover(request):
    if request.method == "POST" and request.FILES.get("cover_image"):
        try:
            user = request.user
            user.cover_image = request.FILES["cover_image"]
            user.save()
            messages.success(request, "Cover image updated successfully!")
        except Exception as e:
            messages.error(request, "Error updating cover image. Please try again.")
    return redirect("movies_profile")


@login_required
def update_quote(request):
    if request.method == "POST":
        try:
            user = request.user
            quote = request.POST.get("quote")
            if quote:
                user.quote = quote
                user.save()
                return JsonResponse({"status": "success"})
            return JsonResponse({"status": "error", "message": "Quote cannot be empty"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})
