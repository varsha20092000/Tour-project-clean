// Clears the form inputs when "Add another" is clicked
document.querySelector('.add-another-btn').addEventListener('click', function() {
    document.querySelector('form').reset();
});
// Function to navigate to the previous page
function goBack() {
    window.history.back();
}
// Clear the form when the "Add another" button is clicked
document.getElementById('add-another-btn').addEventListener('click', function() {
    const form = document.getElementById('role-form');
    form.reset(); // Clears all input and textarea fields
});
