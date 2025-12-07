import { useState, useEffect, useCallback } from "react";
import MovieList from "../../components/MovieList/MovieList";
import { movieService } from "../../services/movieService";
import "./Ratings.css";

export default function Ratings() {
  const [ratings, setRatings] = useState([]);
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadRatings = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const ratingsData = await movieService.getRatings();
      const ratingsArray = Array.isArray(ratingsData) ? ratingsData : [];
      setRatings(ratingsArray);

      const allMovies = await movieService.getMovies();

      const ratedMovieIds = ratingsArray.map((rating) => rating.movie);

      // Flatten the catalog object into a single array
      let allMoviesFlat = [];
      
      if (typeof allMovies === 'object' && allMovies !== null) {
        Object.values(allMovies).forEach((category) => {
          if (Array.isArray(category)) {
            allMoviesFlat = [...allMoviesFlat, ...category];
          }
        });
      } else if (Array.isArray(allMovies)) {
        allMoviesFlat = allMovies;
      }
      
      // Remove duplicates
      const uniqueMovies = allMoviesFlat.reduce((acc, movie) => {
        if (!acc.find(m => m.external_id === movie.external_id)) {
          acc.push(movie);
        }
        return acc;
      }, []);

      // Filter only rated movies
      const moviesFromRatings = uniqueMovies.filter((movie) =>
        ratedMovieIds.includes(movie.external_id)
      );

      setMovies(moviesFromRatings);
    } catch (err) {
      console.error("Error loading ratings:", err);
      setError("Error loading your ratings. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadRatings();
  }, [loadRatings]);

  const handleRate = async (movieId, rating) => {
    try {
      setError("");
      setSuccessMessage("");
      
      await movieService.rateOrUpdateMovie(movieId, rating);
      
      setSuccessMessage("Rating saved successfully!");
      
      await loadRatings();
      
      setTimeout(() => setSuccessMessage(""), 3000);
    } catch (err) {
      console.error("Error rating movie:", err);
      setError(err.message || "Error saving rating. Please try again.");
    }
  };

  return (
    <div className="ratings-page">
      <div className="ratings-content">
        <header className="ratings-header">
          <h1 className="ratings-title">My Ratings</h1>
          <p className="ratings-subtitle">Movies you've rated and reviewed</p>
        </header>
        
        <main className="ratings-movies">
          {successMessage && (
            <div className="success-message" style={{
              backgroundColor: '#4caf50',
              color: 'white',
              padding: '12px 20px',
              borderRadius: '4px',
              marginBottom: '20px',
              textAlign: 'center'
            }}>
              {successMessage}
            </div>
          )}
          
          {error && (
            <div className="error-message" style={{
              backgroundColor: '#f44336',
              color: 'white',
              padding: '12px 20px',
              borderRadius: '4px',
              marginBottom: '20px',
              textAlign: 'center'
            }}>
              {error}
            </div>
          )}
          
          <MovieList
            title=""
            movies={movies}
            loading={loading}
            error={error}
            onRate={handleRate}
            emptyMessage="You haven't rated any movies yet"
            ratings={ratings}
          />
        </main>
      </div>
    </div>
  );
}