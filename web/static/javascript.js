

var todayDate = new Date().getDate();
$(function() {
    $('#datetime_1').datetimepicker({
                minDate: new Date(),
                maxDate: new Date(new Date().setDate(todayDate + 4)),
                format: 'YYYY-MM-DD HH:mm',

                stepping: 30,
                sideBySide: true,
            });
    $('#datetime_2').datetimepicker({
                minDate: new Date(),
                maxDate: new Date(new Date().setDate(todayDate + 4)),
                format: 'YYYY-MM-DD HH:mm',

                stepping: 30,
                sideBySide: true,
            });
    $("#datetime_1").on("dp.change", function(e) {
                $('#datetime_2').data("DateTimePicker").minDate(e.date);
                $('#datetime_2').data("DateTimePicker").date(e.date)
            });
    });

//get the time and station form the user selection
function display_time(){
     var selecttime1 = $('#datetime_1').data("DateTimePicker").date();
     var selecttime2 = $('#datetime_2').data("DateTimePicker").date();
      if (selecttime1) {
                //convert time in unix format
                var selecttime1_unix = selecttime1.unix();
                var selecttime2_unix = selecttime2.unix();
            }
     console.log(selecttime1_unix);
     console.log(selecttime2_unix);

     var station1 = $('#dropdown').val();
     var station2 = $('#des_dropdown').val();

     console.log(station1);
     console.log(station2);

     var url = 'http://18.203.168.242/' + station1 + '/' + selecttime1_unix + '/' + station2 + '/' + selecttime2_unix;
     let json = $.getJSON(url, null, function(obj) {
                showResult(obj)
                drawPredictChart(obj)
            });
}


//show the map things

function dropdown(){
    let json = $.getJSON("http://18.203.168.242/bikeMix", null, function (obj) {

        var stations = obj.bikeMix;
        var options = "<option value=''>Select a departure</option>";
        for (var i = 0; i < stations.length; i++) {
            var StationName = stations[i].name;
            var number = stations[i].number;
            options += "<option value ='" + number + "'>" + StationName + "</option>";

        }
        document.getElementById("dropdown").innerHTML = options


    })
}
dropdown();

function Des_dropdown(){
    let json = $.getJSON("http://18.203.168.242/bikeMix", null, function (obj) {

        var stations = obj.bikeMix;
        var options = "<option value=''>Select a destination</option>";
        for (var i = 0; i < stations.length; i++) {
            var StationName = stations[i].name;
            var number = stations[i].number;
            options += "<option value ='" + number + "'>" + StationName + "</option>";


        }
        document.getElementById("des_dropdown").innerHTML = options


    })
}
Des_dropdown();

function showResult(obj){

  var FromStation=obj[0];
  var From_availableBikes=obj[6][0];
  var ToStation=obj[1];
  var To_availableBikeStands=obj[14][1];
  var From_DTime=obj[2];

  var From_DayOfWeek=[3];
  if (From_DayOfWeek==0){
    From_DayOfWeek="Monday";
  }else if (From_DayOfWeek==1){
    From_DayOfWeek="Tuesday";
  }else if (From_DayOfWeek==2){
    From_DayOfWeek="Wednesday";
  }else if (From_DayOfWeek==3){
    From_DayOfWeek="Thursday";
  }else if (From_DayOfWeek==4){
    From_DayOfWeek="Friday";
  }else if (From_DayOfWeek==5){
    From_DayOfWeek="Sataurday";
  }else if (From_DayOfWeek==6){
    From_DayOfWeek="Sunday";
  };


  var To_DTime=obj[4];

  var To_DayOfWeek=obj[5];

  if (To_DayOfWeek==0){
    To_DayOfWeek="Monday";
  }else if (To_DayOfWeek==1){
    To_DayOfWeek="Tuesday";
  }else if (To_DayOfWeek==2){
    To_DayOfWeek="Wednesday";
  }else if (To_DayOfWeek==3){
    To_DayOfWeek="Thursday";
  }else if (To_DayOfWeek==4){
    To_DayOfWeek="Friday";
  }else if (To_DayOfWeek==5){
    To_DayOfWeek="Sataurday";
  }else if (To_DayOfWeek==6){
    To_DayOfWeek="Sunday";
  };

  let json = $.getJSON("http://18.203.168.242/bikeMix", null, function (data) {

    var stations = data.bikeMix;
    var FromStationName;
    var ToStationName;
        for (var i = 0; i < stations.length; i++) {
            var StationName = stations[i].name;
            var number = stations[i].number;
            if (number == FromStation){
              FromStationName=StationName;}
              if (number == ToStation){
                ToStationName=StationName;}


        }

  document.getElementById('results').innerHTML = "Our model is showing there will be " + From_availableBikes
  + " bikes available at pick up station: " +FromStationName + " on " + From_DayOfWeek+ " at " + From_DTime +"<br>"+" and " +
  To_availableBikeStands+ " bike stands available at drop off station: " +ToStationName+" on " + To_DayOfWeek+ " at " + To_DTime +"."


})
}

function drawPredictChart(obj) {

  var From_availableBikes = obj[7][0];
  var From_availableBikesSub1h = obj[8][0];
  var From_availableBikesSub2h = obj[9][0];
  var From_availableBikesSub3h = obj[10][0];

  var From_availableBikesPlus1h = obj[11][0];
  var From_availableBikesPlus2h = obj[12][0];
  var From_availableBikesPlus3h = obj[13][0];

  var To_availableBikes = obj[14][1];
  var To_availableBikesSub1h = obj[15][1];
  var To_availableBikesSub2h = obj[16][1];
  var To_availableBikesSub3h = obj[17][1];

  var To_availableBikesPlus1h = obj[18][1];
  var To_availableBikesPlus2h = obj[19][1];
  var To_availableBikesPlus3h = obj[20][1];

  var FromHour = obj[20];
  FromHour = parseInt(FromHour+1);

  var ToHour = obj[21];
  FromHour = parseInt(FromHour+1);

  google.charts.load('current', {
                    'packages': ['corechart']
                });
  google.charts.setOnLoadCallback(drawFromChart);
  google.charts.setOnLoadCallback(drawToChart);

  function drawToChart() {
      var ToData = google.visualization.arrayToDataTable([
          ['Hour', 'Available Bikes'],
          ['1h-', To_availableBikesSub1h],
          ['2h-', To_availableBikesSub2h],
          ['3h-', To_availableBikesSub3h],
          [FromHour, From_availableBikes],
          ['1h+', To_availableBikesPlus1h],
          ['2h+', To_availableBikesPlus2h],
          ['3h+', To_availableBikesPlus3h],

      ]);


  var options = {
    title: 'Bikes stands available at drop off station',

    hAxis: {
      title: 'Time',
      titleTextStyle: {
        color: '#333'
      }
    },
    vAxis: {
      minValue: 0,

    }
  };

var chart = new google.visualization.LineChart(document.getElementById('chart_div_predictTo'));
chart.draw(ToData, options);

}



  function drawFromChart() {
      var FromData = google.visualization.arrayToDataTable([
          ['Hour', 'Available Bikes'],
          ['1h-', From_availableBikesSub1h],
          ['2h-', From_availableBikesSub2h],
          ['3h-', From_availableBikesSub3h],
          [FromHour, From_availableBikes],
          ['1h+', From_availableBikesPlus1h],
          ['2h+', From_availableBikesPlus2h],
          ['3h+', From_availableBikesPlus3h],

      ]);


  var options = {
    title: 'Bikes available at pick up station',

    hAxis: {
      title: 'Time',
      titleTextStyle: {
        color: '#333'
      }
    },
    vAxis: {
      minValue: 0,

    }
  };

var chart = new google.visualization.LineChart(document.getElementById('chart_div_predictFrom'));
chart.draw(FromData, options);

}
};


function dropdownForMarker(){
    let json = $.getJSON("http://18.203.168.242/bikeMix", null, function (obj) {

        var stations = obj.bikeMix;
        var options = "<option value=''>Select a station</option>";
        for (var i = 0; i < stations.length; i++) {
            var StationName = stations[i].name;
            var number = stations[i].number;
            options += "<option value ='" + number + "'>" + StationName + "</option>";

        }
        document.getElementById("Markerdropdown").innerHTML = options


    })
}
dropdownForMarker();



function MarkerFromDropdown (){
    var DDnumber = document.getElementById("Markerdropdown").value;
    console.log(DDnumber);
    let json = $.getJSON("http://18.203.168.242/bikeMix", null, function (obj) {
    var stations = obj.bikeMix;
    for (var i = 0; i < stations.length; i++) {
        var number = stations[i].number;
        if (number == DDnumber){
            var lat=stations[i].lat;
            var lng=stations[i].lng;

            var stationsInfo =  '<div class="info_content">' +
        '<p>' + 'Station Number:' + stations[i].number + '</p>' +
        '<p>' + 'Station Name:'+ stations[i].name + '</p>' + '<p>' + 'Total Bike Stands:'+ stations[i].bike_stands + '</p>' +
        'Available Bike Stands:'+ stations[i].available_bike_stands + '</p>' +
        'Available Bikes:'+ stations[i].available_bikes + '</p>' +
                        '</div>';
                        var marker = new google.maps.Marker({
                        position: {
                            lat: lat,
                            lng: lng
                        },
                        map: map,

                        icon: {
                        url: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png",
                        },
                        animation:google.maps.Animation.Drop,
                        title: stations[i].name,
                        station_number: stations[i].number
                    });
                    marker.setVisible(false);
                    map.setZoom(15);
                    map.panTo(marker.position);
                    marker.setMap(map);

                    var infowindow  = new google.maps.InfoWindow({
                        content: ""
                    });
                    var pre = false;

            google.maps.event.addListener(marker,'click', (function(marker,stationsInfo,infowindow){


                pre = infowindow;
                var number_id = stations[i].number;
                pre.setContent(stationsInfo);
                    pre.open(map, marker);
                    showchart(number_id );
                  showchart_week(number_id );
                    showchart_hour(number_id );

            }) (marker,stationsInfo,infowindow));

    }};
    });
    };




function showchart(number_id){

google.charts.load('current', {
'packages': ['corechart']
});

google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var url = 'http://18.203.168.242/dynamic/' + number_id;

let json = $.getJSON(url, null, function (obj) {
 var chart_info = obj.chart_info;
 var arr = [];
 arr.push(['hour', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']);
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
    console.log('arr1', arr1);
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
    gridlines: {
      count: 24,
    }
  }
};

var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
chart.draw(data, options);
});
}}
function showchart_week(number_id){

google.charts.load('current', {
'packages': ['corechart']
});

google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var url = 'http://18.203.168.242/dynamic/weekdata/' + number_id;

let json = $.getJSON(url, null, function (obj) {
 var chart_info = obj.chart_info;
 var arr = [];
 arr.push(['Week', 'Available Bikes']);
 console.log('cgart_info', chart_info);
 for (var i = 0; i < chart_info.length; i++) {
     // var arr1 = [];

     arr.push(chart_info[i]);

        }


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
  var url = 'http://18.203.168.242/dynamic/hourdata/' + number_id;

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
        arr.push(arr1)
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

var Variable;
function myFunction() {
    Variable = setTimeout(showPage, 2000);
}

function showPage() {
  document.getElementById("Myloader").style.display = "none";
  document.getElementById("ActualDiv").style.display = "block";
}

window.addEventListener('load', myFunction);