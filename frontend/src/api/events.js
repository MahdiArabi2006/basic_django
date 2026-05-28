import api from "./client";

export function getEvents(){
    return api.get("/events/");
}

export function createEvent(data){
    return api.post("/events/",data);
}

export function deleteEvent(id){
    return api.delete(`/events/${id}/`);
}

export function updateEvent(id,data){
    return api.patch(`/events/${id}/`,data);
}

export function getCategories(){
    return api.get("/categories/");
}

export function createCategories(data){
    return api.post("/categories/",data);
}

export function deleteCategories(id){
    return api.delete(`/categories/${id}/`);
}

export function updateCategories(id,data){
    return api.patch(`/categories/${id}/`,data);
}
