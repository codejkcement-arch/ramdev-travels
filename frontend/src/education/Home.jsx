import { Link } from 'react-router-dom';
import { ArrowRight, BookOpen, ClipboardCheck, Users, ShieldCheck, Sparkles } from 'lucide-react';

const exams=['REET','Patwari','Gram Sevak','RAS','SSC','CET','Police','Railway'];

export default function Home(){
 return <div className="page">
  <section className="hero">
   <div className="hero-copy"><span className="eyebrow"><Sparkles size={15}/> Free Coaching • Smart Learning</span>
    <h1>शिक्षा की नई राह,<br/><em>सफलता आपके साथ।</em></h1>
    <p>Courses, live classes, mock tests, OMR evaluation और performance analytics — एक ही platform पर.</p>
    <div className="hero-actions"><Link className="btn primary" to="/student">Student Dashboard <ArrowRight size={17}/></Link><Link className="btn ghost" to="/student/tests">Mock Tests</Link></div>
   </div>
   <div className="hero-art"><div className="orbit o1"/><div className="orbit o2"/><div className="hero-card"><GraduationCapIcon/><b>Learn. Practice. Grow.</b><span>Rajasthan Competitive Exams</span></div></div>
  </section>
  <section className="section"><div className="section-head"><div><span className="eyebrow">Popular exams</span><h2>अपनी तैयारी शुरू करें</h2></div></div>
   <div className="exam-grid">{exams.map((x,i)=><div className="exam-card" key={x}><div className="exam-no">0{i+1}</div><b>{x}</b><span>Mock Tests • Notes • Results</span></div>)}</div>
  </section>
  <section className="feature-grid">
   {[['Students','Courses, tests & progress',BookOpen],['Teachers','Create and manage content',Users],['Evaluation','Online tests + OMR',ClipboardCheck],['Secure','Role-based administration',ShieldCheck]].map(([a,b,I])=><div className="feature" key={a}><I/><b>{a}</b><span>{b}</span></div>)}
  </section>
 </div>
}
function GraduationCapIcon(){return <div className="cap"><GraduationCap size={38}/></div>}
