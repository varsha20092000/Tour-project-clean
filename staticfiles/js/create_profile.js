
    const profilePhotoInput = document.getElementById('profile-photo');
    const avatar = document.querySelector('.avatar');

    profilePhotoInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                avatar.style.backgroundImage = `url(${e.target.result})`;
                avatar.style.backgroundSize = 'cover';
                avatar.style.backgroundPosition = 'center';
                avatar.textContent = ''; // Remove the placeholder text
            };
            reader.readAsDataURL(file);
        }
    });

