// This function runs when the page is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Fetch the Greek titles from the server
  fetch('/api/greek-titles')
    .then(response => response.json())
    .then(data => {
      console.log(data); // Add this line to log the data
      // Get the dropdown element
      const dropdown = document.getElementById('book-dropdown');

      // Add an option to the dropdown for each Greek title
      data.data.forEach(item => { // Note the change here
        const option = document.createElement('option');
        option.value = item.greek_title;
        option.textContent = item.greek_title;
        dropdown.appendChild(option);
      });
    })
    .catch(error => console.error('Error:', error));

  // Event listener for when a book is selected
  const bookDropdown = document.getElementById('book-dropdown');
  bookDropdown.addEventListener('change', function() {
    const selectedBook = this.value;
    updateChapterDropdown(selectedBook);
  });
});

// Function to update the chapter dropdown
function updateChapterDropdown(bookTitle) {
  fetch(`/api/chapters?book=${encodeURIComponent(bookTitle)}`)
    .then(response => response.json())
    .then(data => {
      const chapterDropdown = document.getElementById('chapter-dropdown');
      // Clear existing options
      chapterDropdown.innerHTML = '';
      // Assuming the API returns an object with a chapters field that is an array of chapter numbers
      for (let i = 1; i <= data.chapters; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `Chapter ${i}`;
        chapterDropdown.appendChild(option);
      }
    })
    .catch(error => console.error('Error fetching chapters:', error));
}