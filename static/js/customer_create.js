document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("customer-create-form");

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const errorElements = form.querySelectorAll('[id$="-error"], #customer-form-errors');

        errorElements.forEach((element) => {
            element.textContent = "";
            element.classList.add("hidden");
        });

        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton.disabled) return;

            submitButton.disabled = true;

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

            const contentType = response.headers.get("content-type");

            if (!contentType?.includes("application/json")) {
                throw new Error(`Respuesta inesperada del servidor: HTTP ${response.status}`);
            }

            const data = await response.json();

            if (response.ok) {
                console.log("Cliente creado:", data.message);

                const modal = FlowbiteInstances.getInstance(
                    "Modal",
                    "customer-create-modal"
                );

                if (modal) {
                    modal.hide();
                }

                form.reset();

                window.location.reload();
            }


            if (!response.ok) {
                for (const [field, messages] of Object.entries(data.errors ?? {})) {

                    const errorElement = field === "__all__"
                        ? document.getElementById("customer-form-errors")
                        : document.getElementById(`${field}-error`);

                    if (errorElement) {
                        errorElement.textContent = messages
                            .map(error => error.message)
                            .join(" ");

                        errorElement.classList.remove("hidden");
                    }
                }
            }



        } catch (error) {
            console.error("Error de conexión:", error);
            alert("No se ha podido completar la operación. Inténtalo de nuevo.");
        }finally {
            submitButton.disabled = false;
        }

    });

});