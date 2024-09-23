// Initialize the map
function initMap() {
  const map = L.map('mapContainer').setView([19.0760, 72.8777], 5); // Starting point: Mumbai

  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Example ship route
  const routeCoordinates = [
    [19.0760, 72.8777],  // Mumbai
    [6.9271, 79.8612],   // Colombo
    [25.276987, 55.296249]  // Dubai
  ];

  // Draw the route on the map
  const route = L.polyline(routeCoordinates, { color: 'blue' }).addTo(map);

  // Zoom the map to the route
  map.fitBounds(route.getBounds());
}

// Load the map when the window loads
window.onload = initMap;
