document.addEventListener('DOMContentLoaded', function() {
    // Dropdown Management
    const userDropdownToggle = document.getElementById('userDropdownToggle');
    const userDropdownMenu = document.getElementById('userDropdownMenu');

    userDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = userDropdownMenu.style.display === 'block';
        userDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        userDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    const tourDropdownToggle = document.getElementById('tourDropdownToggle');
    const tourDropdownMenu = document.getElementById('tourDropdownMenu');

    tourDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = tourDropdownMenu.style.display === 'block';
        tourDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        tourDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    const globalDropdownToggle = document.getElementById('globalDropdownToggle');
    const globalDropdownMenu = document.getElementById('globalDropdownMenu');

    globalDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = globalDropdownMenu.style.display === 'block';
        globalDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        globalDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    const teamDropdownToggle = document.getElementById('teamDropdownToggle');
    const teamDropdownMenu = document.getElementById('teamDropdownMenu');

    teamDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = teamDropdownMenu.style.display === 'block';
        teamDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        teamDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;';
    });

    // Filter Dropdown Toggle
    const filterBtn = document.getElementById('filter-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');

    filterBtn.addEventListener('click', function () {
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    // Date sorting logic clearly defined (no blinking)
    dropdownMenu.addEventListener('click', function (e) {
        e.preventDefault();
        const clickedItem = e.target;

        if (clickedItem.classList.contains('dropdown-item')) {
            const filterType = clickedItem.textContent.trim().toLowerCase();
            sortTableByDate(filterType);
            dropdownMenu.style.display = 'none';
        }
    });

    function sortTableByDate(order) {
        const tbody = document.querySelector('table tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        const parseDate = (str) => {
            const [day, month, year] = str.split('/');
            return new Date(`20${year}`, month - 1, day);
        };

        rows.sort((rowA, rowB) => {
            const dateA = parseDate(rowA.cells[5].textContent.trim());
            const dateB = parseDate(rowB.cells[5].textContent.trim());
            return order === 'latest' ? dateB - dateA : dateA - dateB;
        });

        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));
    }

    // Search with Green Highlight
    const searchBtn = document.getElementById('search-btn');
    searchBtn.addEventListener('click', function () {
        const input = document.getElementById('search').value.toLowerCase().trim();
        const rows = document.querySelectorAll('table tbody tr');
        let found = false;

        rows.forEach(row => {
            row.style.backgroundColor = '';
            row.style.boxShadow = '';
        });

        if (!input) {
            alert("Please enter a name to search.");
            return;
        }

        rows.forEach(row => {
            const userName = row.cells[1].textContent.toLowerCase();
            if (userName.includes(input)) {
                row.style.backgroundColor = '#e8f5e9';
                row.style.boxShadow = '0 0 10px green';
                row.scrollIntoView({ behavior: 'smooth', block: 'center' });
                found = true;
            }
        });

        if (!found) {
            alert("No user found with that name.");
        }
    });

    // Close dropdown when clicking outside
    window.onclick = function (event) {
        if (!event.target.matches('.dropdown-arrow, #filter-btn')) {
            const dropdowns = document.getElementsByClassName("dropdown-menu");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.style.display === 'block') {
                    openDropdown.style.display = 'none';
                }
            }
        }
    };
});
