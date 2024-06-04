var map = L.map('map').setView([40.7691, -73.9814], 15); // Coordenadas del Trump International Hotel & Tower

    // Añadir el tile layer de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Añadir un marcador al mapa en la ubicación del hotel
    L.marker([40.7691, -73.9814]).addTo(map)
        .bindPopup('Trump International Hotel & Tower')
        .openPopup();