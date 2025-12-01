import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar({ user, onLogout }) {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    onLogout();
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h1 className="navbar-logo" onClick={() => navigate("/")}>
          FilmHub
        </h1>

        <div className="navbar-links">
          <button className="navbar-link" onClick={() => navigate("/")}>
            Home
          </button>
          <button
            className="navbar-link"
            onClick={() => navigate("/recommendations")}
          >
            Recommendations
          </button>
        </div>

        <div className="navbar-user">
          <button
            className="navbar-user-btn"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {user?.username || "User"}
          </button>

          {menuOpen && (
            <div className="navbar-dropdown">
              <button
                className="navbar-dropdown-item"
                onClick={() => navigate("/ratings")}
              >
                My Ratings
              </button>
              <button
                className="navbar-dropdown-item navbar-logout"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
