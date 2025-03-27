document.addEventListener('DOMContentLoaded', () => {
  /* ===== Liked Destinations (Existing Code) ===== */
  const dreamDestinationCards = document.getElementById('dream-destination-cards');

  if (!dreamDestinationCards) {
    console.error('Container not found: #dream-destination-cards');
  } else {
    // Retrieve liked destinations from localStorage (stored under "likedDestinations")
    const storedDestinations = localStorage.getItem('likedDestinations');
    let likedDestinations = {};
    if (storedDestinations) {
      try {
        likedDestinations = JSON.parse(storedDestinations);
        console.log('Liked Destinations Loaded:', likedDestinations);
      } catch (error) {
        console.error('Error parsing likedDestinations from localStorage:', error);
      }
    } else {
      console.log('No liked destinations found in localStorage.');
    }

    // Function to create a destination card element
    function createDestinationCard(destination) {
      const card = document.createElement('div');
      card.classList.add('card');
      card.dataset.name = destination.name; // Use a data attribute for easier lookup

      card.innerHTML = `
        <img src="${destination.image}" alt="${destination.name}">
        <h3>${destination.name}</h3>
        <p>${destination.description}</p>
        <p><strong>Location:</strong> ${destination.location}</p>
      `;
      return card;
    }

    // Function to display a destination card if it doesn't already exist
    function displayDestination(destination) {
      // Check if a card for this destination already exists
      const existingCard = document.querySelector(`#dream-destination-cards .card[data-name="${destination.name}"]`);
      if (existingCard) {
        console.warn(`Card for ${destination.name} already exists.`);
        return;
      }
      console.log(`Creating card for ${destination.name}`);
      const card = createDestinationCard(destination);
      dreamDestinationCards.appendChild(card);
    }

    // Loop through each liked destination and display it
    Object.values(likedDestinations).forEach(destination => {
      displayDestination(destination);
    });
  }

  /* ===== Liked Packages (New Code) ===== */
  const favoritePackagesContainer = document.getElementById('favorite-packages');

  if (!favoritePackagesContainer) {
    console.error('Container not found: #favorite-packages');
  } else {
    // Retrieve liked packages from localStorage (stored under "likedPackages")
    const storedPackages = localStorage.getItem('likedPackages');
    let likedPackages = {};
    if (storedPackages) {
      try {
        likedPackages = JSON.parse(storedPackages);
        console.log('Liked Packages Loaded:', likedPackages);
      } catch (error) {
        console.error('Error parsing likedPackages from localStorage:', error);
      }
    } else {
      console.log('No liked packages found in localStorage.');
    }

    // Function to create a package card element
    function createPackageCard(pkg) {
      const card = document.createElement('div');
      card.classList.add('card');
      card.dataset.id = pkg.id; // Use data-id for easier lookup

      card.innerHTML = `
        <img src="${pkg.image}" alt="${pkg.name}">
        <h3>${pkg.name}</h3>
        <p>${pkg.description}</p>
        <p><strong>Price:</strong> ${pkg.price}</p>
      `;
      return card;
    }

    // Function to display a package card if it doesn't already exist
    function displayPackage(pkg) {
      const existingCard = document.querySelector(`#favorite-packages .card[data-id="${pkg.id}"]`);
      if (existingCard) {
        console.warn(`Card for package ${pkg.name} already exists.`);
        return;
      }
      console.log(`Creating card for package ${pkg.name}`);
      const card = createPackageCard(pkg);
      favoritePackagesContainer.appendChild(card);
    }

    // Loop through each liked package and display it
    Object.values(likedPackages).forEach(pkg => {
      displayPackage(pkg);
    });
  }
});

/* ===== Duplicate createDestinationCard Function (if required) ===== */
function createDestinationCard(destination) {
  const card = document.createElement('div');
  card.classList.add('card');
  card.dataset.name = destination.name;
  
  card.innerHTML = `
    <img src="${destination.image}" alt="${destination.name}" onerror="this.onerror=null; this.src=placeholderImage;">
    <h3>${destination.name}</h3>
    <p>${destination.description}</p>
    <p><strong>Location:</strong> ${destination.location}</p>
  `;
  return card;
}
