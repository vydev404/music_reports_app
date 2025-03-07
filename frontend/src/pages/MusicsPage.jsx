// Файл: /src/pages/MusicsPage.jsx
import { useState, useEffect } from "react";
import Table from "../components/Table";
import Modal from "../components/Modal";

function MusicsPage() {
  const [musics, setMusics] = useState([]);
  const [selectedMusic, setSelectedMusic] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/v1/musics")
      .then((response) => response.json())
      .then((data) => setMusics(data.data))
      .catch((error) => console.error("Помилка завантаження музики:", error));
  }, []);

  // Ключі для виводу у таблиці (без id)
  const columns = ["name", "title", "artist", "album", "right_holder"];

  return (
    <div>
      <h2>Музична бібліотека</h2>
      <Table data={musics} columns={columns} onRowClick={setSelectedMusic} />
      {selectedMusic && <Modal data={selectedMusic} onClose={() => setSelectedMusic(null)} />}
    </div>
  );
}

export default MusicsPage;

