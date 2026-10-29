
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("monthly-transactions-chart");
    const dataElement = document.getElementById("monthly-chart-data");

    if (!canvas || !dataElement || typeof Chart === "undefined") return;

    const monthlyData = JSON.parse(dataElement.textContent);

    // Formatear importes en euros
    const euroFormatter = new Intl.NumberFormat("es-ES", {
        style: "currency",
        currency: "EUR",
        maximumFractionDigits: 2,
    });

    // Convertir 2026-09 en "sept 2026"
    const labels = monthlyData.map((item) => {
        const [year, month] = item.month.split("-").map(Number);

        return new Intl.DateTimeFormat("es-ES", {
            month: "short",
            year: "numeric",
        }).format(new Date(year, month - 1, 1));
    });

    const chart = new Chart(canvas, {
        type: "bar",

        data: {
            labels: labels,

            datasets: [
                {
                    label: "Cargos",
                    data: monthlyData.map((item) => item.charges),
                    backgroundColor: "#3B82F6",
                    borderRadius: 5,
                },
                {
                    label: "Pagos",
                    data: monthlyData.map((item) => item.payments),
                    backgroundColor: "#10B981",
                    borderRadius: 5,
                },
            ],
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            interaction: {
                mode: "index",
                intersect: false,
            },

            plugins: {
                legend: {
                    position: "bottom",
                },

                tooltip: {
                    callbacks: {
                        label: (context) =>
                            `${context.dataset.label}: ${euroFormatter.format(context.parsed.y)}`
                    },
                },
            },

            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => euroFormatter.format(value),
                    },
                },
            },
        },
    });

    // Adaptar los textos del gráfico al tema
    function updateChartTheme() {
        const isDark = document.documentElement.classList.contains("dark");

        const textColor = isDark ? "#D1D5DB" : "#4B5563";
        const gridColor = isDark
            ? "rgba(255,255,255,0.08)"
            : "rgba(0,0,0,0.06)";

        chart.options.plugins.legend.labels.color = textColor;
        chart.options.scales.x.ticks.color = textColor;
        chart.options.scales.y.ticks.color = textColor;
        chart.options.scales.y.grid.color = gridColor;
        chart.options.scales.x.grid.display = false;

        chart.update();
    }

    updateChartTheme();

    // Detectar cambios del modo claro/oscuro
    const observer = new MutationObserver(updateChartTheme);

    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
    });
});
