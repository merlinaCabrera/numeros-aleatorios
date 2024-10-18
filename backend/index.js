const express = require("express")
const app = express()
const port = 3000

app.get("/", (req, res) => {
  res.send(`Server running on port ${port}!`)
})

app.listen(port, () => {
  console.log(`Server running on port ${port}`)
})
