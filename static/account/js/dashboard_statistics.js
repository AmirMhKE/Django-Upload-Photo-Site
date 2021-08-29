$(document).ready(function() {
    let stat = JSON.parse($("#stat").val());
    let hits = [];
    let likes = [];
    let downloads = [];

    let dates = new Set();

    for(let item of stat["hits"]) {
        dates.add(en_nums_to_fa_nums(item[0]));
        hits.push(item[1]);    
    }

    for(let item of stat["likes"]) {
        dates.add(en_nums_to_fa_nums(item[0]));
        likes.push(item[1]);    
    }

    for(let item of stat["downloads"]) {
        dates.add(en_nums_to_fa_nums(item[0]));
        downloads.push(item[1]);    
    }

    dates = [...dates];
    
    let chart = {
        type: 'column'
    };
    let title = {
        text: $(".title").text()   
    };
    let subtitle = {
        text: 'آمار اخیر'  
    };
    let xAxis = {
        categories: dates,
        crosshair: true,
        className: "d-none d-xl-inline-block"
    };
    let yAxis = {
        min: 0,
        title: {
            text: 'تعداد'         
        },
        className: "hy-labels"      
    };
    let tooltip = {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style = "padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    };
    let plotOptions = {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        },
    };  
    let credits = {
        enabled: false
    };
    let series= [
        {
            name: 'تعداد لایک ها',
            data: likes
        }, 
        {
            name: 'تعداد دانلود ها',
            data: downloads
        }, 
        {
            name: 'تعداد بازدید ها',
            data: hits
        }, 
    ];
    
    let colors = ["#f30067", "#00d1cd", "#444444"];
    
    let json = {};   
    json.chart = chart; 
    json.title = title;   
    json.subtitle = subtitle; 
    json.tooltip = tooltip;
    json.xAxis = xAxis;
    json.yAxis = yAxis;  
    json.series = series;
    json.plotOptions = plotOptions;  
    json.credits = credits;
    json.colors = colors;
    $('#container').highcharts(json);

    for(item of selector(".hy-labels text")) {
        item.innerHTML = en_nums_to_fa_nums(item.innerHTML);
    }

    for(let i = 0; i < 3; i++) {
        for(label of selector(`[class$=highcharts-series-${i}]`)) {
            label.children[0].setAttribute("text-anchor", "end");
        }
    }
    
    function selector(s) {
        return document.querySelectorAll(s);
    }
});
