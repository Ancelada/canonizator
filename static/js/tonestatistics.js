if (typeof tonestatistics != 'undefined'){

	google.charts.setOnLoadCallback(drawStackedColumnChart);

	function drawStackedColumnChart(){
		$.each(tonestatistics, function(i){
			if (tonestatistics[i]['data'].length > 1){
				var data = google.visualization.arrayToDataTable(tonestatistics[i]['data']);

				var options = {
					title: tonestatistics[i]['name'],
					subtitle: tonestatistics[i]['name_rus'],
					legend: {position: 'top', maxLines: 4},
					isStacked: true,
				}


				var chart = new google.visualization.ColumnChart(
					document.getElementById(tonestatistics[i]['id'])
				);

				chart.draw(data, options);
			}
		});
	}
}