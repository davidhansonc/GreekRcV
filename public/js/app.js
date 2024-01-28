const sqlite3 = require('sqlite3').verbose();

// Open the database
let db = new sqlite3.Database('../new_testament.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log('Connected to the new_testament.db database.');
  }
});

function executeSqlQuery(sql, params, callback) {
  db.all(sql, params, (err, rows) => {
    callback(err, rows);
  });
}

// Function to fetch Greek titles from the Books table
function getGreekTitles() {
  return new Promise((resolve, reject) => {
    // This is a placeholder for your database fetching logic
    executeSqlQuery("SELECT greek_title FROM Books WHERE greek_title IS NOT NULL AND greek_title != ''", [], (error, results) => {
      if (error) {
        reject(error);
      } else {
        resolve(results);
      }
    });
  });
}

// Function to populate the dropdown
function populateBookDropdown() {
  const dropdown = document.getElementById('book-dropdown');
  
  getGreekTitles().then(greekTitles => {
    greekTitles.forEach(title => {
      const option = document.createElement('option');
      option.value = title;
      option.textContent = title;
      dropdown.appendChild(option);
    });
  }).catch(error => {
    console.error('Error fetching Greek titles:', error);
  });
}

// Call the function to populate the dropdown when the page loads
document.addEventListener('DOMContentLoaded', populateBookDropdown);

// Remember to close the database connection when your app is closing
process.on('exit', () => {
  db.close((err) => {
    if (err) {
      console.error(err.message);
    } else {
      console.log('Closed the database connection.');
    }
  });
});

// Export the function if you need to use it in other modules
module.exports = {
  executeSqlQuery
};
