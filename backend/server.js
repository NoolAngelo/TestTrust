
const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Test Trust Backend Server');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});