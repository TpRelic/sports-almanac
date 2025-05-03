const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

const mobileMenu = () => {
    menu.classList.toggle('is-active')
    menuLinks.classList.toggle('active')
}

menu.addEventListener('click', mobileMenu);

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("changeTextButton").addEventListener("click", function() {
        // The new text you want to appear
        var newText = "Here is the new AI Insight text!";
        
        // Set the new text in the textarea
        document.getElementById("outputBox").value = newText;
    });
}); 

document.getElementById('playerSearchForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent page reload

    const player = document.getElementById('playerInput').value;

    fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player: player })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('result').innerHTML = data.output;
    })
    .catch(err => {
        console.error('Error:', err);
        document.getElementById('result').innerText = 'An error occurred.';
    });
});

