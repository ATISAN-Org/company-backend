
document.addEventListener('DOMContentLoaded', function () {

    const reportsLink = [...document.querySelectorAll('a')].find(link => link.textContent.includes("Investor Reports"));
    if (reportsLink) {
        reportsLink.classList.add('text-primary');
    }
    if (!sessionStorage.getItem('somiti_welcome_shown')) {
        const toast = document.createElement('div');
        toast.innerText = "👋 Welcome to the Somiti Admin Panel!";
        toast.style.position = "fixed";
        toast.style.bottom = "20px";
        toast.style.right = "20px";
        toast.style.backgroundColor = "#2c3e50";
        toast.style.color = "#fff";
        toast.style.padding = "12px 20px";
        toast.style.borderRadius = "6px";
        toast.style.zIndex = "9999";
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
        sessionStorage.setItem('somiti_welcome_shown', 'true');
    }
});
