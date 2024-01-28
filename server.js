const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const port = 3000;

// Serve static files from the 'public' directory
app.use(express.static('public'));

// Open the database
let db = new sqlite3.Database('./new_testament.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log('Connected to the new_testament.db database.');
  }
});

// Endpoint to fetch greek_title entries from the Books table
app.get('/api/greek-titles', (req, res) => {
  const sql = "SELECT greek_title FROM Books WHERE greek_title IS NOT NULL AND greek_title != ''";
  
  db.all(sql, [], (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({
      message: 'Success',
      data: rows
    });
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});

// Close the database connection when the server is closed
process.on('SIGINT', () => {
  db.close((err) => {
    if (err) {
      return console.error(err.message);
    }
    console.log('Closed the database connection.');
    process.exit(0);
  });
});