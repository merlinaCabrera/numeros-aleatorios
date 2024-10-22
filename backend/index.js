import express from "express"
import { pool } from "./mysql.js"
const app = express()
const port = 3000
app.use(express.json())

app.get("/health-check", (req, res) => {
  res.send(`Server running on port ${port}!`)
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

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
})
