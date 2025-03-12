// Файл: /src/pages/MusicsPage.jsx
import { useState, useEffect } from "react";
import Table from "../components/Table";
import Modal from "../components/Modal";

function MusicsPage() {
  const [musics, setMusics] = useState([]);
  const [selectedMusic, setSelectedMusic] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/v1/musics")
      .then((response) => response.json())
      .then((data) => setMusics(data.data.files))
      .catch((error) => console.error("Помилка завантаження музики:", error));
  }, []);

  // Ключі для виводу у таблиці (без id)
  const columns = ["name", "title", "artist", "album", "right_holder"];
  const headers = ["Name", "Original title", "Artist", "Album", "Right Holder"]

  return (
    <div>
      <h2>Музична бібліотека</h2>
      <Table data={musics} headers={headers} columns={columns} onRowClick={setSelectedMusic} />
      {selectedMusic && <Modal data={selectedMusic} onClose={() => setSelectedMusic(null)} />}
    </div>
  );
}

export default MusicsPage;

