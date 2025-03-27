// Example credentials for demonstration purposes
const registeredUsername = "user123";
const registeredPassword = "password123";

// Function to check login credentials
function checkLogin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (username === registeredUsername && password === registeredPassword) {
    // Successful login
    alert("Login successful!");
  } else {
    // Error message for incorrect credentials
    alert("Error: Incorrect username or password. Please try again.");
  }
}

// Event listener for the login button
document.getElementById("loginButton").addEventListener("click", checkLogin);
