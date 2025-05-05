const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

const mobileMenu = () => {
    menu.classList.toggle('is-active')
    menuLinks.classList.toggle('active')
}

menu.addEventListener('click', mobileMenu);

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("changeTextButton").addEventListener("click", function () {

        const tables = document.querySelectorAll('table');
        let allTablesHTML = '';

        tables.forEach(table => {
            allTablesHTML += table.outerHTML;
        });

        //console.log("AI_Insight, sending: ", {table: allTablesHTML})
        var newText = "Loading...";
        document.getElementById("outputBox").value = newText;

        setTimeout(() => {
            fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ table: allTablesHTML }) 
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("outputBox").value = data.output;
            })
            .catch(err => {
                console.error('Error:', err);
                document.getElementById("outputBox").value = "An error occurred.";
            });
        }, 0); 
    });
}); 

document.addEventListener('DOMContentLoaded', function () {
    const playerForm = document.getElementById('playerSearchForm');
    
    if (playerForm) {
        playerForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const searchType = document.getElementById('searchType').value;
            const playerName = document.getElementById('playerInput').value;
            
            //console.log("Sending:", { player: playerName, type: searchType });

            fetch('/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player: playerName, type: searchType })
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
    }   
});

document.addEventListener('DOMContentLoaded', function () {
    const teamForm = document.getElementById('teamSearchForm');
  
    if (teamForm) {
      teamForm.addEventListener('submit', function (e) {
        e.preventDefault();
  
        const searchType = document.getElementById('searchType').value;
        const teamName = document.getElementById('teamInput').value;

        //console.log("Sending:", { team: teamName, type: searchType });
  
        fetch('/search-team', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ team: teamName, type: searchType })
        })
          .then(res => res.json())
          .then(data => {
            document.getElementById('teamResult').innerHTML = data.output;
          })
          .catch(err => {
            console.error('Error:', err);
            document.getElementById('result').innerText = 'An error occurred.';
          });
      });
    }
  });
  
