let access = null;
let username = null;

const $ = (q) => document.querySelector(q);
const BASE_URL = window.location.origin;  // lấy domain tự động

function setLoggedInUI(on) {
    // Hide login & signup when logged in
    $("#login-box").style.display = on ? "none" : "block";
    $("#signup-box").style.display = on ? "none" : "block";
    $("#loggedin").style.display = on ? "block" : "none";
    $("#predict").style.display = on ? "block" : "none";
    $("#history").style.display = on ? "block" : "none";
}

async function login() {
    const u = $("#username").value.trim();
    const p = $("#password").value.trim();
    const res = await fetch(`${BASE_URL}/api/token/`, {
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

    const res = await fetch(`${BASE_URL}/api/predict/`, {
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
    // Extract values
    const resultGoals = data.result && data.result.length ? data.result[0] : 0;
    const playerSelect = $("#player");
    const opponentSelect = $("#opponent");

    const playerName = playerSelect.options[playerSelect.selectedIndex].text;
    const opponentName = opponentSelect.options[opponentSelect.selectedIndex].text;

    // // Format output
    // $("#result").textContent = `${playerName} is predicted to score ${resultGoals} goal against ${opponentName}.`;

    // Format the message with a condition
    let message;
    if (resultGoals === 0) {
        message = `<b>${playerName}</b> is not expected to score against <b>${opponentName}</b>.`;
    } else if (resultGoals === 1) {
        message = `<b>${playerName}</b> is predicted to score <b>1</b> goal against <b>${opponentName}</b>.`;
    } else {
        message = `<b>${playerName}</b> is predicted to score <b>${resultGoals}</b> goals against <b>${opponentName}</b>.`;
    }

    // Show formatted output
    $("#result").innerHTML  = message;

    await loadHistory();
}

async function loadHistory() {
    const res = await fetch(`${BASE_URL}/api/history/`, {
        headers: { "Authorization": "Bearer " + access }
    });
    const data = await res.json();
    const tbody = $("#history-table tbody");
    tbody.innerHTML = "";

    (data || []).forEach(row => {
        const tr = document.createElement("tr");

        // Time
        const tdTime = document.createElement("td");
        tdTime.textContent = new Date(row.created_at).toLocaleString();
        tr.appendChild(tdTime);

        // Input
        const tdInput = document.createElement("td");
        const input = row.input_data || {};
        const playerName = playersMap[input.player_id] || `Player#${input.player_id}`;
        const opponentName = teamsMap[input.opponent_id] || `Team#${input.opponent_id}`;
        const homeName = teamsMap[input.home_team_id] || `Team#${input.home_team_id}`;
        tdInput.textContent = `${playerName} vs ${opponentName} (Home: ${homeName})`;
        tr.appendChild(tdInput);

        // Result (pretty)
        const tdResult = document.createElement("td");
        const goals = row.result && row.result.length ? row.result[0] : 0;
        tdResult.textContent = `${goals} goal${goals === 1 ? "" : "s"}`;
        tr.appendChild(tdResult);

        tbody.appendChild(tr);
    });
}


let playersMap = {};
let teamsMap = {};

async function loadDropdowns() {
    const res = await fetch(`${BASE_URL}/api/dropdown-data/`, {
        headers: { "Authorization": "Bearer " + access }
    });
    if (!res.ok) {
        alert("Failed to load dropdown data");
        return;
    }
    const data = await res.json();

    playersMap = {};
    teamsMap = {};

    const playerSelect = $("#player");
    playerSelect.innerHTML = "";
    data.players.forEach(p => {
        const option = document.createElement("option");
        option.value = p.id;
        option.textContent = p.name;
        playerSelect.appendChild(option);

        // store lookup
        playersMap[p.id] = p.name;
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

        // store lookup
        teamsMap[t.id] = t.name;
    });
}


document.addEventListener("DOMContentLoaded", () => {
    $("#btn-login").addEventListener("click", login);
    $("#btn-logout").addEventListener("click", logout);
    $("#btn-predict").addEventListener("click", predict);
});
