import { useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import useAuth from "./hooks/useAuth";
import Layout from "./components/Layout/Layout";
import RequireAuth from "./components/RequireAuth/RequireAuth";
import Auth from "./pages/Auth/Auth"; // Ensure this path is correct
import MainPage from "./pages/MainPage/MainPage";
import "./App.css";

function App() {
  const { setAuth } = useAuth();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");

    if (token && savedUser) {
      setAuth({
        user: JSON.parse(savedUser),
        token: token,
      });
    }

    setLoading(false);
  }, [setAuth]);

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="login" element={<Auth />} />

        <Route element={<RequireAuth />}>
          <Route path="mainpage" element={<MainPage />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
