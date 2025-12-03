from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import requests

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

from .validators import get_or_create_movie_from_external_id, get_or_search_movie_from_external_id
from .models import Movie, Rating, UserProfile
from .serializers import UserSerializer, MovieSerializer, RatingSerializer
from .permissions import IsSuperUserOrReadOnly
from .utils import update_recommendations, API_BASE_URL, API_KEY

# ****  USER **** #

# Register view
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        UserProfile.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid Credentials!'}, status=status.HTTP_401_UNAUTHORIZED)

# ****  RATING **** #

@api_view(['GET', 'POST', 'UPDATE'])
@permission_classes([IsAuthenticated])
def ratings(request):
    if request.method == 'GET':
        ratings = Rating.objects.filter(user=request.user)
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Check if the movie exists
        external_id = request.data.get('movie')
        movie = get_or_create_movie_from_external_id(external_id)
        if not movie:
            return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Prevent users from rating the same movie multiple times
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            movie_obj = serializer.validated_data['movie']
            if (Rating.objects.filter(user=request.user, movie=movie_obj).exists()):
                return Response({'error': 'You have already rated this movie.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'UPDATE':
        # TODO: Implement update logic for ratings
        serializer = RatingSerializer(data=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# **** WATCHED MOVIES **** #

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watched_movies(request):
    if request.method == 'GET':
        user_profile = request.user.userprofile
        watched_movies = user_profile.watched_movies.all()
        serializer = MovieSerializer(watched_movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        movie_id = request.data.get('external_id')
        movie = get_or_create_movie_from_external_id(movie_id)
        if not movie:
            return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
        user_profile = request.user.userprofile
        # Check if movie is already in watched movies
        if user_profile.watched_movies.filter(pk=movie.pk).exists():
            return Response({'error': 'Movie already in your watched movies.'}, status=status.HTTP_400_BAD_REQUEST)
        user_profile.watched_movies.add(movie)
        return Response({'message': f'Movie "{movie.title}" added to your watched movies.'}, status=status.HTTP_200_OK)

# **** WATCH LIST **** #

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def watch_list(request):
    if request.method == 'GET':
        user_profile = request.user.userprofile
        watch_list_movies = user_profile.watch_list.all()
        serializer = MovieSerializer(watch_list_movies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        movie = get_or_create_movie_from_external_id(request.data.get('external_id'))
        if not movie:
            return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
        user_profile = request.user.userprofile
        # Check if movie is already in watch list
        if user_profile.watch_list.filter(pk=movie.pk).exists():
            return Response({'error': 'Movie already in your watch list.'}, status=status.HTTP_400_BAD_REQUEST)
        user_profile.watch_list.add(movie)
        return Response({'message': f'Movie "{movie.title}" added to your watch list.'}, status=status.HTTP_200_OK)

# **** RECOMMENDED MOVIES **** #

@api_view(['GET', 'UPDATE'])
@permission_classes([IsAuthenticated])
def recommended_movies_list(request):
    if request.method == 'GET':
        user_profile = request.user.userprofile
        recommended = user_profile.recommended_movies.all()
        serializer = MovieSerializer(recommended, many=True)
        return Response(serializer.data)
    elif request.method == 'UPDATE':
        user_profile = request.user.userprofile
        recommended = user_profile.update_recommendations()
        serializer = MovieSerializer(recommended, many=True)
        return Response(serializer.data)
    
# **** MOVIE BY ID **** #
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_by_id(request):
    external_id = request.data.get('external_id')
    if not external_id:
        return Response({'error': 'external_id parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    movie = get_or_search_movie_from_external_id(external_id)
    if not movie:
        return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

# **** MOVIES CATALOG **** #

# Map of genre IDs to names
GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western",
}

def format_movie(movie):
    # check if movie has the required fields
    title = movie.get('title', '').strip()
    poster = movie.get('poster_path')
    movie_id = movie.get('id')
    
    if not title or not poster or not movie_id:
        return None
    
    # get genres
    genre_ids = movie.get('genre_ids', [])
    genre_names = []
    for genre_id in genre_ids:
        if genre_id in GENRE_MAP:
            genre_names.append(GENRE_MAP[genre_id])
        else:
            genre_names.append("Unknown")
    
    if genre_names:
        genre_string = ", ".join(genre_names)
    else:
        genre_string = "Unknown"
    
    # extract year
    date = movie.get('release_date', '')
    year = None
    if date:
        try:
            year = int(date.split('-')[0])
        except:
            pass
    
    # build poster url
    poster_url = f"https://image.tmdb.org/t/p/w185{poster}"
    
    # get rating
    rating = movie.get('vote_average', 0)
    try:
        rating_float = round(float(rating), 1)
    except:
        rating_float = 0.0
    
    return {
        "external_id": movie_id,
        "title": title,
        "poster_url": poster_url,
        "genre": genre_string,
        "year": year,
        "average_rating": rating_float,
    }

def fetch_movies(url, params, limit=20):
    try:
        response = requests.get(url, params=params)
        data = response.json()
        movies = data.get('results', [])
        
        result = []
        for movie in movies:
            if len(result) >= limit:
                break
            
            formatted = format_movie(movie)
            if formatted:
                result.append(formatted)
        
        return result
    except Exception as e:
        return []

def search_by_director(director_name):
    try:
        # search for the person first
        url = f"{API_BASE_URL}/search/person"
        params = {"api_key": API_KEY, "query": director_name, "page": 1}
        response = requests.get(url, params=params)
        data = response.json()
        people = data.get('results', [])
        
        if not people:
            return []
        
        # get the first person found (usually the most popular one)
        person_id = people[0].get('id')
        
        # now get all movies this person worked on
        url = f"{API_BASE_URL}/person/{person_id}/movie_credits"
        params = {"api_key": API_KEY}
        response = requests.get(url, params=params)
        data = response.json()
        crew = data.get('crew', [])
        
        result = []
        for job in crew:
            if len(result) >= 20:
                break
            
            # only get movies where they were director
            if job.get('job') == 'Director':
                formatted = format_movie(job)
                if formatted:
                    result.append(formatted)
        
        return result
    except:
        return []

def search_by_genre(genre_name):
    try:
        # look up the genre id
        genre_id = None
        for gid, gname in GENRE_MAP.items():
            if gname.lower() == genre_name.lower():
                genre_id = gid
                break
        
        if not genre_id:
            return []
        
        # get movies for this genre
        url = f"{API_BASE_URL}/discover/movie"
        params = {"api_key": API_KEY, "with_genres": genre_id, "sort_by": "popularity.desc", "page": 1}
        response = requests.get(url, params=params)
        data = response.json()
        movies = data.get('results', [])
        
        result = []
        for movie in movies:
            if len(result) >= 20:
                break
            
            formatted = format_movie(movie)
            if formatted:
                result.append(formatted)
        
        return result
    except:
        return []

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movies_catalog(request):
    search = request.GET.get('search', '').strip()
    search_type = request.GET.get('search_type', 'title').strip().lower()

    # handle search
    if search:
        if search_type == 'director':
            movies = search_by_director(search)
        elif search_type == 'genre':
            movies = search_by_genre(search)
        else:
            # default is title search
            url = f"{API_BASE_URL}/search/movie"
            params = {"api_key": API_KEY, "query": search, "page": 1}
            movies = fetch_movies(url, params, limit=20)
        
        return Response(movies)
    
    # return catalog with different sections
    catalog = {}
    
    # popular movies
    url = f"{API_BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "page": 1}
    catalog["popular"] = fetch_movies(url, params, limit=20)
    
    # top rated
    url = f"{API_BASE_URL}/movie/top_rated"
    params = {"api_key": API_KEY, "page": 1}
    catalog["top_rated"] = fetch_movies(url, params, limit=20)
    
    # action
    url = f"{API_BASE_URL}/discover/movie"
    params = {"api_key": API_KEY, "with_genres": 28, "sort_by": "popularity.desc", "page": 1}
    catalog["action"] = fetch_movies(url, params, limit=20)
    
    # comedy
    url = f"{API_BASE_URL}/discover/movie"
    params = {"api_key": API_KEY, "with_genres": 35, "sort_by": "popularity.desc", "page": 1}
    catalog["comedy"] = fetch_movies(url, params, limit=20)
    
    # drama
    url = f"{API_BASE_URL}/discover/movie"
    params = {"api_key": API_KEY, "with_genres": 18, "sort_by": "popularity.desc", "page": 1}
    catalog["drama"] = fetch_movies(url, params, limit=20)
    
    return Response(catalog)
