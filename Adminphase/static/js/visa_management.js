// Search Functionality
document.querySelector('#search-input').addEventListener('input', function () {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
});

// Placeholder for Filter Button
document.querySelector('#filter-btn').addEventListener('click', function () {
    alert('Filter functionality is not implemented yet.');
});
document.addEventListener('DOMContentLoaded', function() {
    // User Management Dropdown
    const userDropdownToggle = document.getElementById('userDropdownToggle');
    const userDropdownMenu = document.getElementById('userDropdownMenu');
  
    userDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = userDropdownMenu.style.display === 'block';
        userDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        userDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;'; // Start with ▲ and switch to ▼
    });
  
    // Tour Management Dropdown
    const tourDropdownToggle = document.getElementById('tourDropdownToggle');
    const tourDropdownMenu = document.getElementById('tourDropdownMenu');
  
    tourDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = tourDropdownMenu.style.display === 'block';
        tourDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        tourDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;'; // Start with ▲ and switch to ▼
    });
  
    // Global Settings Dropdown
    const globalDropdownToggle = document.getElementById('globalDropdownToggle');
    const globalDropdownMenu = document.getElementById('globalDropdownMenu');
  
    globalDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = globalDropdownMenu.style.display === 'block';
        globalDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        globalDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;'; // Start with ▲ and switch to ▼
    });
  
    // Team Management Dropdown
    const teamDropdownToggle = document.getElementById('teamDropdownToggle');
    const teamDropdownMenu = document.getElementById('teamDropdownMenu');
  
    teamDropdownToggle.addEventListener('click', function() {
        const isDropdownVisible = teamDropdownMenu.style.display === 'block';
        teamDropdownMenu.style.display = isDropdownVisible ? 'none' : 'block';
        teamDropdownToggle.innerHTML = isDropdownVisible ? '&#9650;' : '&#9660;'; // Start with ▲ and switch to ▼
    });
  });
  document.getElementById('userDropdownToggle').addEventListener('click', function() {
    document.getElementById('userDropdownMenu').classList.toggle('show');
  });
  
  window.onclick = function(event) {
    if (!event.target.matches('.dropdown-arrow')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
  }