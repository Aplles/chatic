const darkMode = document.querySelector('.dark-mode');


            
const darkModeButton = document.querySelector('.dark-mode');
const body = document.body;

            
function setThemeFromLocalStorage() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        if (savedTheme === 'dark-mode-variables') {
            darkModeButton.querySelector('span:nth-child(1)').classList.remove('active');
            darkModeButton.querySelector('span:nth-child(2)').classList.add('active');
            
            
        } else {
            darkModeButton.querySelector('span:nth-child(2)').classList.remove('active');
            darkModeButton.querySelector('span:nth-child(1)').classList.add('active');
            
        }
    }
}

            
setThemeFromLocalStorage();

darkModeButton.addEventListener('click', () => {

    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');

    body.classList.toggle('dark-mode-variables');
    body.classList.toggle('light-mode-variables');

    // Сохраняем текущий режим в localStorage
    if (body.classList.contains('dark-mode-variables')) {
         localStorage.setItem('theme', 'dark-mode-variables');
    } else {
        localStorage.setItem('theme', 'light-mode-variables');
    }
});
