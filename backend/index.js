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
  const { figure_count, square_count, unique_position_value, temperature, seed, generated_number } =
    req.body
  const [rows] = await pool.query(
    "INSERT INTO generated_numbers (figure_count, square_count, unique_position_value, temperature, seed, generated_number) VALUES (?, ?, ?, ?, ?, ?)",
    [figure_count, square_count, unique_position_value, temperature, seed, generated_number]
  )
  res.send({
    id: rows.insertId,
    figure_count,
    square_count,
    unique_position_value,
    temperature,
    seed,
    generated_number,
  })
})

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
