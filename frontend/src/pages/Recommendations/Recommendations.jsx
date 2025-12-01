import { useState, useCallback } from "react";
import MovieList from "../../components/MovieList/MovieList";

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);
  const [recommendationsLoading, setRecommendationsLoading] = useState(false);

  const handleRate = useCallback((movieId, rating) => {
    console.log(`Rated movie ${movieId} with ${rating} stars`);
  }, []);

  const handleSelectMovie = useCallback((movieId) => {
    console.log(`Selected movie ${movieId}`);
  }, []);

  if (recommendations.length === 0 && !recommendationsLoading) {
    return (
      <div className="movie-list-section">
        <h2 className="movie-list-title">Recommended for You</h2>
        <div className="movie-list-empty">
          <span className="empty-icon"></span>
          <p>Rate some movies to get personalized recommendations!</p>
        </div>
      </div>
    );
  }
  return (
    <MovieList
      title="Recommended for You"
      movies={recommendations}
      loading={recommendationsLoading}
      error={""}
      onRate={handleRate}
      onSelectMovie={handleSelectMovie}
      emptyMessage="Rate some movies to get recommendations!"
    />
  );
}
