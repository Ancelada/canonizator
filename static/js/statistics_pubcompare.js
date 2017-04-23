if (typeof statistics_pubcompare != 'undefined'){

	google.charts.setOnLoadCallback(drawPieChart);

	function drawPieChart(){
		var data = google.visualization.arrayToDataTable(statistics_pubcompare['chart_array']);

		var options = {
			title: statistics_pubcompare['name'],
		}

		var chart = new google.visualization.PieChart(document.getElementById(
			statistics_pubcompare['id'].toString()));

		chart.draw(data, options);
	}
}