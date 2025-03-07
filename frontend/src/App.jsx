import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Sidebar from "./components/Sidebar";
import FilesPage from "./pages/FilesPage";
import MusicsPage from "./pages/MusicsPage";
import ReportsPage from "./pages/ReportsPage";
import TasksPage from "./pages/TasksPage";

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
          <main className="main-container">
            <Routes>
              <Route path="/" element={<FilesPage />} />
              <Route path="/musics" element={<MusicsPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/tasks" element={<TasksPage />} />
            </Routes>
          </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
