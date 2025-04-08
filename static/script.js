document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".flash-message");

    messages.forEach((msg) => {
        setTimeout(() => {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 500);
        }, 4000);
    });
});
