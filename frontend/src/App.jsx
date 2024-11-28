import { useEffect, useState } from "react";
import "./App.css";
import io from "socket.io-client";

const apiHost = import.meta.env.VITE_API_HOST;

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Conectar a Socket.IO
    const socket = io("https://two024-g5-numeros-aleatorios-cloudfare.onrender.com", {
      transports: ["websocket"],
    });

    socket.on("newPost", () => {
      console.log("Datos actualizados desde el backend. Recargando...");
      fetchData();
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const fetchData = () => {
    fetch(`${apiHost}/api/data`)
      .then((response) => response.json())
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error al obtener la data:", error);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <div className="spinner"></div>;

  return (
    <>
      <h1 className="numbers-title">Números Generados 🔒📛💻</h1>
      <div className="card">
        {data.map((item, index) => (
          <h4 key={index} className="numbers-item">
            ✔️ {item.generated_number} [ seed: {item.seed}, figure_count: {item.figure_count},
            square_count: {item.square_count}, unique_position_value: {item.unique_position_value},
            temperature: {item.temperature}, created_at: {item.created_at.slice(0, 19)} ]
          </h4>
        ))}
        <div className="typing-dots"></div>
      </div>
    </>
  );
}

export default App;
