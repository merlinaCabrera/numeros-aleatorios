import express from "express"
import { pool } from "./mysql.js"
const app = express()
const port = 3000

app.get("/health-check", (req, res) => {
  res.send(`Server running on port ${port}!`)
})

app.get("/api/data", async (req, res) => {
  const [result] = await pool.query("SELECT * FROM generated_numbers")
  res.json(result[0])
})

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
})
