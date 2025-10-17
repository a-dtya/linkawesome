// This function runs when the webpage is fully loaded.
window.addEventListener('DOMContentLoaded', () => {
    
    // The URL of our Flask API endpoint
    const API_URL = 'http://127.0.0.1:5000/api/data';

    // Use the fetch API to get data from our backend
    fetch(API_URL)
        .then(response => response.json()) // Convert the response to JSON
        .then(data => {
            // The 'data' variable now holds our profile information
            console.log(data); // Good for debugging
            updateProfile(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            // You could display an error message to the user here
        });
});

function updateProfile(data) {
    // Update the header information
    document.getElementById('profile-pic').src = data.profile_picture_url;
    document.getElementById('username').textContent = data.username;
    document.getElementById('bio').textContent = data.bio;

    // Get the container for our links
    const linksList = document.getElementById('links-list');
    
    // Clear any existing links (optional, but good practice)
    linksList.innerHTML = '';

    // Loop through the links from the data and create HTML elements
    data.links.forEach(link => {
        // Create the list item
        const li = document.createElement('li');
        
        // Create the anchor tag (the link)
        const a = document.createElement('a');
        a.href = link.url;
        a.textContent = link.title;
        a.target = '_blank'; // Open link in a new tab

        // Add the anchor tag inside the list item
        li.appendChild(a);

        // Add the list item to our list container
        linksList.appendChild(li);
    });
}