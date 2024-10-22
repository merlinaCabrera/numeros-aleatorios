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
      <h1>números generados 🔒📛💻</h1>
      <div className="card">
        {data.map((item, index) => (
          <h4 key={index}>
            ✔️ {item.number} [ seed: {item.seed} ]
          </h4>
        ))}
        <h4>...</h4>
      </div>
    </>
  )
}

export default App
