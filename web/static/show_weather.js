function show_weather(){
 let json = $.getJSON("http://18.203.168.242/weather", null, function (data) {

    if ('weather' in data) {

        var weather = data.weather;
        var description = weather[0].description;
        var feels_like = weather[0].feels_like;
        var gust = weather[0].gust;
        var icon=weather[0].icon;

        var iconUrl = "http://openweathermap.org/img/w/" + icon + ".png";
        console.log(iconUrl);
        display_info = "<table border = 1 id=\"weatherTable\">";
            display_info += "<tr><td>feels like</td><td>" + weather[0].feels_like + "</td><td>icon</td><td>" + "<img src='" + iconUrl  + "'>"  +"</td></tr>";
            display_info += "<tr><td>temperature</td><td>" + weather[0].temp + "</td><td>description </td><td>" + weather[0].description + "</td></tr>";
            display_info += "<tr><td>min temperature</td><td>" + weather[0].temp_min + "</td><td>pressure</td><td>" + weather[0].pressure + " hpa</td></tr>";
            display_info += "<tr><td>max temperature</td><td>" + weather[0].temp_max + "</td><td>humidity</td><td>" + weather[0].humidity + "%</td></tr>";
            display_info += "<tr><td>sunrise</td><td>" + weather[0].sunrise + "</td><td>sunset</td><td>" + weather[0].sunset + "</td></tr>";


            display_info += "</table>"

            document.getElementById("weather").innerHTML = display_info;
    }

});
}
show_weather();