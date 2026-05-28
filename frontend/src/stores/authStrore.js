import { defineStore } from "pinia";
import { login, logout } from "@/api/auth";
import axios from "axios";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        accessToken: null,
        user: null,
        authChecked : false
    }),
    actions: {
        async restoreSession(){
            const refresh = localStorage.getItem("refresh");

            if (!refresh){
                this.authChecked = true;
                return;
            }

            try{
                const response = await axios.post("/api/token/refresh/",{
                    refresh: refresh
                })

                this.accessToken = response.data.access;
                localStorage.setItem("refresh",response.data.refresh);
            }catch(error){
                localStorage.removeItem("refresh")
            }

            this.authChecked = true;
        },

        async login(email, password) {
            try {
                const response = await login({
                    email,
                    password
                })

                this.accessToken = response.data.access;
                localStorage.setItem("refresh",response.data.refresh);
                this.user = {
                    email
                }
            } catch (e) {
                this.accessToken = null;
                this.user = null;
            }
        },

        async logout() {
            try {
                const response = await logout();

                this.accessToken = null;
                localStorage.removeItem("refresh");
                this.user = null;
                return true;
            } catch (err) {
                return false;
            }
        }
    }
})