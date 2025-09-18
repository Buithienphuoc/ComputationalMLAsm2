// const BASE_URL = window.location.origin;

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

            const username = document.getElementById("signup-username").value;
            const email = document.getElementById("signup-email").value;
            const password = document.getElementById("signup-password").value;

            try {
                const res = await fetch(`${BASE_URL}/api/signup/`, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json", 
                        "X-CSRFToken": csrftoken  // Get CSRF Token
                            },
                    body: JSON.stringify({ username, email, password })
                });

                const data = await res.json();
                const msgEl = document.getElementById("signup-msg");

                if (res.status === 201) {
                    msgEl.innerText = "✅ Signup successful! You can now login.";
                    msgEl.style.color = "green";
                } else {
                    msgEl.innerText = "❌ Signup failed: " + JSON.stringify(data);
                    msgEl.style.color = "red";
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
