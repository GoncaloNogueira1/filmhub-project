from django.core.exceptions import ValidationError

from ..models import Movie
from ..utils import create_movie_from_external_id
    
def get_or_create_movie_from_external_id(movie_id):
    movie = None
    try:
        movie = Movie.objects.get(external_id=movie_id)
    except Movie.DoesNotExist:
        movie = create_movie_from_external_id(movie_id)
        if not movie:
            return None
    return movie