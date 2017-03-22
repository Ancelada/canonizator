if (typeof statistics_dict != 'undefined'){

	google.charts.load('current', {'packages':['bar']});

	google.charts.setOnLoadCallback(drawChart);

	function drawChart(){
		$.each(statistics_dict, function(i){
			var data = google.visualization.arrayToDataTable(statistics_dict[i]['data']);

			var options = {
				charts: {
					'title': statistics_dict[i]['name'],
					'subtitle': 'Публикации и ошибки'
				}
			}

			var chart = new google.charts.Bar(document.getElementById(statistics_dict[i]['id'].toString()));

			chart.draw(data, options);
		});
	}

	console.log(statistics_dict);
}