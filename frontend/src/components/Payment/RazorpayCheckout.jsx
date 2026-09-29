import {createOrder,verifyPayment} from "../../services/paymentService";
export default function RazorpayCheckout({booking,onPaid}){async function pay(){const r=await createOrder(booking.id);if(!r.data.key_id){alert("Configure Razorpay keys on the backend.");return}
 if(!window.Razorpay){alert("Load Razorpay Checkout script in your app before payment.");return}
 const options={key:r.data.key_id,amount:r.data.amount,currency:r.data.currency,name:"Ramdev Travels",order_id:r.data.order_id,
 handler:async response=>{await verifyPayment({booking_id:booking.id,razorpay_order_id:response.razorpay_order_id,razorpay_payment_id:response.razorpay_payment_id,razorpay_signature:response.razorpay_signature});onPaid()}};
 new window.Razorpay(options).open();}
 return <button className="btn" onClick={pay}>Pay ₹{booking.amount}</button>}
