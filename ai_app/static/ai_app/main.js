let access = null;
let username = null;

const $ = (q) => document.querySelector(q);

function setLoggedInUI(on) {
    $("#login-box").style.display = on ? "none" : "block";
    $("#loggedin").style.display = on ? "block" : "none";
    $("#predict").style.display = on ? "block" : "none";
    $("#history").style.display = on ? "block" : "none";
}

async function login() {
    const u = $("#username").value.trim();
    const p = $("#password").value.trim();
    const res = await fetch("/api/token/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: u, password: p})
    });
    const data = await res.json();
    if (data && data.access) {
        access = data.access;
        username = u;
        $("#whoami").textContent = "Logged in as: " + username;
        setLoggedInUI(true);
        await loadHistory();
    } else {
        alert("Login failed");
    }
}

async function logout() {
    access = null;
    username = null;
    setLoggedInUI(false);
    $("#whoami").textContent = "";
    $("#result").textContent = "";
    $("#input-data").value = "";
    $("#history-table tbody").innerHTML = "";
}

async function predict() {
    // let payload;
    // try {
    //     payload = JSON.parse($("#input-data").value || "[]");
    // } catch (e) {
    //     alert("Input phải là JSON hợp lệ.");
    //     return;
    // }
    let payload = $("#input-data").value || "";
    const res = await fetch("/api/predict/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access
        },
        body: JSON.stringify({ input_data: payload })
    });
    const data = await res.json();
    if (!res.ok) {
        alert("Predict error: " + (data.error || res.statusText));
        return;
    }
    $("#result").textContent = JSON.stringify(data, null, 2);
    await loadHistory();
}

async function loadHistory() {
    const res = await fetch("/api/history/", {
        headers: { "Authorization": "Bearer " + access }
    });
    const data = await res.json();
    const tbody = $("#history-table tbody");
    tbody.innerHTML = "";
    (data || []).forEach(row => {
        const tr = document.createElement("tr");
        const tdTime = document.createElement("td");
        tdTime.textContent = new Date(row.created_at).toLocaleString();
        const tdInput = document.createElement("td");
        tdInput.textContent = JSON.stringify(row.input_data);
        const tdResult = document.createElement("td");
        tdResult.textContent = JSON.stringify(row.result);
        tr.appendChild(tdTime);
        tr.appendChild(tdInput);
        tr.appendChild(tdResult);
        tbody.appendChild(tr);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    $("#btn-login").addEventListener("click", login);
    $("#btn-logout").addEventListener("click", logout);
    $("#btn-predict").addEventListener("click", predict);
});
