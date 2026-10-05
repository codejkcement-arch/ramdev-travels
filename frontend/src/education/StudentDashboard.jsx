import { Link } from 'react-router-dom';
import { BookOpen, ClipboardCheck, Trophy, Clock, ArrowUpRight } from 'lucide-react';

const courses=[['REET Level 1 & 2','Education','72%'],['Patwari Complete Course','General Science','48%'],['Gram Sevak','Rajasthan GK','61%'],['CET','Maths & Reasoning','35%']];
export default function StudentDashboard(){
 return <div className="page">
  <div className="page-title"><div><span className="eyebrow">Student Portal</span><h1>Welcome, Rohit 👋</h1><p>Keep learning, keep growing.</p></div><div className="rank-pill"><Trophy size={17}/> Rank #42</div></div>
  <div className="stats">{[['12','Total Courses',BookOpen],['5','Tests Attempted',ClipboardCheck],['76%','Average Score',ArrowUpRight],['42','Current Rank',Trophy]].map(([v,l,I])=><div className="stat" key={l}><div className="stat-icon"><I size={18}/></div><div><b>{v}</b><span>{l}</span></div></div>)}</div>
  <section className="panel"><div className="panel-head"><h2>My Courses</h2><Link to="/student/courses">View all <ArrowUpRight size={15}/></Link></div>
   <div className="course-grid">{courses.map(([t,s,p])=><div className="course-card" key={t}><div className="course-cover"><BookOpen/><span>{p}</span></div><div className="course-body"><b>{t}</b><span>{s}</span><div className="progress"><i style={{width:p}}/></div><button>Continue</button></div></div>)}</div>
  </section>
  <section className="panel"><div className="panel-head"><h2>Upcoming Tests</h2><Link to="/student/tests">View all</Link></div>
   <div className="test-list">{['Rajasthan Patwari Mock Test','REET Level 1 Test','Gram Sevak Full Mock'].map((x,i)=><div className="test-row" key={x}><div className="test-icon"><ClipboardCheck/></div><div><b>{x}</b><span>Oct {i+1}, 2026 • {10+i}:00 AM • 100 Questions</span></div><Link className="mini-btn" to="/test/demo">Start Test</Link></div>)}</div>
  </section>
 </div>
}
