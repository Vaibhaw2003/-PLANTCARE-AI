async function loadChart() {
    const response = await fetch("/history");
    const data = await response.json();

    let counts = {
        "Healthy": 0,
        "Powdery Mildew": 0,
        "Rust": 0,
        "Leaf Spot": 0
    };

    data.forEach(item => {
        counts[item.disease]++;
    });

    const ctx = document.getElementById("diseaseChart").getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(counts),
            datasets: [{
                label: "Number of Predictions",
                data: Object.values(counts),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

loadChart();