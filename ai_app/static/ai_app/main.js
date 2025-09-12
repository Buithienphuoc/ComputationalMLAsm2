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
        await loadDropdowns();
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
    $("#history-table tbody").innerHTML = "";
    $("#player").innerHTML = "";
    $("#opponent").innerHTML = "";
    $("#home_team").innerHTML = "";
}

async function predict() {
    const playerId = $("#player").value;
    const opponentId = $("#opponent").value;
    const homeTeamId = $("#home_team").value;

    if (!playerId || !opponentId || !homeTeamId) {
        alert("Please select player, opponent, and home team.");
        return;
    }

    const payload = {
        player_id: playerId,
        opponent_id: opponentId,
        home_team_id: homeTeamId
    };

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

async function loadDropdowns() {
    const res = await fetch("/api/dropdown-data/", {
        headers: { "Authorization": "Bearer " + access }
    });
    if (!res.ok) {
        alert("Failed to load dropdown data");
        return;
    }
    const data = await res.json();

    const playerSelect = $("#player");
    playerSelect.innerHTML = "";
    data.players.forEach(p => {
        const option = document.createElement("option");
        option.value = p.id;
        option.textContent = p.name;
        playerSelect.appendChild(option);
    });

    const opponentSelect = $("#opponent");
    const homeSelect = $("#home_team");
    opponentSelect.innerHTML = "";
    homeSelect.innerHTML = "";
    data.teams.forEach(t => {
        const opt1 = document.createElement("option");
        opt1.value = t.id;
        opt1.textContent = t.name;
        opponentSelect.appendChild(opt1);

        const opt2 = document.createElement("option");
        opt2.value = t.id;
        opt2.textContent = t.name;
        homeSelect.appendChild(opt2);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    $("#btn-login").addEventListener("click", login);
    $("#btn-logout").addEventListener("click", logout);
    $("#btn-predict").addEventListener("click", predict);
});
