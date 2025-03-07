// Файл: /src/components/Table.jsx
function Table({ data, columns, headers, onRowClick }) {
  if (!data || data.length === 0) return <p>Дані відсутні</p>;

  return (
    <div className="flex-table">
      {/* Заголовок таблиці */}
      <div className="flex-row flex-header">
        <div className="flex-cell cell-s1">#</div> {/* Нумерація рядків */}
        {headers.map((col) => (
          <div className="flex-cell" key={col}>{col}</div>
        ))}
      </div>

      {/* Дані таблиці */}
      {data.map((item, index) => (
        <div key={index} className="flex-row" onClick={() => onRowClick(item)}>
          <div className="flex-cell cell-s1">{index + 1}</div> {/* Відображаємо номер рядка */}
          {columns.map((col) => (
            <div className={`flex-cell ${item[col] && item[col].length <= 5 ? "cell-s1" : ""}`}  key={col}>{item[col]}</div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default Table;
