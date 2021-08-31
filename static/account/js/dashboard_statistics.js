$(document).ready(function() {
    let stat = JSON.parse($("#stat").html());
    
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
        categories: stat["dates"],
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
            data: stat["likes"]
        }, 
        {
            name: 'تعداد دانلود ها',
            data: stat["downloads"]
        }, 
        {
            name: 'تعداد بازدید ها',
            data: stat["hits"]
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
