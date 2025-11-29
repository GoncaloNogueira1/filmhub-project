import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import AuthContext from "../context/AuthProvider";
import { authService } from "../services/authService";

const useAuth = () => {
  const context = useContext(AuthContext);
  const navigate = useNavigate();

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  const { setAuth } = context;

  const logout = () => {
    setAuth({});
    authService.logout();
    navigate("/login", { replace: true });
  };

  return { ...context, logout };
};

export default useAuth;
