
    document.addEventListener("DOMContentLoaded", () => {
        const form = document.getElementById("payment-create-form");

        if (!form) return;

        const submitButton = document.getElementById("payment-submit-btn");
        const errorContainer = document.getElementById("payment-form-error");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            errorContainer.classList.add("hidden");
            errorContainer.textContent = "";

            submitButton.disabled = true;
            submitButton.textContent = "Guardando...";

            const formData = new FormData(form);

            const paymentData = {
                date: formData.get("date"),
                description: formData.get("description"),
                amount: formData.get("amount"),
                payment_method: formData.get("payment_method"),
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
                    body: JSON.stringify(paymentData),
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
                        "No se ha podido registrar el pago."
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
                submitButton.textContent = "Guardar pago";
            }
        });
    });
