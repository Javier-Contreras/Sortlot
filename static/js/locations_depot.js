//
// locations_depot.js
// static
//
// Created by Javier Contreras el 13/03/2021
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// Universidad Politécnica de Madrid
// 

var markers=[]
var marker = null;
var columns = ['name', 'address', "use"];

window.addEventListener('DOMContentLoaded', (event) => {
	console.log(data);

	var html = '';
	for(var i = 0; i < data.length; i++){
		data[i].use = (data[i].use === 'true') || (data[i].use == true);
		var use = data[i].use ? "checked" : "";
		html += '<tr><td readonly="readonly" class="uneditable">' + i + 
		'</td><td readonly="readonly" class="uneditable">' + data[i].name + 
		'</td><td readonly="readonly" class="uneditable">' + data[i].address + 
		'</td><td class="input_cell"><input type="checkbox" ' + use + '></td></tr>';

		if (data[i].use)
		  var src_point = blue_marker;
		else
		  var src_point = red_marker;

		map = initialize_map("map-depot", data[i].coordinates,src_point);
		
		var lat = data[i].coordinates[0];
		var lng = data[i].coordinates[1];

		add_map_point(lat,lng, i);


	}

	$('#depot_table tr').first().after(html);

	make_table_editable_depot();
});





function make_table_editable_depot(){
		var prev_value
		var new_value
		$('#depot_table').editableTableWidget();

		$('#depot_table' + ' td.uneditable').click(function(e) {
			return false;
		});
		//    

		$("#depot_table").on('change', function(e, value) {
			var clickedCell = $(e.target).closest("td");
			var clickedRow = $(e.target).closest("tr");
			var index = clickedCell.index()-1;
			var data_index = clickedRow.index()-1;
			  //if (clickedCell.index() == 0 || clickedCell.index() == 1){

			  //  return;
			 // }


			field = columns[index];
			if (field == "use"){
				if (data[data_index][field]){
					var src_point = red_marker;
			    	data[data_index][field] = false;
				}
				else {
					data[data_index][field] = true;
					var src_point = blue_marker;
				}
				var feature = marker.getSource().getFeatureById(data_index)
        		feature.setStyle(new ol.style.Style({ image: new ol.style.Icon({
                  anchor: [0.5, 0.5],
                  anchorXUnits: "fraction",
                  anchorYUnits: "fraction",
                  src: src_point
              }) }))
			    
			} else {

			    data[data_index][field] = clickedCell.children("input").val();
			    new_value = value;
			}

			var file = document.getElementById('json');
			file.value = data;
			console.log(data);


		});
		

		$(".edit_field").click(function(e) {

			var clickedCell = $(e.target).closest("td");
			var clickedRow = $(e.target).closest("tr");
			if (clickedCell.index() == 0 || clickedCell.index() == 6)
				return false;
			prev_value = clickedCell.text();

		});

		$(".input_cell").click(function(e) {
	    	$( this ).children("input").focus();
		});

	}

function format(){
	var file = document.getElementById('json')
	file.value = JSON.stringify(data)
	console.log(name)
	console.log(data)
	document.getElementById("name").value = name
}