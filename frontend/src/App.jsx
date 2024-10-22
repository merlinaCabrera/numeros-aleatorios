import { useEffect, useState } from "react"
import "./App.css"

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://localhost:3000/api/data")
      .then((response) => response.json())
      .then((data) => {
        setData(data)
        setLoading(false)
      })
      .catch((error) => {
        console.error("Error al obtener la data:", error)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="spinner"></div>

  return (
    <>
      <h1 className="numbers-title">números generados 🔒📛💻</h1>
      <div className="card">
        {data.map((item, index) => (
          <h4 key={index} className="numbers-item">
            ✔️ {item.number} [ seed: {item.seed} ]
          </h4>
        ))}
        <div className="typing-dots"></div>
      </div>
    </>
  )
}

export default App
