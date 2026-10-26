document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("season-create-form");
    if (!form) return;

    const submitButton = document.getElementById("season-create-submit");
    const confirmation = document.getElementById("season-change-confirmation");
    const confirmationMessage = document.getElementById("season-confirmation-message");
    const confirmButton = document.getElementById("season-confirm-change");
    const cancelButton = document.getElementById("season-cancel-change");
    const generalErrors = document.getElementById("season-create-errors");

    let expectedSeasonId = null;
    let isSubmitting = false;

    function clearErrors() {
        form.querySelectorAll('[id^="season-"][id$="-error"]').forEach((element) => {
            element.textContent = "";
            element.classList.add("hidden");
        });

        generalErrors.textContent = "";
        generalErrors.classList.add("hidden");
    }

    function showError(message) {
        generalErrors.textContent = message;
        generalErrors.classList.remove("hidden");
    }

    async function submitSeason(confirmed = false) {
        if (isSubmitting) return;

        isSubmitting = true;
        submitButton.disabled = true;
        confirmButton.disabled = true;
        clearErrors();

        try {
            const formData = new FormData(form);

            if (confirmed) {
                formData.set("confirm_change", "true");
                formData.set("expected_active_season_id", expectedSeasonId);
            }

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    Accept: "application/json",
                },
            });

            const contentType = response.headers.get("content-type") || "";

            if (!contentType.includes("application/json")) {
                throw new Error("Respuesta inesperada del servidor.");
            }

            const data = await response.json();

            if (response.ok) {
                window.location.reload();
                return;
            }

            if (response.status === 409 && data.requires_confirmation) {
                expectedSeasonId = data.season.id;

                const amount = Number(data.season.total_pending)
                    .toLocaleString("es-ES", {
                        style: "currency",
                        currency: "EUR",
                    });

                confirmationMessage.textContent =
                    `La temporada ${data.season.name} será desactivada. ` +
                    `Tiene ${data.season.pending_accounts_count} cuentas ` +
                    `con un saldo pendiente total de ${amount}. ` +
                    `¿Quieres continuar?`;

                confirmation.classList.remove("hidden");
                submitButton.classList.add("hidden");
                return;
            }

            if (response.status === 400 && data.errors) {
                for (const [field, errors] of Object.entries(data.errors)) {
                    const errorElement = field === "__all__"
                        ? generalErrors
                        : document.getElementById(`season-${field}-error`);

                    if (errorElement) {
                        errorElement.textContent = errors
                            .map((error) => error.message)
                            .join(" ");

                        errorElement.classList.remove("hidden");
                    }
                }
                return;
            }

            throw new Error("No se pudo crear la temporada.");

        } catch (error) {
            showError(error.message || "Error de conexión.");
        } finally {
            isSubmitting = false;
            submitButton.disabled = false;
            confirmButton.disabled = false;
        }
    }

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        confirmation.classList.add("hidden");
        submitButton.classList.remove("hidden");
        expectedSeasonId = null;
        submitSeason();
    });

    confirmButton.addEventListener("click", () => {
        if (expectedSeasonId === null) return;
        submitSeason(true);
    });

    cancelButton.addEventListener("click", () => {
        confirmation.classList.add("hidden");
        submitButton.classList.remove("hidden");
        expectedSeasonId = null;
    });
});