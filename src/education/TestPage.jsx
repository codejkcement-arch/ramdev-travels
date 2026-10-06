import { useState } from 'react';
import { ChevronLeft, ChevronRight, Clock, CheckCircle2 } from 'lucide-react';
const qs=[
 'निम्नलिखित में से भारत का सबसे बड़ा राज्य कौन सा है?',
 'राजस्थान की राजधानी कौन सी है?',
 'भारत का संविधान कब लागू हुआ?'
];
export default function TestPage(){
 const [q,setQ]=useState(0); const [ans,setAns]=useState({});
 return <div className="page test-page"><div className="test-head"><div><span className="eyebrow">Mock Test</span><h1>Rajasthan Patwari Mock Test</h1></div><div className="timer"><Clock/> 01:58:24</div></div>
  <div className="test-layout"><section className="question-card"><div className="question-meta"><span>Question {q+1} / 100</span><span>1 Mark</span></div><h2>{qs[q]}</h2>
   {['A. मध्य प्रदेश','B. राजस्थान','C. महाराष्ट्र','D. उत्तर प्रदेश'].map(x=><label className="option" key={x}><input type="radio" name={'q'+q} checked={ans[q]===x} onChange={()=>setAns({...ans,[q]:x})}/><span>{x}</span></label>)}
   <div className="question-actions"><button onClick={()=>setQ(Math.max(0,q-1))}><ChevronLeft/> Previous</button><button className="primary" onClick={()=>setQ(Math.min(2,q+1))}>Next <ChevronRight/></button></div>
  </section><aside className="palette"><b>OMR Sheet</b><div className="palette-grid">{Array.from({length:20},(_,i)=><button className={i===q?'active':''} onClick={()=>setQ(Math.min(2,i))} key={i}>{i+1}</button>)}</div><div className="legend"><span><i/> Answered</span><span><i/> Not Answered</span></div><button className="submit"><CheckCircle2/> Submit Test</button></aside></div>
 </div>
}
