// script.js - External JavaScript for MivoTech India

(function () {
    // Wait for DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function () {
        // Check if theme toggle button exists (it will be loaded later)
        const checkThemeButton = setInterval(function () {
            const btn = document.getElementById('themeToggleBtn');
            if (btn) {
                clearInterval(checkThemeButton);
                initializeTheme(btn);
            }
        }, 100);
    });

    function initializeTheme(btn) {
        const themeSpan = document.getElementById('themeText');
        const body = document.body;

        // Check localStorage for saved theme
        const stored = localStorage.getItem('mivotechTheme');

        // Apply saved theme or default to light
        if (stored === 'dark') {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            if (themeSpan) {
                themeSpan.innerText = 'Light';
                btn.innerHTML = '<i class="fas fa-sun"></i><span id="themeText">Light</span>';
            }
        } else {
            body.classList.add('light-theme');
            body.classList.remove('dark-theme');
            if (themeSpan) {
                themeSpan.innerText = 'Dark';
                btn.innerHTML = '<i class="fas fa-moon"></i><span id="themeText">Dark</span>';
            }
        }

        // Theme toggle click handler
        btn.addEventListener('click', function () {
            if (body.classList.contains('light-theme')) {
                // Switch to dark theme
                body.classList.replace('light-theme', 'dark-theme');
                localStorage.setItem('mivotechTheme', 'dark');
                if (themeSpan) {
                    themeSpan.innerText = 'Light';
                    btn.innerHTML = '<i class="fas fa-sun"></i><span id="themeText">Light</span>';
                }
            } else {
                // Switch to light theme
                body.classList.replace('dark-theme', 'light-theme');
                localStorage.setItem('mivotechTheme', 'light');
                if (themeSpan) {
                    themeSpan.innerText = 'Dark';
                    btn.innerHTML = '<i class="fas fa-moon"></i><span id="themeText">Dark</span>';
                }
            }
        });
    }
    
})();

// ===== WELCOME POPUP (SHOW EVERY REFRESH) =====

window.addEventListener("load", function () {
    const popup = document.getElementById("welcomePopup");
    if (popup) {
        popup.style.display = "flex";
    }
});

function closeWelcome() {
    document.getElementById("welcomePopup").style.display = "none";
}
document.addEventListener('DOMContentLoaded', function() {
    // Get CSRF token from cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Set CSRF token in all forms
    const csrftoken = getCookie('csrftoken');
    const forms = document.getElementsByTagName('form');
    for (let form of forms) {
        const csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) {
            csrfInput.value = csrftoken;
        }
    }
});
