import {Link} from "react-router-dom";
import {useDispatch,useSelector} from "react-redux";
import {logout} from "../../store/authSlice";
export default function Navbar(){
 const user=useSelector(s=>s.auth.user), dispatch=useDispatch();
 return <nav style={{background:"#991b1b",color:"white",padding:"14px 0"}}><div className="container" style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
 <Link to="/" style={{color:"white",fontWeight:800,fontSize:22,textDecoration:"none"}}>Ramdev Travels</Link>
 <div style={{display:"flex",gap:16,alignItems:"center"}}><Link to="/bookings" style={{color:"white"}}>My Bookings</Link>
 {user?<><span>{user.name}</span><button onClick={()=>dispatch(logout())}>Logout</button></>:<Link to="/login" style={{color:"white"}}>Login</Link>}</div></div></nav>
}
