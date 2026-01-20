// ----------------------------
// CREATE MAP (basic example)
// ----------------------------
const map = L.map("map").setView([37.8, -96], 4);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors"
}).addTo(map);

// ----------------------------
// COLOR FUNCTION (ONLY 2 COLORS)
// ----------------------------
function getColor(cluster) {
  return cluster === 1
    ? "#de2d26"   // High vulnerability
    : "#9ecae1";  // Baseline
}

// ----------------------------
// LOAD CLUSTERS CSV
// ----------------------------
fetch("/static/data/county_clusters.csv")
  .then(response => response.text())
  .then(csvText => {
    const clusterData = Papa.parse(csvText, {
      header: true,
      dynamicTyping: true
    }).data;

    // Build lookup: fips → row
    const clusterLookup = {};
    clusterData.forEach(row => {
      if (row.fips) {
        clusterLookup[row.fips] = row;
      }
    });

    loadCounties(clusterLookup);
  });

// ----------------------------
// LOAD GEOJSON & STYLE
// ----------------------------
function loadCounties(clusterLookup) {
  fetch("/static/us_counties.geojson")
    .then(response => response.json())
    .then(countyGeoJson => {

      L.geoJson(countyGeoJson, {
        style: feature => {
          const county = clusterLookup[feature.id];

          return {
            fillColor: county ? getColor(county.Cluster) : "#ccc",
            weight: 0.5,
            color: "#555",
            fillOpacity: 0.8
          };
        },
        onEachFeature: (feature, layer) => {
          const county = clusterLookup[feature.id];

          if (county) {
            layer.bindTooltip(`
              <strong>${county.County}, ${county.State}</strong><br>
              ${county.risk_label}<br>
              ${county.Cluster === 1
                ? "High minority & low food access"
                : "Typical food access & demographics"}
            `);
          }
        }
      }).addTo(map);

    });
}
