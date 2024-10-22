import express from "express"
import cors from "cors"
import { pool } from "./mysql.js"
import { PORT } from "./config.js"

const app = express()

app.use(express.json())
app.use(cors())

app.get("/health-check", (req, res) => {
  res.send(`Server running on port ${PORT}!`)
})

app.get("/api/data", async (req, res) => {
  const [result] = await pool.query("SELECT * FROM generated_numbers")
  res.json(result)
})

app.post("/api/data", async (req, res) => {
  const { number, seed } = req.body
  const [rows] = await pool.query("INSERT INTO generated_numbers(number, seed) VALUES (?, ?)", [
    number,
    seed,
  ])
  res.send({
    id: rows.insertId,
    number,
    seed,
  })
})

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
