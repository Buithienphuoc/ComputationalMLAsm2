// signup.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signup-form");

    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const username = document.getElementById("signup-username").value.trim();
            const email = document.getElementById("signup-email").value.trim();
            const password = document.getElementById("signup-password").value.trim();
            const password2 = document.getElementById("signup-password2").value.trim();

            const msgEl = document.getElementById("signup-msg");

            if (password !== password2) {
                msgEl.innerText = "❌ Passwords do not match!";
                msgEl.style.color = "red";
                return;
            }

            try {
                const res = await fetch(`${BASE_URL}/api/signup/`, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json", 
                        "X-CSRFToken": csrftoken  
                    },
                    body: JSON.stringify({ username, email, password, password2 })
                });

                const data = await res.json();

                if (res.status === 201) {
                    msgEl.innerText = "Signup successful! You can now login.";
                    msgEl.style.color = "green";

                    // Switch back to Login tab
                    setTimeout(() => {
                        const loginTab = document.querySelector("#login-tab");
                        if (loginTab) loginTab.click();

                        // Ensure login UI is shown
                        if (typeof setLoggedInUI === "function") {
                            setLoggedInUI(false);
                        }
                    }, 1000);
                } else {
                    msgEl.style.color = "red";

                    // Try to extract a cleaner error message
                    let errorMsg = "Signup failed";
                    if (data) {
                        if (typeof data === "object") {
                            // Flatten first error value
                            const firstKey = Object.keys(data)[0];
                            if (firstKey && Array.isArray(data[firstKey]) && data[firstKey].length > 0) {
                                errorMsg = data[firstKey][0]; 
                            } else {
                                errorMsg = JSON.stringify(data);
                            }
                        } else {
                            errorMsg = data.toString();
                        }
                    }
                    msgEl.innerText = errorMsg;
                }
            } catch (err) {
                console.error("Signup error:", err);
                const msgEl = document.getElementById("signup-msg");
                msgEl.innerText = "⚠️ Network error. Please try again.";
                msgEl.style.color = "orange";
            }
        });
    }
});
