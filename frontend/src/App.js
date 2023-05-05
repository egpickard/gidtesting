import React from "react"; //Source #4
import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages";
import Begin from "./pages/begin";
import HowTo from "./pages/howto";
import AboutGid from "./pages/aboutgid";
import AboutUs from "./pages/aboutus";
import OnlineAnalysis from "./pages/onlineanalysis";

const App = () => {
  return (
    <nav className="navbar">
      <div className="nav-elements">
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/home" element={<Home />} />
            <Route path="/begin" element={<Begin />} />
            <Route path="/howto" element={<HowTo />} />
            <Route path="/aboutgid" element={<AboutGid />} />
            <Route path="/aboutus" element={<AboutUs />} />
            <Route path="/onlineAnalysis" element={<OnlineAnalysis />} />
          </Routes>
        </Router>
      </div>
    </nav>
  );
};

export default App;
