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
});