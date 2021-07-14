//
// map_location.js
// static
//
// Created by Javier Contreras el 13/03/2021
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// Universidad Politécnica de Madrid
// 


function initialize_map(map_id,center,src) {
  var vectorLayer = new ol.layer.Vector({
      source: new ol.source.Vector(),
      style: new ol.style.Style({
          image: new ol.style.Icon({
              anchor: [0.5, 0.5],
              anchorXUnits: "fraction",
              anchorYUnits: "fraction",
              src: src
          })
      })
  });
  markers.push(vectorLayer);
  marker = vectorLayer;
  var mapLat = center[0];
  var mapLng = center[1];
  var mapDefaultZoom = 8;
  map = new ol.Map({
      target: map_id,
      layers: [
          new ol.layer.Tile({
              source: new ol.source.OSM({
                  url: "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
              })
          }),
          vectorLayer
      ],
      view: new ol.View({
          center: ol.proj.fromLonLat([mapLng, mapLat]),
          zoom: mapDefaultZoom
      })
  });
}

function add_map_point(lat, lng, index_location) {
  var feature = 
      new ol.Feature({
          id: index_location, 
          geometry: new ol.geom.Point(ol.proj.transform([parseFloat(lng), parseFloat(lat)], 'EPSG:4326', 'EPSG:3857')),
      })
  feature.setId(index_location);
  marker.getSource().addFeature(feature);
}