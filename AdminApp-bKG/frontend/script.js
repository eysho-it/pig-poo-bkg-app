// --- Hilfsfunktionen ---

function showMessage(message, type) {
    const messageDiv = document.getElementById("message");
    messageDiv.textContent = message;
    messageDiv.classList.add(type);
    setTimeout(() => {
        messageDiv.textContent = "";
        messageDiv.classList.remove(type);
    }, 3000); // Nachricht nach 3 Sekunden ausblenden
}

function encryptData(data) {
    // Verschlüsseln Sie den API-Schlüssel vor der Speicherung
    return btoa(data);
}

function decryptData(data) {
    // Entschlüsseln Sie den API-Schlüssel bei der Verwendung
    return atob(data);
}

async function sendApiRequest(endpoint, method, data = null) {
    const apiKey = decryptData(localStorage.getItem("apiKey"));

    try {
        const response = await fetch(`/api/${endpoint}`, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "X-API-Key": apiKey
            },
            body: data ? JSON.stringify(data) : null
        });

        const responseData = await response.json();
        if (!response.ok) {
            throw new Error(responseData.error || "API-Fehler");
        }
        return responseData;
    } catch (error) {
        showMessage(error.message, "error");
        throw error; 
    }
}

// --- Login ---

const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const toggleFormButton = document.getElementById("toggle-form");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const username = loginForm.elements.username.value;
    const password = loginForm.elements.password.value;
    
    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `username=${username}&password=${password}`
        });

        if (response.redirected) {
            window.location.href = response.url;
        } else {
            const data = await response.json();
            showMessage(data.message, "error");
        }
    } catch (error) {
        showMessage("Fehler bei der Anmeldung", "error");
    }
});

// --- Registrierung ---

toggleFormButton.addEventListener("click", () => {
    loginForm.style.display = loginForm.style.display === "none" ? "block" : "none";
    registerForm.style.display = registerForm.style.display === "none" ? "block" : "none";
    toggleFormButton.textContent = loginForm.style.display === "none" ? "Zum Login wechseln" : "Zur Registrierung wechseln";
});

async function fetchData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
}

async function renderChart() {
    const data = await fetchData();
    const ctx = document.getElementById('userChart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Benutzeranzahl',
                data: data.counts,
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: true
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    renderChart();
});

document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const query = document.getElementById("search-query").value;
    window.location.href = `/search?query=${query}`;
});
