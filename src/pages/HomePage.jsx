import {Link} from "react-router-dom"; import BusSearch from "../components/Bookings/BusSearch";
export default function HomePage(){return <><section style={{padding:"60px 0",background:"#fee2e2"}}><div className="container"><h1 style={{fontSize:42,margin:0}}>Travel made simple.</h1><p>Bus, flight and cinema booking in one place.</p><Link className="btn" to="/booking">Start booking</Link></div></section><div className="container" style={{marginTop:30}}><BusSearch onSelect={()=>{}}/></div>
<section style={{margin:"50px 0",padding:"45px 25px",background:"linear-gradient(135deg,#fff7ed,#eff6ff)",borderRadius:20}}>
<div className="container">
<h2 style={{fontSize:32,marginTop:0}}>🎓 Ramdev Education Platform</h2>
<p style={{fontSize:18,lineHeight:1.6}}>Students, Teachers, Tests and Online OMR Evaluation — all in one platform.</p>
<Link className="btn" to="/education">Explore Education Platform →</Link>
</div>
</section></>}
