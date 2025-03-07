// Файл: /src/components/Header.jsx
import { Link } from "react-router-dom";
import logo from "/vylogo.png"; // Додай лого в /public

function Header() {
  return (
    <header className="header-container">
      <div className="header-site">
          <div className="header-site-item">
              <img className="site-logo" src={logo} alt="Logo"/>
          </div>
          <div className="header-site-item">
              <h1>Music Reports</h1>
          </div>
      </div>
        <nav className="header-nav">
        <Link className="header-nav-link" to="/">Файли</Link>
        <Link className="header-nav-link" to="/musics">Музика</Link>
        <Link className="header-nav-link" to="/reports">Звіти</Link>
        <Link className="header-nav-link" to="/tasks">Черга завдань</Link>
      </nav>
    </header>
  );
}

export default Header;

