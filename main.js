// Main JavaScript for Dual-League Manager

document.addEventListener('DOMContentLoaded', function() {
    // Close alert messages
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required], select[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = '#e74c3c';
                } else {
                    input.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Por favor completa todos los campos requeridos');
            }
        });
    });
});

// API Functions
async function signPlayer(playerId) {
    try {
        const response = await fetch('/transfers/api/sign', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ player_id: playerId })
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ocurrió un error al fichar el jugador');
    }
}

async function getClubStats() {
    try {
        const response = await fetch('/stats/api/club-stats');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

async function getMyClub() {
    try {
        const response = await fetch('/clubs/api/my-club');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
