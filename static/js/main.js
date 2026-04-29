/* Dual-League Manager – JavaScript principal */

// Mostrar/ocultar campo de posición según rol seleccionado
document.addEventListener('DOMContentLoaded', function () {
    var roleSelect = document.getElementById('role');
    var positionGroup = document.getElementById('position-group');

    if (roleSelect && positionGroup) {
        function togglePosition() {
            positionGroup.style.display = roleSelect.value === 'player' ? 'block' : 'none';
        }
        togglePosition();
        roleSelect.addEventListener('change', togglePosition);
    }
});
