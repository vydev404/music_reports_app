// Файл: /src/pages/TasksPage.jsx
import { useState, useEffect } from "react";
import Table from "../components/Table";
import Modal from "../components/Modal";

function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/v1/tasks")
      .then((response) => response.json())
      .then((data) => setTasks(data.data))
      .catch((error) => console.error("Помилка завантаження завдань:", error));
  }, []);

  // Ключі для виводу у таблиці
  const columns = ["id", "name", "status", "created_at"];

  return (
    <div>
      <h2>Черга завдань</h2>
      <Table data={tasks} columns={columns} onRowClick={setSelectedTask} />
      {selectedTask && <Modal data={selectedTask} onClose={() => setSelectedTask(null)} />}
    </div>
  );
}

export default TasksPage;

