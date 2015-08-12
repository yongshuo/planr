$(document).ready(function(e){
    load_pie_chart();
    load_line_chart();
})

$(document).bind("kendo:skinChange", load_pie_chart);
$(document).bind("kendo:skinChange", load_line_chart);


function load_pie_chart(){
    var dataSource = new Array();
    
    $.ajax({
        url: '/load_dashboard_pie/',
        dataType: 'json',
        type: 'post',
        beforeSend: function(e){
            $('#money_dashboard').hide();
        },
        error : function(e){
            $('#money_dashboard').find('span.errormsg').html(e.errorThrown);
            $('#money_dashboard').show();  
        },
        success: function(e){
            for (var i = 0; i< e.details.length; i++) {
                dataSource.push({
                    'category' : e.details[i].category,
                    'value' : e.details[i].value,
                    'color' : e.details[i].color,
                });    
            }
            $("#dashboard_pie").kendoChart({
                dataSource: dataSource,
                
                series: [{
                    field: "value",
                    categoryField: "category",
                }],
                
                title: {
                    position: "top",
                    text: gettext("Your money category PIE chart")
                },
                legend: {
                    position: "top"
                },
                chartArea: {
                    background: ""
                },
                seriesDefaults: {
                    type: "pie",
                    labels: {
                        visible: true,
                        background: "transparent",
                        template: "#= category # - #= kendo.format('{0:P}', percentage)#",
                        position: "outsideEnd",
                    }
                },
                tooltip: {
                    visible: true,
                    template:  "#= category # - #= kendo.format('{0:P}', percentage) #"
                }
            });
        }
    });
}

function load_line_chart(){
    var dataSource = new Array();
    
    $.ajax({
        url: '/load_dashboard_line/',
        dataType: 'json',
        type: 'post',
        beforeSend: function(e){
            $('#money_dashboard').hide();
        },
        error : function(e){
            $('#money_dashboard').find('span.errormsg').html(e.errorThrown);
            $('#money_dashboard').show();  
        },
        success: function(e){
            $("#dashboard_linechart").kendoChart({
                title: {
                    text: gettext("Your money balance line chart for recent 14 days")
                },
                legend: {
                    position: "top"
                },
                chartArea: {
                    background: ""
                },
                seriesDefaults: {
                    type: "line",
                    style: "smooth"
                },
                series: [{
                    name: gettext("Balance"),
                    data: e.value_list,
                }],
                valueAxis: {
                    labels: {
                        format: "{0}"
                    },
                    line: {
                        visible: false
                    },
                    axisCrossingValue: -500
                },
                categoryAxis: {
                    categories: e.date_list,
                    majorGridLines: {
                        visible: false
                    },
                    labels: {
                        rotation: "auto"
                    }
                },
                tooltip: {
                    visible: true,
                    format: "{0}%",
                    template: "#= series.name #: #= value #"
                }
            });
        }
    });        
}
