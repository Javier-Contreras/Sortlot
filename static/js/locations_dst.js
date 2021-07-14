//
// locations_dst.js
// static
//
// Created by Javier Contreras el 13/03/2021
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// Universidad Politécnica de Madrid
// 

var markers=[]
var marker = null;
var columns = ['name', 'address', 'capacity', "deliver_to", "from_time", "to_time", "use"];
var province_selected = "Alava";




var provinces_dic = { 
  "Alava": [ 42.909673, -2.812 ], 
  "Albacete": [ 38.810584, -1.949169 ], 
  "Alicante": [ 38.470773, -0.58679 ], 
  "Almeria": [ 37.123594, -2.281178 ], 
  "Asturias": [ 43.365517, -5.941384 ], 
  "Avila": [ 40.588601, -4.846529 ], 
  "Badajoz": [ 38.622888, -6.285155 ], 
  "Barcelona": [ 41.616675, 2.023662 ], 
  "Burgos": [ 42.32603, -3.666448 ], 
  "Caceres": [ 39.783956, -6.206693 ],
  "Cadiz": [ 36.47248, -5.80728 ], 
  "Cantabria": [ 43.280797, -3.953059 ], 
  "Castellon": [ 40.183362, -0.066911 ], 
  "Ciudad_Real": [ 38.927025, -3.782109 ],
  "Cordoba": [ 37.953852, -4.742714 ],
  "Coruña": [ 43.024099, -8.562117 ], 
  "Cuenca": [ 39.899388, -2.151187 ], 
  "Gipuzkoa": [ 43.186318, -2.1864 ], 
  "Girona": [ 42.111534, 2.817163 ], 
  "Granada": [ 37.182491, -3.520719 ], 
  "Guadalajara": [ 40.812681, -2.575393 ],
  "Huelva": [ 37.572965, -6.867033 ],
  "Huesca": [ 42.212146, -0.07079 ], 
  "Jaen": [ 37.969375, -3.378378 ], 
  "Rioja": [ 42.297716, -2.472572 ],
  "Leon": [ 42.595782, -5.720123 ], 
  "Lerida": [ 41.965717, 1.138506 ],
  "Lugo": [ 43.006177, -7.473601 ],
  "Madrid": [ 40.410673, -3.706576 ], 
  "Malaga": [ 36.730729, -4.653259 ], 
  "Murcia": [ 37.94781, -1.356492 ], 
  "Navarra": [ 42.751425, -1.662552 ], 
  "Ourense": [ 42.180225, -7.585861 ],
  "Palencia": [ 42.383889, -4.570723 ],
  "Pontevedra": [ 42.337872, -8.533218 ],
  "Salamanca": [ 40.850514, -6.101343 ],
  "Segovia": [ 41.172298, -4.116957 ],
  "Sevilla": [ 37.402606, -5.682544 ],
  "Soria": [ 41.651573, -2.539412 ],
  "Tarragona": [ 41.134362, 0.916797 ],
  "Teruel": [ 40.682727, -0.844679 ], 
  "Toledo": [ 39.842743, -4.108004 ], 
  "Valencia": [ 39.320635, -0.74428 ], 
  "Valladolid": [ 41.619489, -4.82218 ],
  "Vizcaya": [ 43.256776, -2.868784 ], 
  "Zamora": [ 41.823282, -5.961302 ],
  "Zaragoza": [ 41.669114, -0.852152 ] 
};

window.addEventListener('DOMContentLoaded', (event) => {

  load_json();
  var i = 0;
  for (const [province, coord] of Object.entries(provinces_dic)) {
    var option = document.createElement("option");
    option.value = province;
    if (province === "Ciudad_Real"){
        option.innerHTML = "Ciudad Real";

    } else if (province === "Coruña"){
        option.innerHTML = "A Coruña";

    } else if (province === "Rioja"){
        option.innerHTML = "La Rioja";

    } else {
      option.innerHTML = province;
    }
    callback = 'get_data_by_province(\"'+province+'\")'
    option.setAttribute("value",province);
    option.setAttribute("onClick",callback);
    document.getElementById("provinces").appendChild(option);
    i++;
  }
get_data_by_province(province_selected)

});


function generate_table(province){

  //var i = provinces.indexOf(province)
  var province_element = document.createElement("DIV");
  province_element.id = province + "-id";
  province_element.innerHTML = "<h3>" + province_selected + "</h3>";

  var map = document.createElement("DIV");

  map.style.width = "400px";
  map.style.height = "300px";
  map.style.marginRight ="15px";
  map.style.marginTop ="15px";
  map.style.marginBottom ="40px";

  map.id = "map-" + province;

  var tr = document.createElement("tr");
  tr.id = "tr-"+province

  var td_province = document.createElement("td");
  td_province.id = "td_province-"+province;

  var td_map = document.createElement("td");
  td_map.id = "td_map-"+province

  var td_table = document.createElement("td");
  td_table.id = "td_table-"+province

  var table = document.createElement("TABLE");
  table.className = "table";
  table.id="table-"+province;

  var thead = document.createElement("THEAD");
  thead.className = "thead-dark";
  thead.innerHTML = "<tr> <th>ID</th> <th>Name</th> <th>Address</th> <th>Demand</th> <th>Deliver To [ID]</th> <th>From Time</th> <th>To Time</th> <th>Use</th> </tr>";
  thead.id="thead-"+province;
  
  var tbody = document.createElement("tbody");
  //tbody.innerHTML = "<tr> <th>#</th> <th>Name</th> <th>Address</th> <th>Capacity</th> <th>Deliver To</th> <th>From Time</th> <th>To Time</th> <th>Use</th> </tr>";
  tbody.class = "editable-"+province;
  tbody.id = "editable-"+province;

  var search_bar = document.createElement("input");
  search_bar.id = "search_bar-"+province;
  search_bar.type = "text";
  search_bar.style = "margin-right: 10px";
  search_bar.placeholder = "Search...";

  document.getElementById("tables").appendChild(tr);
  document.getElementById("tr-"+province).appendChild(td_province);
  document.getElementById("tr-"+province).appendChild(td_map);
  document.getElementById("tr-"+province).appendChild(td_table);

  document.getElementById("td_province-"+province).appendChild(province_element);
  document.getElementById("td_map-"+province).appendChild(map);
  document.getElementById("td_table-"+province).appendChild(table);
  document.getElementById("table-"+province).appendChild(thead);
  document.getElementById("table-"+province).appendChild(tbody);

  var src_point = "{{ url_for('static', filename='images/RedDot.svg') }}";

  map = initialize_map("map-" + province, provinces_dic[province],src_point);
  for (var j = 0; j<data.length; j++){
    data[j].use = (data[j].use === 'true') || (data[j].use == true);

    if(data[j].province === province){
      var lat = data[j].coordinates[0];
      var lng = data[j].coordinates[1];
      if (data[j].use)
        var src_point = "{{ url_for('static', filename='images/Blue_Marker.png') }}"
      else
        var src_point = "{{ url_for('static', filename='images/RedDot.svg') }}";
      add_map_point(lat, lng, j)
    }
  }
}

function load_json(){
  try {
    document.getElementById('json_file').onchange = function() {
      var files = document.getElementById('json_file').files;

      if (files.length <= 0) {
        return false;
      }

      var fr = new FileReader();

      fr.onload = function(e) { 
        var result = JSON.parse(e.target.result);
        console.log(result);
        data = result;
        //poblate_table(data, provinces);
        remove_table();

        generate_table('Alava');
        poblate_table_one_province(data,'Alava',marker);

        var formatted = JSON.stringify(result, null, 2);
        var file = document.getElementById('json')
        file.value = JSON.stringify(formatted)
        document.getElementById("name").value = document.getElementById("name_of_shippment").value    
        json_loaded = true;  
      }

      fr.readAsText(files.item(0));
    };
  } catch (error) {
    console.error(error);
  }
}

function make_table_editable(province, provinces,){
    var prev_value
    var new_value
    $('#editable-' + province).editableTableWidget();

    $('#editable-' + province + ' td.uneditable').click(function(e) {
      return false;
    });
    //    
    $("#editable-"+ province).on('change', function(e, value) {
      var clickedCell= $(e.target).closest("td");
      var clickedRow= $(e.target).closest("tr");
      
        //if (clickedCell.indexOx() == 0 || clickedCell.index() == 1){

        //  return;
       // }
      index_of_data = parseInt(clickedRow.text().split(" ")[0]);
      field = columns[clickedCell.index()-1]
      if (field == "use"){
        var province = data[index_of_data]['province'];
        if (data[index_of_data][field]){
            var src_point = "static/images/RedDot.svg";
            data[index_of_data][field] = false
        } else {
          var src_point = "static/images/Blue_Marker.png"
          data[index_of_data][field] = true
        }
        var feature = marker.getSource().getFeatureById(index_of_data)
        feature.setStyle(new ol.style.Style({ image: new ol.style.Icon({
                  anchor: [0.5, 0.5],
                  anchorXUnits: "fraction",
                  anchorYUnits: "fraction",
                  src: src_point
              }) }))          
      } else 
          data[index_of_data][field] = clickedCell.children("input").val();
      var file = document.getElementById('json')
      file.value = data
      console.log(data)
    });
      
    $("#search_bar").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#td_table-"+province+" tbody tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
     
    });

    $(".edit_field").click(function(e) {

      var clickedCell= $(e.target).closest("td");
      var clickedRow= $(e.target).closest("tr");
      if (clickedCell.index() == 0 || clickedCell.index() == 6)
        return false;
      prev_value = clickedCell.text();

    });

    $(".input_cell").click(function(e) {
        $( this ).children("input").focus();
    });

  }



  
function remove_table(){
  for (const [province, coord] of Object.entries(provinces_dic)) {
    try{
      document.getElementById("tr-"+province).remove();

    } catch (error){
      continue;
    }
  }
}

//map = init_map();
function poblate_table_one_province(data_province, province,marker){
  var html = '';

  make_table_editable(province, provinces);
  
  for(var j = 0; j < data_province.length; j++){
    if (data_province[j].province === province){
      var d = Math.random();

      /*if (d < 0.3){
        data_province[j].use = true;
        data[data_province[j].id].use = true;

      } else {
        data_province[j].use = false;
        data[data_province[j].id].use = false;

      }*/
      data_province[j].use = (data_province[j].use === 'true') || (data_province[j].use == true);
      var use = data_province[j].use ? "checked" : "";
      
      html += '<tr><td readonly="readonly" class="uneditable">' + data_province[j].id + 
        '</td> <td readonly="readonly" class="uneditable">' + data_province[j].name +
        '</td> <td readonly="readonly" class="uneditable">' + data_province[j].address +
        '</td><td class="input_cell" ><input type="number" min="0" value="'+ data_province[j].capacity + 
        '" ></td><td class="input_cell" ><input type="number" min="0" value="'+ data_province[j].deliver_to +
        '" ></td><td class="input_cell"><input  type="time" value="'+ data_province[j].from_time + 
        '"></td><td class="input_cell"><input type="time" value="'+ data_province[j].to_time + 
        '" ></td><td class="input_cell"><input type="checkbox" ' + use + '></td></tr>';
      var province = data_province[j]['province'];

        
      if (data_province[j]['use'])
        var src_point = "static/images/Blue_Marker.png"
      else 
        var src_point = "static/images/RedDot.svg";
      
  
      var feature = marker.getSource().getFeatureById(data_province[j].id)
          feature.setStyle(new ol.style.Style({ image: new ol.style.Icon({
                  anchor: [0.5, 0.5],
                  anchorXUnits: "fraction",
                  anchorYUnits: "fraction",
                  src: src_point
              }) }))
        
    } 
  }
  $("#editable-"+province).append(html);
  return data_province
}     
        
    


function get_data_by_province(province = ""){
  if (province === ""){
    province = document.getElementById("provinces").value
  }
  if (province === "Ciudad_Real"){
        province_selected = "Ciudad Real";

    } else if (province === "Coruña"){
        province_selected = "A Coruña";

    } else if (province === "Rioja"){
        province_selected = "La Rioja";

    } else {
      province_selected = province;
    }
    if (!json_loaded){
      $.ajax({
          type: "GET",
          url: "http://127.0.0.1:8080/get_data/"+province,
          //contentType: "application/json",
          //dataType: "json",                        
          success: function (response) {
              remove_table();
              generate_table(province);
              poblate_table_one_province(JSON.parse(response),province,marker);
          },
          error: function (response){

              console.log("Error while fetching data");
          }
      });
    }else {
      remove_table();
      generate_table(province);
      poblate_table_one_province(data,province,marker);
    }
}

function format(json_file=null){
  if (json_file != null){
    var file = document.getElementById('json')
    file.value = JSON.stringify(json_file)
    console.log(json_file)
    document.getElementById("name").value = document.getElementById("name_of_shippment").value
  } else{
    var file = document.getElementById('json')
    file.value = JSON.stringify(data)
    document.getElementById("name").value = document.getElementById("name_of_shippment").value
  }
}


function alert_error(error_msg){
  alert(error_msg);
}