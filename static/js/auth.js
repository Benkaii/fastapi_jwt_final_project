// Save JWT token
function saveToken(token) {
    localStorage.setItem("token", token);
}

// Get JWT token
function getToken() {
    return localStorage.getItem("token");
}

// Remove JWT token
function logout() {
    localStorage.removeItem("token");
    alert("Logged out.");
    window.location.href = "/login";
}