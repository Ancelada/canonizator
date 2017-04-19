if (typeof vocabulary_statistics != 'undefined'){

	/*google.charts.load('current', {'packages':['corechart']});*/

	google.charts.setOnLoadCallback(drawCoreChart);

	function drawCoreChart(){
		$.each(vocabulary_statistics, function(i){

			var data = google.visualization.arrayToDataTable(vocabulary_statistics[i]['google_chart']);

			var options = {
				title: vocabulary_statistics[i]['name'],
				subtitle: vocabulary_statistics[i]['name_rus'],
				hAxis: {title: 'Дата',  titleTextStyle: {color: '#333'}},
				vAxis: {minValue: 0},
				legend: {position: 'top'}
			}


			var chart = new google.visualization.AreaChart(
				document.getElementById(vocabulary_statistics[i]['name'])
			);

			chart.draw(data, options);
		});
	}
}