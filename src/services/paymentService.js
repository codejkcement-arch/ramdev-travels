import api from "./api";
export const createOrder = booking_id => api.post("/payments/create-order",{booking_id});
export const verifyPayment = data => api.post("/payments/verify",data);
