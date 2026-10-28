
document.querySelectorAll(".season-edit-form").forEach((editForm) => {

    editForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const submitButton = editForm.querySelector('[type="submit"]');
        const generalErrors = editForm.querySelector("[data-form-errors]");

        if (submitButton.disabled) return;

        submitButton.disabled = true;

        // Limpiar errores anteriores
        editForm.querySelectorAll("[data-field-error]").forEach((element) => {
            element.textContent = "";
            element.classList.add("hidden");
        });

        generalErrors.textContent = "";
        generalErrors.classList.add("hidden");

        try {
            const response = await fetch(editForm.action, {
                method: "POST",
                body: new FormData(editForm),
                headers: {
                    "Accept": "application/json",
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

            if (response.status === 400 && data.errors) {
                for (const [field, errors] of Object.entries(data.errors)) {

                    const errorElement = field === "__all__"
                        ? generalErrors
                        : Array.from(
                            editForm.querySelectorAll("[data-field-error]")
                        ).find(
                            (element) => element.dataset.fieldError === field
                        );

                    if (errorElement) {
                        errorElement.textContent = errors
                            .map((error) => error.message)
                            .join(" ");

                        errorElement.classList.remove("hidden");
                    }
                }
            } else {
                throw new Error("No se pudo actualizar la temporada.");
            }

        } catch (error) {
            generalErrors.textContent =
                error.message || "Error de conexión.";

            generalErrors.classList.remove("hidden");

        } finally {
            submitButton.disabled = false;
        }
    });
});
