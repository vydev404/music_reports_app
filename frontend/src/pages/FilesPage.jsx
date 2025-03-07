// Файл: /src/pages/FilesPage.jsx
import { useState, useEffect } from "react";
import Table from "../components/Table";
import Modal from "../components/Modal";

function FilesPage() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/v1/files")
      .then((response) => response.json())
      .then((data) => setFiles(data.data.files))
      .catch((error) => console.error("Помилка завантаження файлів:", error));
  }, []);

  // Ключі для виводу у таблиці (не всі з API)
  const columns = ["name", "path", "created_at", "updated_at", "status", "error_stage", "error_message"];
  const headers = ["Name", "Source file", "Created", "Modified", "Status", "Error Stage", "Error Message"]

  return (
    <div>
      <h2>Файли</h2>
      <Table data={files} columns={columns} headers={headers} onRowClick={setSelectedFile} />
      {selectedFile && <Modal data={selectedFile} onClose={() => setSelectedFile(null)} />}
    </div>
  );
}

export default FilesPage;

