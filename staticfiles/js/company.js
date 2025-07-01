document.addEventListener('DOMContentLoaded', function() {
    // User Management Dropdown
    const userDropdownToggle = document.getElementById('userDropdownToggle');
    const userDropdownMenu = document.getElementById('userDropdownMenu');

    userDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = userDropdownMenu.style.display === 'block';
        userDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        userDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    // Tour Management Dropdown
    const tourDropdownToggle = document.getElementById('tourDropdownToggle');
    const tourDropdownMenu = document.getElementById('tourDropdownMenu');

    tourDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = tourDropdownMenu.style.display === 'block';
        tourDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        tourDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    // Global Settings Dropdown
    const globalDropdownToggle = document.getElementById('globalDropdownToggle');
    const globalDropdownMenu = document.getElementById('globalDropdownMenu');

    globalDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = globalDropdownMenu.style.display === 'block';
        globalDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        globalDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    // Team Management Dropdown
    const teamDropdownToggle = document.getElementById('teamDropdownToggle');
    const teamDropdownMenu = document.getElementById('teamDropdownMenu');

    teamDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = teamDropdownMenu.style.display === 'block';
        teamDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        teamDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    // Search Functionality for Companies
    const searchInput = document.querySelector('.header input[type="search"]');

    searchInput.addEventListener('input', function() {
        let input = this.value.toLowerCase().trim();
        let table = document.querySelector('.table-container table tbody');
        let rows = table.getElementsByTagName('tr');
        let found = false;

        // Reset all rows' styles
        for (let row of rows) {
            row.style.boxShadow = 'none';
            row.style.backgroundColor = '';
        }

        if (input === "") {
            return;
        }

        for (let row of rows) {
            let userId = row.cells[0].textContent.toLowerCase();
            let username = row.cells[1].textContent.toLowerCase();

            if (userId.includes(input) || username.includes(input)) {
                row.style.boxShadow = "0 0 10px green";
                row.style.backgroundColor = "#e8f5e9";
                found = true;
                row.scrollIntoView({ behavior: 'smooth', block: 'center' });
                break;
            }
        }

        if (!found) {
            console.log("No such user with that name or ID found.");
        }
    });
});

// Additional Dropdown toggle

document.getElementById('userDropdownToggle').addEventListener('click', function() {
    document.getElementById('userDropdownMenu').classList.toggle('show');
});

window.onclick = function(event) {
    if (!event.target.matches('.dropdown-arrow')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}
