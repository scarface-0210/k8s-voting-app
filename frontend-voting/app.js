const API_URL = "/api";


async function vote(choice) {

    const message = document.getElementById("message");

    message.innerText = "Submitting vote...";

    try {

        const response = await fetch(`${API_URL}/vote`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                choice: choice
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Vote failed");
        }

        message.innerText =
            `Vote recorded for ${choice.toUpperCase()}!`;

    } catch (error) {

        message.innerText =
            `Error: ${error.message}`;

    }
}


async function loadResults() {

    const resultsElement =
        document.getElementById("results");

    resultsElement.innerText =
        "Loading results...";

    try {

        const response =
            await fetch(`${API_URL}/results`);

        const data =
            await response.json();

        resultsElement.innerHTML = `

            <div class="result">

                <h2>Results</h2>

                <p>🐱 Cats: ${data.cat}</p>

                <p>🐶 Dogs: ${data.dog}</p>

                <p>Total votes: ${data.total}</p>

            </div>

        `;

    } catch (error) {

        resultsElement.innerText =
            "Unable to retrieve results.";

    }
}
