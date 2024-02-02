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

// Endpoint to fetch the number of chapters for a given book based on its Greek title
app.get('/api/chapters', (req, res) => {
  const bookTitle = req.query.book;
  if (!bookTitle) {
    res.status(400).json({ error: "Missing book title in query parameters." });
    return;
  }
  
  const sql = "SELECT chapter_count FROM Books WHERE greek_title = ?";
  
  db.get(sql, [bookTitle], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    if (row) {
      res.json({
        message: 'Success',
        chapters: row.chapter_count
      });
    } else {
      res.status(404).json({ error: "Book not found." });
    }
  });
});

// Endpoint to fetch the number of verses for a given book and chapter
app.get('/api/verses', (req, res) => {
  const bookName = req.query.book;
  const chapterNumber = req.query.chapter;
  if (!bookName || !chapterNumber) {
    res.status(400).json({ error: "Missing book name or chapter number in query parameters." });
    return;
  }
  
  const sql = "SELECT COUNT(verse_number) AS verse_count FROM Verses WHERE book_name = ? AND chapter_number = ?";
  
  db.get(sql, [bookName, chapterNumber], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    if (row) {
      res.json({
        message: 'Success',
        verses: row.verse_count
      });
    } else {
      res.status(404).json({ error: "No verses found for the specified book and chapter." });
    }
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