$(document).ready(function(e){
    load_event_dashboard();
});

var G_timezone_offset = new Date().getTimezoneOffset();

function load_event_dashboard(){
    var dataSource = new kendo.data.DataSource({
        transport: {
            read:  {
                url: '/load_event_dashboard/',
                dataType: "json",
            },
            parameterMap: function(options, operation) {
                if (operation == "read") {
                    return {tz: G_timezone_offset};
                }
            }
        },
        batch: true,
        
        schema: {
            data: "details",
            model: {
                id: "eventID",
            }
        },
        
        error: function (e) {
            $('#dashboard_event').find('span.errormsg').html(e.errorThrown);
            $('#dashboard_event').show();
        },
        change: function (e) {
            if (e.action == "sync") {
            }
        },
        requestStart: function (e) {
            $('#dashboard_event').hide();
        }
    });
    
    if ($("#my_events").data("kendoGrid") ){
        $("#my_events").data("kendoGrid").destroy();
    }
    
    $("#my_events").kendoGrid({
        dataSource: dataSource,
        pageable: false,
        height: 550,
        
        columns: [
            { field: "category", title: gettext("Category"), width: "200px"},
            { field: "title", title: gettext("Title"), width: "200px"},
            { field: "start",title:gettext("Start"), width: "200px" },
            { field: "end", title: gettext("End"), width: "200px" },
            { field: "description", title: gettext("Description"), width: "300px"},
        ],
    });
}