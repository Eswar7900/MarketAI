// ---------------- CAMPAIGN ----------------
function generateCampaign() {
    const product = document.getElementById("product").value;

    if (!product) {
        alert("Please enter a product name");
        return;
    }

    document.getElementById("result").innerText = "Generating campaign...";

    fetch("/generate_campaign", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ product: product })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.result;
    })
    .catch(error => {
        document.getElementById("result").innerText = "Error generating campaign.";
        console.error(error);
    });
}


// ---------------- SALES ----------------
function generateSales() {
    const product = document.getElementById("salesProduct").value;

    if (!product) {
        alert("Please enter a product name");
        return;
    }

    document.getElementById("salesResult").innerText = "Generating sales pitch...";

    fetch("/generate_sales", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ product: product })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("salesResult").innerText = data.result;
    })
    .catch(error => {
        document.getElementById("salesResult").innerText = "Error generating sales pitch.";
        console.error(error);
    });
}


// ---------------- LEAD SCORING ----------------
function scoreLead() {
    const name = document.getElementById("leadName").value;

    if (!name) {
        alert("Please enter a lead name");
        return;
    }

    document.getElementById("leadResult").innerText = "Calculating lead score...";

    fetch("/score_lead", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("leadResult").innerText = data.result;
    })
    .catch(error => {
        document.getElementById("leadResult").innerText = "Error scoring lead.";
        console.error(error);
    });
}
