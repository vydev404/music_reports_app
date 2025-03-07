// Файл: /src/components/Modal.jsx
import styles from "../styles/modal.module.css";

function Modal({ data, onClose }) {
  return (
    <div className={styles.overlay}>
      <div className={styles.modal}>
        <h3>{data.name || "Деталі"}</h3> {/* Відображаємо назву файлу */}
        {Object.entries(data).map(([key, value]) => (
          <p key={key}>
            <strong>{key}:</strong> {value}
          </p>
        ))}
        <button onClick={onClose}>Закрити</button>
      </div>
    </div>
  );
}

export default Modal;
