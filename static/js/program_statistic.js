if (typeof program_statistic != 'undefined'){

	google.charts.setOnLoadCallback(drawBarChart);

	function drawBarChart(){
		var data = google.visualization.arrayToDataTable(program_statistic['chart_array']);


		var options = {
			chart: {
				title: program_statistic['name'],
				subtitle: 'Публикации и ошибки'
			}
		}



		var chart = new google.charts.Bar(document.getElementById(program_statistic['id'].toString()));

		chart.draw(data, options);
	}
}