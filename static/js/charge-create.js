
    document.addEventListener("DOMContentLoaded", () => {
        const form = document.getElementById("charge-create-form");

        if (!form) return;

        const submitButton = document.getElementById("charge-submit-btn");
        const errorContainer = document.getElementById("charge-form-error");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            errorContainer.classList.add("hidden");
            errorContainer.textContent = "";

            submitButton.disabled = true;
            submitButton.textContent = "Guardando...";

            const formData = new FormData(form);

            const chargeData = {
                date: formData.get("date"),
                description: formData.get("description"),
                amount: formData.get("amount"),
                notes: formData.get("notes"),
            };

            try {
                const response = await fetch(form.dataset.apiUrl, {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    },
                    body: JSON.stringify(chargeData),
                });

                const result = await response.json();

                if (!response.ok) {
                    const messages = [];

                    for (const [field, errors] of Object.entries(result)) {
                        const details = Array.isArray(errors)
                            ? errors.join(", ")
                            : String(errors);

                        messages.push(`${field}: ${details}`);
                    }

                    throw new Error(
                        messages.join("\n") ||
                        "No se ha podido registrar el cargo."
                    );
                }

                if (response.status !== 201) {
                    throw new Error("Respuesta inesperada del servidor.");
                }

                window.location.reload();

            } catch (error) {
                errorContainer.textContent = error.message;
                errorContainer.classList.remove("hidden");

            } finally {
                submitButton.disabled = false;
                submitButton.textContent = "Guardar cargo.";
            }
        });
    });
