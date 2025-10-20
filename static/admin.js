// This function runs when the admin page is fully loaded
window.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. Get references to our forms ---
    const profileForm = document.getElementById('profile-form');
    
    // --- 2. Load initial profile data ---
    loadProfileData();

    // --- 3. Add event listener for profile form submission ---
    profileForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Stop the form from causing a page reload
        
        // Get the data from the form fields
        const formData = new FormData(profileForm);
        const data = {
            username: formData.get('username'),
            bio: formData.get('bio'),
            profile_pic: formData.get('profile_pic')
        };

        // Send the data to the backend
        fetch('/api/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            console.log('Success:', result);
            alert('Profile updated!');
            // Optionally update the form fields again in case the server changed something
            loadProfileData();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating profile.');
        });
    });
});

/**
 * Fetches the current profile data and populates the form.
 */
function loadProfileData() {
    fetch('/api/profile')
        .then(response => response.json())
        .then(data => {
            // Fill the form with the data we got from the server
            document.getElementById('username').value = data.username;
            document.getElementById('bio').value = data.bio;
            document.getElementById('profile_pic').value = data.profile_picture_url;
        })
        .catch(error => console.error('Error loading profile data:', error));
}