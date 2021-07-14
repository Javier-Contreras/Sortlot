//
// solution_map.js
// static
//
// Created by Javier Contreras el 13/03/2021
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// Universidad Politécnica de Madrid
// 



function map_route(registration){
  var map_id = registration + '_map';
  var vehicle_index_for_mapping = 0;

  for (var i = 0; i< data.vehicles.length; i++){
    if (vehicles_registration_used.includes(data.vehicles[i].registration)){
      index_of_vehicle = vehicles_registration_used.indexOf(data.vehicles[i].registration);
      var map_div = document.getElementById(vehicles_registration_used[index_of_vehicle]+'_map')
      
      if (vehicles_registration_used[index_of_vehicle] === registration){
        vehicle_index_for_mapping = i;
        if (map_div.style.display === 'none')
          map_div.style.display='block';
      } else if (map_div.style.display === 'block')
        map_div.style.display = 'none';  
    }
  }

  if (!loaded[vehicle_index_for_mapping]){
    loaded[vehicle_index_for_mapping] = true;
    var start_end;
    var waypoints_list = [];
    for (var location_index_in_route = 0; location_index_in_route <solution.routes[vehicle_index_for_mapping].length-1; location_index_in_route++){
      if (location_index_in_route==0){
        start_end = [data.coordinates_depot[solution.routes[vehicle_index_for_mapping][location_index_in_route]][0], 
        data.coordinates_depot[solution.routes[vehicle_index_for_mapping][location_index_in_route]][1]];
        waypoints_list.push(start_end)
      }
      else 
        waypoints_list.push([data.coordinates_dst[solution.routes[vehicle_index_for_mapping][location_index_in_route]-1][0], 
          data.coordinates_dst[solution.routes[vehicle_index_for_mapping][location_index_in_route]-1][1]]);
    }

      var map = L.map(map_id).setView(start_end, 5);
      L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 12,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiamF2aWVyLWNvbnRyZXJhcyIsImEiOiJja3E1MmV5MGYxMzg2MnZsbmsyZ2ppdmN4In0.kuHgz0ZcZFbj_V0xV4MwHQ'
      }).addTo(map);
      waypoints_list.push(start_end)

      L.Routing.control({
        waypoints: waypoints_list,
        serviceUrl: 'http://127.0.0.1:5000/route/v1'
      }).addTo(map);
  }
} 


