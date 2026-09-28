import api from "./api";
export const searchBuses = params => api.get("/buses/search",{params});
export const seats = id => api.get(`/buses/${id}/seats`);
export const searchFlights = params => api.get("/flights/search",{params});
export const createBooking = data => api.post("/bookings",data);
export const history = () => api.get("/bookings");

export const searchCinema = params => api.get("/cinema/search",{params});
