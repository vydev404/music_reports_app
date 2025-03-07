// Файл: /src/components/Sidebar.jsx
import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <nav>
        <ul>
          <li><Link to="/">Файли</Link></li>
          <li><Link to="/musics">Музика</Link></li>
          <li><Link to="/reports">Звіти</Link></li>
          <li><Link to="/tasks">Черга завдань</Link></li>
        </ul>
      </nav>
    </aside>
  );
}

export default Sidebar;

