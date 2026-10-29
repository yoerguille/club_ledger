
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("account-distribution-chart");
    const dataElement = document.getElementById("account-distribution-data");

    if (!canvas || !dataElement || typeof Chart === "undefined") return;

    const distribution = JSON.parse(dataElement.textContent);

    const labels = [
        "Pendientes de cobro",
        "Saldadas",
        "Cerradas",
        "Saldo a favor del cliente",
    ];

    const values = [
        distribution.pending,
        distribution.balance_0,
        distribution.closed,
        distribution.negative_balance,
    ];

    const chart = new Chart(canvas, {
        type: "doughnut",

        data: {
            labels: labels,
            datasets: [
                {
                    data: values,
                    backgroundColor: [
                        "#F59E0B", // Pendientes: naranja
                        "#3B82F6", // Saldadas: verde
                        "#10B981", // Cerradas: gris
                        "#EF4444", // Saldo a favor: azul
                    ],
                    borderWidth: 0,
                    hoverOffset: 8,
                },
            ],
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "72%",

            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        pointStyle: "circle",
                    },
                },

                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const total = values.reduce(
                                (sum, value) => sum + value,
                                0
                            );

                            const count = context.parsed;
                            const percentage = total > 0
                                ? ((count / total) * 100).toFixed(1)
                                : "0.0";

                            return `${context.label}: ${count} cuentas (${percentage}%)`;
                        },
                    },
                },
            },
        },
    });

    // Adaptar colores al modo claro/oscuro
    function updateChartTheme() {
        const isDark = document.documentElement.classList.contains("dark");

        chart.options.plugins.legend.labels.color = isDark
            ? "#D1D5DB"
            : "#4B5563";

        chart.update();
    }

    updateChartTheme();

    const observer = new MutationObserver(updateChartTheme);

    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
    });
});
