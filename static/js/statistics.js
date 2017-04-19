if (typeof statistics != 'undefined'){

	/*google.charts.load('current', {'packages':['bar', 'corechart']});*/

	google.charts.setOnLoadCallback(drawBarChart);

	function drawBarChart(){
		$.each(statistics, function(i){

			var data = google.visualization.arrayToDataTable(statistics[i]['chart_array']);


			var options = {
				chart: {
					title: statistics[i]['name'],
					subtitle: 'Публикации и ошибки'
				}
			}



			var chart = new google.charts.Bar(document.getElementById(statistics[i]['id'].toString()));

			chart.draw(data, options);
		});
	}
}