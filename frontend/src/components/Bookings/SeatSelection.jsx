import {useEffect,useState} from "react"; import {seats} from "../../services/bookingService";
export default function SeatSelection({bus,onConfirm}){const [rows,setRows]=useState([]),[selected,setSelected]=useState([]);
 useEffect(()=>{seats(bus.id).then(r=>setRows(r.data))},[bus.id]);
 const toggle=s=>!s.is_booked&&setSelected(x=>x.includes(s.seat_number)?x.filter(y=>y!==s.seat_number):[...x,s.seat_number]);
 return <div className="card"><h2>Select Seats</h2><div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:8}}>{rows.map(s=><button key={s.id} disabled={s.is_booked} onClick={()=>toggle(s)} style={{padding:10,borderRadius:8,background:selected.includes(s.seat_number)?"#16a34a":s.is_booked?"#ddd":"#fff"}}>{s.seat_number}</button>)}</div><button className="btn" style={{marginTop:20}} disabled={!selected.length} onClick={()=>onConfirm(selected)}>Continue</button></div>}
