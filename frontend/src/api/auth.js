import api from "./client";

export function login(data){
    return api.post("/users/login/",data);
}

export function register(data){
    return api.post("/users/register/",data);
}

export function logout(){
    return api.post("/users/logout/",{
      refresh : localStorage.getItem("refresh")
    });
}

export async function refreshAccessToken(refresh) {
  try {
    const response = await fetch("/api/token/refresh/", {
      method: "POST",
      body : {
        refresh
      }
    })

    if (!response.ok) throw new Error("Refresh failed")

    const data = await response.json()
    const { access } = data
    localStorage.setItem("refresh",data.refresh);
    return access
  } catch (err) {
    console.error("Token refresh error:", err)
    return null
  }
}
