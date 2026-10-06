import { NavLink, Outlet } from 'react-router-dom';
import { BookOpen, Home, GraduationCap, Users, ClipboardCheck, Settings, LogIn } from 'lucide-react';

const links=[
 ['/', 'Home', Home], ['/student','Student Dashboard',GraduationCap],
 ['/student/courses','Courses',BookOpen], ['/student/tests','Tests',ClipboardCheck],
 ['/teacher','Teacher',Users], ['/admin','Admin',Settings]
];

export default function EducationLayout(){
 return <div className="app-shell">
  <aside className="sidebar">
   <div className="brand"><span className="brand-mark">◆</span><div><b>Ramdev Travels</b><small>Education Platform</small></div></div>
   <nav>{links.map(([to,label,Icon])=><NavLink key={to} to={to} end={to==='/'}>
      <Icon size={18}/><span>{label}</span>
   </NavLink>)}</nav>
   <div className="side-bottom"><NavLink to="/login"><LogIn size={18}/> Login / Register</NavLink></div>
  </aside>
  <main className="main">
   <header className="topbar"><div className="mobile-brand">Ramdev Education</div><div className="top-actions"><span>🔔</span><div className="avatar">RS</div></div></header>
   <Outlet/>
  </main>
 </div>
}
