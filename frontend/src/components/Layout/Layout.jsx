import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <main className="App">
      <div className="content">
        <Outlet />
      </div>
    </main>
  );
};

export default Layout;
