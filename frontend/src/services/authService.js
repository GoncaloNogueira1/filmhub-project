const API_URL = "http://localhost:8000/api";

export const authService = {
  login: async (username, password) => {
    const response = await fetch(`${API_URL}/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });
    return response.json();
  },

  logout: () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  },

  register: async (username, email, password) => {
    const response = await fetch(`${API_URL}/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password }),
    });
    return response.json();
  },

  saveToken: (token, user) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));
  },
};
