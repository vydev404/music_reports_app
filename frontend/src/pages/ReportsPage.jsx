// Файл: /src/pages/ReportsPage.jsx
import { useState, useEffect } from "react";
import Table from "../components/Table";
import Modal from "../components/Modal";

function ReportsPage() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/v1/reports")
      .then((response) => response.json())
      .then((data) => setReports(data.data))
      .catch((error) => console.error("Помилка завантаження звітів:", error));
  }, []);

  // Ключі для виводу у таблиці
  const columns = ["id", "name", "status", "created_at"];

  return (
    <div>
      <h2>Список звітів</h2>
      <Table data={reports} columns={columns} onRowClick={setSelectedReport} />
      {selectedReport && <Modal data={selectedReport} onClose={() => setSelectedReport(null)} />}
    </div>
  );
}

export default ReportsPage;

