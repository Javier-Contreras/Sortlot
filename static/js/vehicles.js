//
// vehicles.js
// static
//
// Created by Javier Contreras el 13/03/2021
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// Universidad Politécnica de Madrid
// 

var columns = ['image', 'registration', 'capacity', "use"]

window.addEventListener('DOMContentLoaded', (event) => {
	var html = '';
	for(var i = 0; i < data.length; i++){
		var use = data[i].use ? "checked" : "";
        var truck_img = 'truck_'+i;
   
        html += '<tr><td readonly="readonly" class="uneditable">' + i + 
        '</td><td class="uneditable"><img width="400px" height="200px" alt="'
        +truck_img+'" src='+ trucks_img[i]+
        '> </td><td class="uneditable">' + data[i].registration + 
        '</td><td class="uneditable">' + data[i].capacity + 
        '</td><td class="input_cell"><input type="checkbox" ' + use + '></td></tr>';
    }

	$('#vehicles_table tr').first().after(html);
	make_table_editable_vehicles();
});

function make_table_editable_vehicles(){
		var prev_value
		var new_value
		$('#vehicles_table').editableTableWidget();

		$('#vehicles_table' + ' td.uneditable').click(function(e) {
			return false;
		});
		//    

		$("#vehicles_table").on('change', function(e, value) {
			var clickedCell = $(e.target).closest("td");
			var clickedRow = $(e.target).closest("tr");
			var index = clickedCell.index()-1;
			var data_index = clickedRow.index()-1;

			field = columns[index];
			if (field == "use"){
				if (data[data_index][field])
			    	data[data_index][field] = false;
				else 
			    	data[data_index][field] = true;
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
