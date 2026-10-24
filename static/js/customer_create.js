document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("customer-create-form");

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

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
                    const errorElement = document.getElementById(`${field}-error`);

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
        }

    });

});