// This function runs when the webpage is fully loaded.
window.addEventListener('DOMContentLoaded', () => {
    
    // The URL of our Flask API endpoint
    const API_URL = 'http://127.0.0.1:5000/api/data'; // <-- FIX 1: Point to the API route

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
    // FIX 2: Access data from the nested 'profile' object
    const profile = data.profile; 
    document.getElementById('profile-pic').src = profile.profile_picture_url;
    document.getElementById('username').textContent = profile.username;
    document.getElementById('bio').textContent = profile.bio;

    // Get the container for our links
    const linksList = document.getElementById('links-list');
    
    linksList.innerHTML = ''; // Clear any existing links

    // Loop through the links from the data
    data.links.forEach(link => { // This part was already correct
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = link.url;
        a.textContent = link.title;
        a.target = '_blank';
        li.appendChild(a);
        linksList.appendChild(li);
    });
}