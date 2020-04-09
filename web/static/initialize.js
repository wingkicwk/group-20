var myCenter=new google.maps.LatLng(53.350140, -6.266155);
    var map;
    var mapProp;
function initialize() {

    mapProp = {
        center: new google.maps.LatLng(53.350140, -6.266155),
        zoom: 13,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    var marker = new google.maps.Marker({
        position: myCenter,
    });



    function showStationMarkers() {
        let json = $.getJSON("http://127.0.0.1:5000/bikeMix", null, function (obj) {

                var stations = obj.bikeMix;
                for (var i = 0; i < stations.length; i++) {
                    var lat = stations[i].lat;
                    var lng = stations[i].lng;


                    var stationsInfo =  '<div class="info_content">' +
                        '<p>' + 'Station Number:' + stations[i].number + '</p>' +
                        '<p>' + 'Station Name:'+ stations[i].name + '</p>' + '<p>' + 'Total Bike Stands:'+ stations[i].bike_stands + '</p>' +
                        'Available Bike Stands:'+ stations[i].available_bike_stands + '</p>' +
                        'Available Bikes:'+ stations[i].available_bikes + '</p>' +
                                        '</div>';

                    var station_number = stations[i].number;
                    var marker = new google.maps.Marker({
                        position: {
                            lat: lat,
                            lng: lng
                        },
                        map: map,
                        animation:google.maps.Animation.Drop,
                        title: stations[i].name,
                        station_number: stations[i].number
                    });
                    marker.setMap(map);


                    var infowindow  = new google.maps.InfoWindow({
                        content: ""
                    });
                    var pre = false;

                google.maps.event.addListener(marker,'click', (function(marker,stationsInfo,infowindow){
                    if(pre){
                        pre.close();
                    }
                    pre = infowindow;
                    var number_id = stations[i].number;
                    return function() {
                        pre.setContent(stationsInfo);
                        pre.open(map, marker);
                        showchart_week(number_id);
                        showchart_hour(number_id);
                        showchart(number_id);
                    };
                })(marker,stationsInfo,infowindow));
             };
        });

function showchart(number_id){

        google.charts.load('current', {'packages': ['corechart']});
        google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
             var url = 'http://127.0.0.1:5000/dynamic/' + number_id;

             let json = $.getJSON(url, null, function (obj) {
                 var chart_info = obj.chart_info;
                 var arr = [];
                 arr.push(['hour', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']);
                 console.log(arr);
                 for (var i = 0; i < chart_info.length; i++) {
                     var arr1 = [];

                    for (var j = 0; j < chart_info[i].length; j++) {
                        if (j==0){
                            arr1.push(chart_info[i][j]+"");
                        }
                        else{
                            arr1.push(chart_info[i][j]);
                        }
                    }
                    // console.log('arr1', arr1);
                     arr.push(arr1)
                }


            var data = google.visualization.arrayToDataTable(arr);

        var options = {
          title: 'Average bikes in use per hour, per day(based on the last 2 weeks)',

          hAxis: {
            title: 'Hour',
            titleTextStyle: {
              color: '#333'
            }
          },
            vAxis: {
            minValue: 0,
            }
           };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
            chart.draw(data, options);
             });
            }
        }
function showchart_week(number_id){

        google.charts.load('current', {
        'packages': ['corechart']
      });

      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
          var url = 'http://127.0.0.1:5000/dynamic/weekdata/' + number_id;

     let json = $.getJSON(url, null, function (obj) {
         var chart_info = obj.chart_info;
         // console.log(chart_info)
         var arr = [];
         arr.push(['Week', 'Available Bikes']);
         console.log('cgart_info', chart_info);
         for (var i = 0; i < chart_info.length; i++) {
             // var arr1 = [];

             arr.push(chart_info[i]);

                }



            console.log('arr', arr);
                // arr.push(arr1);


        var data = google.visualization.arrayToDataTable(arr);

        var options = {
          title: 'Average bikes in use per week',

          hAxis: {
            title: 'week',
            titleTextStyle: {
              color: '#333'
            }
          },
          vAxis: {
            minValue: 0,

          }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div_week'));
        chart.draw(data, options);
      });
      }

    }
function showchart_hour(number_id){

        google.charts.load('current', {
        'packages': ['corechart']
      });

      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
          var url = 'http://127.0.0.1:5000/dynamic/hourdata/' + number_id;

     let json = $.getJSON(url, null, function (obj) {
         var chart_info = obj.chart_info;
         var arr = [];
         arr.push(['Hour', 'Available Bikes']);
         console.log('cgart_info', chart_info);
          for (var i = 0; i < chart_info.length; i++) {
             var arr1 = [];

            for (var j = 0; j < chart_info[i].length; j++) {
                if (j==0){
                    arr1.push(chart_info[i][j]+"");
                }
                else{
                    arr1.push(chart_info[i][j]);
                }


            }
            // console.log('arr1', arr1);
                arr.push(arr1);
              console.log('arr1', arr1);
        }



        var data = google.visualization.arrayToDataTable(arr);

        var options = {
          title: 'Average bikes in use per hour',

          hAxis: {
            title: 'week',
            titleTextStyle: {
              color: '#333'
            }
          },
          vAxis: {
            minValue: 0,

          }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div_hour'));
        chart.draw(data, options);
      });
      }

    }
    }
    showStationMarkers();
}
google.maps.event.addDomListener(window, 'load', initialize);