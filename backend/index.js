import express from "express";
import cors from "cors";
import { pool } from "./mysql.js";
import { PORT } from "./config.js";
import { Server } from "socket.io";
import http from "http";

const app = express()



app.use(express.json());
app.use(cors({
    origin: "https://front-2024-g5-numeros-aleatorios.onrender.com", // Permitir solicitudes del frontend
    methods: ["GET", "POST"],
}));

const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "https://front-2024-g5-numeros-aleatorios.onrender.com", // Permitir solicitudes del frontend
        methods: ["GET", "POST"],
    },
});

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

  io.emit('newPost');
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

io.on("connection", (socket) => {
  console.log("Cliente conectado:", socket.id);

  socket.on("disconnect", () => {
      console.log("Cliente desconectado:", socket.id);
  });
});
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
