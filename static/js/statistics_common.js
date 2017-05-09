if (typeof statistics_common != 'undefined'){

	/*google.charts.load('current', {'packages':['bar', 'corechart']});*/

	google.charts.setOnLoadCallback(drawBarChart2);

	function drawBarChart2(){
		$.each(statistics_common, function(i){

			var data = google.visualization.arrayToDataTable(statistics_common[i]['chart_array']);

			var options = {
				chart: {
					title: statistics_common[i]['name'],
					subtitle: 'Статистика работы всех програм.'
				}
			}

			var chart = new google.charts.Bar(document.getElementById(
				statistics_common[i]['id'].toString()));

			chart.draw(data, options);
		});
	}
}