import axios from "axios";
import { useAuthStore } from "@/stores/authStrore";
import { refreshAccessToken } from "./auth";

const api = axios.create({
    baseURL: "/api/v1"
});

api.interceptors.request.use(config => {
    const auth = useAuthStore();

    if (auth.accessToken) {
        config.headers.Authorization = `Bearer ${auth.accessToken}`
    }

    return config;
})

api.interceptors.response.use(
    response => response,
    async error => {
        const auth = useAuthStore();

        const originalRequest = error.config;

        const isAuthEndpoint =
            originalRequest.url.includes("/users/login/") ||
            originalRequest.url.includes("/users/logout/") ||
            originalRequest.url.includes("/token/refresh/")

        if (error.response?.status == 401 && !originalRequest._retry && !isAuthEndpoint) {
            originalRequest._retry = true;

            try {
                const refresh = localStorage.getItem("refresh");
                if (!refresh) throw new Error("No refresh token");
                const token = await refreshAccessToken(refresh);
                auth.accessToken = token;
                originalRequest.headers.Authorization = `Bearer ${token}`;

                return api(originalRequest);
            }
            catch (err) {
                auth.logout();
                return Promise.reject(err);
            }
        }

        return Promise.reject(error);
    }
)

export default api;