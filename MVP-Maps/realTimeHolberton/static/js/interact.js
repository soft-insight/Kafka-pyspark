let map = L.map('map').setView([4.710916742021916, -74.0765626060271], 6);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);

let marker = L.marker([4.710916742021916, -74.0765626060271]).addTo(map);

document.getElementById('select_location').addEventListener('change', function(e){
    let coords = e.target.value.split(",");
    map.flyTo(coords, 5)
})

