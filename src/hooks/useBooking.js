import {useSelector} from "react-redux";
export default function useBooking(){return useSelector(s=>s.booking);}
