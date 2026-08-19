document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("delete-transaction-modal");
    const form = document.getElementById("delete-transaction-form");
    const description = document.getElementById(
        "delete-transaction-description"
    );
    const cancelButton = document.getElementById(
        "delete-transaction-cancel"
    );

    const deleteButtons = document.querySelectorAll(
        ".transaction-delete-btn"
    );


    function openModal(url, transactionDescription) {

        form.action = url;
        description.textContent = transactionDescription;

        modal.classList.remove("hidden");
        modal.classList.add("flex");

    }


    function closeModal() {

        modal.classList.add("hidden");
        modal.classList.remove("flex");

        form.removeAttribute("action");
        description.textContent = "";

    }


    deleteButtons.forEach((button) => {

        button.addEventListener("click", () => {

            openModal(
                button.dataset.deleteUrl,
                button.dataset.description
            );

        });

    });


    cancelButton.addEventListener("click", closeModal);


    modal.addEventListener("click", (event) => {

        if (event.target === modal) {
            closeModal();
        }

    });


    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {
            closeModal();
        }

    });

});