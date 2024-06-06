const searchInput = document.getElementById('searchInput');
const reservationTable = document.getElementById('reservationTable');
const rows = reservationTable.getElementsByTagName('tr');

searchInput.addEventListener('value', function() {
    const filter = searchInput.value.toUpperCase();
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;
        for (let j = 0; j < cells.length; j++) {
            const cellText = cells[j].textContent.toUpperCase();
            if (cellText.includes(filter)) {
                found = true;
                break;
            }
        }
        if (found) {
            rows[i].style.display = '';
        } else {
            rows[i].style.display = 'none';
        }
    }
});
