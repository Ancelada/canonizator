if (typeof tonestatistics_common != 'undefined'){

	google.charts.setOnLoadCallback(drawColumnChartCommon);

	function drawColumnChartCommon(){
		$.each(tonestatistics_common, function(i){
			if (tonestatistics_common[i]['data'].length > 1){
				var data = google.visualization.arrayToDataTable(tonestatistics_common[i]['data']);

				var options = {
					title: tonestatistics_common[i]['name'],
					subtitle: tonestatistics_common[i]['name_rus'],
				}


				var chart = new google.visualization.ColumnChart(
					document.getElementById(tonestatistics_common[i]['id'])
				);

				chart.draw(data, options);
			}
		});
	}
}