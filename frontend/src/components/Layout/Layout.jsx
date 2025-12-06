import { Outlet, useLocation } from "react-router-dom";
import Navbar from "../Navbar/Navbar";
import useAuth from "../../hooks/useAuth";

const Layout = () => {
  const { auth, logout } = useAuth();
  const location = useLocation();

  const showNavbar = location.pathname !== "/login";

  return (
    <main className="App">
      <div className="content">
        <Outlet />
        {showNavbar && <Navbar user={auth.user} onLogout={logout} />}
      </div>
    </main>
  );
};

export default Layout;