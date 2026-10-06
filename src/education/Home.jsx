import './education.css';
import { Link } from 'react-router-dom';
import { ArrowRight, BookOpen, ClipboardCheck, Users, ShieldCheck, GraduationCap } from 'lucide-react';

const exams = ['REET','Patwari','Gram Sevak','RAS','SSC','CET','Police','Railway'];

export default function EducationHome() {
  return (
    <div className="page">

      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">
            🎓 Free Coaching • Smart Learning
          </span>

          <h1>
            शिक्षा की नई राह,<br />
            <em>सफलता आपके साथ।</em>
          </h1>

          <p>
            Courses, Mock Tests, Online OMR Evaluation और Performance
            Analytics — एक ही platform पर।
          </p>

          <div className="hero-actions">
            <Link className="btn primary" to="/education/student">
              Student Dashboard <ArrowRight size={17}/>
            </Link>

            <Link className="btn ghost" to="/education/tests/demo">
              Mock Tests
            </Link>
          </div>
        </div>

        <div className="hero-art">
          <div className="orbit o1"></div>
          <div className="orbit o2"></div>

          <div className="hero-card">
            <div className="cap">
              <GraduationCap size={38}/>
            </div>
            <b>Learn. Practice. Grow.</b>
            <span>Rajasthan Competitive Exams</span>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <div>
            <span className="eyebrow">Popular Exams</span>
            <h2>अपनी तैयारी शुरू करें</h2>
          </div>
        </div>

        <div className="exam-grid">
          {exams.map((exam, i) => (
            <Link
              className="exam-card"
              key={exam}
              to="/education/tests/demo"
            >
              <div className="exam-no">
                {String(i + 1).padStart(2, '0')}
              </div>
              <b>{exam}</b>
              <span>Mock Tests • Notes • Results</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="feature-grid">

        <Link className="feature" to="/education/student">
          <BookOpen/>
          <b>Students</b>
          <span>Courses, tests & progress</span>
        </Link>

        <Link className="feature" to="/education/student">
          <Users/>
          <b>Teachers</b>
          <span>Create and manage content</span>
        </Link>

        <Link className="feature" to="/education/tests/demo">
          <ClipboardCheck/>
          <b>Evaluation</b>
          <span>Online tests + OMR</span>
        </Link>

        <Link className="feature" to="/admin">
          <ShieldCheck/>
          <b>Administration</b>
          <span>Role-based administration</span>
        </Link>

      </section>

    </div>
  );
}
