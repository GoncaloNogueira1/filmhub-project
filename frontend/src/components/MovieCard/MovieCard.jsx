import { useNavigate } from "react-router-dom";
import "./MovieCard.css";

export default function MovieCard({ movie, userRatings = [] }) {
  const navigate = useNavigate();
  
  // Find user's rating for this movie
  const userRatingObj = userRatings.find(r => r.movie === movie.external_id);
  const userRating = userRatingObj ? userRatingObj.score : 0;

  const renderStars = (rating, size = 'small') => {
    const stars = [];
    for (let i = 1; i <= 10; i++) {
      const filled = i <= Math.round(rating);
      stars.push(
        <span
          key={i}
          className={`star star-${size} ${filled ? "star-filled" : "star-empty"}`}
        >
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <div className="movie-card">
      <div
        className="movie-card-poster"
        onClick={() => navigate(`/movie/${movie.external_id}`)}
      >
        {movie.poster_url ? (
          <img src={movie.poster_url} alt={movie.title} />
        ) : (
          <div className="movie-card-placeholder">
            <span></span>
          </div>
        )}
      </div>

      <div className="movie-card-info">
        <h3 className="movie-card-title">{movie.title}</h3>

        <div className="movie-card-meta">
          <span className="movie-card-year">{movie.year}</span>
          <span className="movie-card-genre">{movie.genre}</span>
        </div>

        <div className="movie-card-rating">
          <div className="movie-card-avg-rating">
            {renderStars(movie.average_rating || 0, 'small')}
            <span className="rating-value">
              {movie.average_rating ? movie.average_rating.toFixed(1) : "N/A"}
            </span>
          </div>
        </div>

        <div className="movie-card-user-rating">
          <span className="your-rating-label">Your rating:</span>
          <div className="your-rating-container">
            {userRating > 0 ? (
              <div className="your-rating-display">
                <div className="your-rating-stars">{renderStars(userRating, 'small')}</div>
                <span className="your-rating-number">{userRating}</span>
              </div>
            ) : (
              <span className="your-rating-none">Not rated</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}