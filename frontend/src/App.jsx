import { useState } from "react";
import AnalyzePage from "./pages/AnalyzePage";
import ComparePage from "./pages/ComparePage";
import AboutPage from "./pages/AboutPage";
import "./App.css";

function App() {
  const [activePage, setActivePage] = useState("analyze");

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">A</div>
          <div>
            <h1>Academic Analyzer</h1>
            <p>OCR-based academic document insights</p>
          </div>
        </div>

        <nav className="sidebar-nav">
          <button
            className={activePage === "analyze" ? "nav-link active" : "nav-link"}
            onClick={() => setActivePage("analyze")}
          >
            Analyze
          </button>
          <button
            className={activePage === "compare" ? "nav-link active" : "nav-link"}
            onClick={() => setActivePage("compare")}
          >
            Compare
          </button>
          <button
            className={activePage === "about" ? "nav-link active" : "nav-link"}
            onClick={() => setActivePage("about")}
          >
            About
          </button>
        </nav>

        <div className="sidebar-note">
          Your document is processed temporarily and is not permanently stored.
        </div>
      </aside>

      <main className="main-content">
        {activePage === "analyze" && <AnalyzePage />}
        {activePage === "compare" && <ComparePage />}
        {activePage === "about" && <AboutPage />}
      </main>
    </div>
  );
}

export default App;
