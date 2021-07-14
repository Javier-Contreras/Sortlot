//
// solution.js
// static
//
// Created by Javier Contreras el 13/03/2021
// Escuela Técnica Superior de Ingenieros de Telecomunicación
// Universidad Politécnica de Madrid
// 

vehicles_registration_used = [];
loaded = [];

window.addEventListener('DOMContentLoaded', (event) => {
  for (var i = 0; i < solution.routes.length ; i++){
    if  (solution.routes[i].length > 2){
      vehicles_registration_used.push(data.vehicles[i].registration)
      loaded.push(false)
    }
  }
  
  html = ''
  for (var i = 0; i<solution.result_table_content.length; i++){
    table_element = solution.result_table_content[i]
    if (table_element['route_distance'] != 0)
      html += '<tr><td readonly="readonly" class="uneditable">' + 
      table_element['vehicle'] + '</td><td readonly="readonly" class="uneditable">' + 
      table_element['route'] + '</td><td readonly="readonly" class="uneditable">' + 
      table_element['route_time'] + '</td><td readonly="readonly" class="uneditable">' + 
      table_element['route_distance'] + '</td><td readonly="readonly" class="uneditable">' + 
      table_element['route_load'] + '</td></tr>';
  }
  $('#solution tr').first().after(html);

  for (var i = 0; i< vehicles_registration_used.length;i++){
    
    registration = vehicles_registration_used[i]
    var btn = document.createElement("input");
    btn.type = "button";
    btn.className = "btn btn-dark";
    btn.style.margin = "3px";
    btn.style.textAlign = "center";
    btn.name = registration;
    btn.value = registration;
    btn.id = registration;
    
    //<input type="button" name="button1" id="button1" onclick="map_route(document.getElementById('button1').value)" value="4538 NHG">
    //<input type="button" id="button2" onclick="map_route(document.getElementById('button2').value)" value="1221 DFS">
    callback = 'map_route(\"'+registration+'\")'
    btn.setAttribute("onClick",callback);
    document.getElementById("nav_buttons").appendChild(btn);
 

    var div = document.createElement("div");
    div.style.width = "80%";
    div.style.height = "600px";
    div.style.display = "none";
    div.style.margin = "15px";
    div.style.marginLeft = "10%";

    div.name = registration + "_map";
    div.id = registration + "_map";

    document.getElementById("map").appendChild(div);

  }
  map_route(vehicles_registration_used[0])
});



function Export() {
  html2canvas(document.getElementById('solution-table'), {
    onrendered: function (canvas) {
      var data = canvas.toDataURL();
      var docDefinition = {
        content: [{
          image: data,
          width: 500
        }]
      };
      pdfMake.createPdf(docDefinition).download("Routes.pdf");
    }
  });
}

function download() {
  var a = document.createElement("a");
  var file = new Blob([JSON.stringify(solution.result_table_content)], {type: 'text/plain'});
  a.href = URL.createObjectURL(file);
  a.download = 'json.txt';
  a.click();
}
