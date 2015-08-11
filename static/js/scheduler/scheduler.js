var G_timezone_offset = new Date().getTimezoneOffset();

function load_scheduler(){
    
    if ($("#scheduler").data("kendoScheduler") ){
        
        $("#scheduler").data("kendoScheduler").destroy();
        
        $('#scheduler').find('.k-header').hide();
        
    }
    
    var dataSource = load_category_datasource();
    
    
    $("#scheduler").kendoScheduler({
        date : new Date(),
        startDate: new Date(),
        startTime: new Date(new Date().getFullYear(), new Date().getMonth(),new Date().getDate(),7, 0, 0, 0),
        height: 550,
        views: [
            "day",
            "week",
            "month",
            {type : "agenda", selected : true},
        ],
        dataSource: {
            batch: true,
            transport: {
                read: {
                    url: "/load_events_ajax/",
                    dataType: "json",
                    type: 'post',
                },
                update: {
                    url: "/update_events_ajax/",
                    dataType: "json",
                    type: 'post',
                },
                create: {
                    url: "/create_events_ajax/",
                    dataType: "json",
                    type: 'post',
                },
                destroy: {
                    url: "/delete_event_ajax/",
                    dataType: "json",
                    type: 'post',
                },
                parameterMap: function(options, operation) {
                    if (operation !== "read" && options.models) {
                        return {models: kendo.stringify(options.models), tz: kendo.stringify(G_timezone_offset)};
                    }else if (operation == 'read') {
                        var value = {};
                        value['tz'] = G_timezone_offset;
                        return {models: kendo.stringify(value)};
                    }
                }
            },
            schema: {
                data: "details",
                model: {
                    id: "eventId",
                    fields: {
                        eventId: { from: "eventId", type: "number" },
                        title: { from: "title", defaultValue: "No title", validation: { required: true } },
                        start: { type: "date", from: "start" },
                        end: { type: "date", from: "end" },
                        description: { from: "description" },
                        recurrenceId: { from: "recurrenceID" },
                        recurrenceRule: { from: "recurrenceRule" },
                        recurrenceException: { from: "recurrenceException" },
                        categoryId: { from: "categoryId"},
                        isAllDay: { type: "boolean", from: "isAllDay" }
                    }
                }
            },
            error: function (e) {
                console.log(e);
                $('#scheduler_error').find('span.errormsg').html(e.errorThrown);
                $('#scheduler_error').show();
            },
            change: function (e) {
                
            },
            requestStart: function (e) {
                $('#scheduler_error').hide();
            }
        },
        resources: [
            {
                field: "categoryId",
                title: "Category",
                dataSource: dataSource,
                multiple: false,
            }
        ],
        "messages": {
            "today": gettext("today"),
            "save": gettext("save"),
            "cancel": gettext("cancel"),
            "destroy": gettext("destory"),
            "event": gettext("event"),
            "date": gettext("date"),
            "time": gettext("time"),
            "allDay": gettext("allDay"),
            "views": {
                "day": gettext("day"),
                "week": gettext("week"),
                "month":gettext("month"),
                "agenda" : gettext("agenda"),
            },
            "category":gettext("Category"),
            "recurrenceMessages": {
                "deleteWindowTitle": gettext("Delete Event"),
                "deleteWindowOccurrence": gettext("Delete ocurrence event"),
                "deleteWindowSeries": gettext("Delete whole serial"),
                "editWindowTitle": gettext("Edit Event"),
                "editWindowOccurrence": gettext("Edit ocurrence event"),
                "editWindowSeries": gettext("Edit whole serial"),
                "editRecurring": gettext("Are you sure to edit the recurrence ?"),
                "deleteRecurring": gettext("Are you sure the delete the recurrence event ?")
            },
            "editor": {
                "title": gettext("Title"),
                "start": gettext("Start"),
                "end": gettext("End"),
                "allDayEvent": gettext("allDayEvent"),
                "description": gettext("Description"),
                "repeat": gettext("Repeat"),
                "timezone": gettext("Timezone"),
                "startTimezone": gettext("Start Timezone"),
                "endTimezone": gettext("End Timezone"),
                "separateTimezones": gettext("Separate Timezone"),
                "editorTitle": gettext("Edit")
            },
            "recurrenceEditor": {
                "frequencies": {
                    "never": gettext("Never"),
                    "daily": gettext("Daily"),
                    "weekly": gettext("Weekly"),
                    "monthly": gettext("Monthly"),
                    "yearly": gettext("Yearly")
                },
                "daily": {
                    "repeatEvery": gettext("Repeat every day"),
                    "days": gettext("days")
                },
                "weekly": {
                    "weeks": gettext("Weeks"),
                    "repeatEvery": gettext("Repeat every"),
                    "repeatOn": gettext("Repeat on")
                },
                "monthly": {
                    "repeatEvery": gettext("Repeat every"),
                    "repeatOn": gettext("Repeat on"),
                    "months": gettext("Months"),
                    "day": gettext("Day"),
                },
                "yearly": {
                    "repeatEvery": gettext("Repeat every"),
                    "repeatOn": gettext("Repeat on"),
                    "years": gettext("Years"),
                    "of": gettext("of"),
                },
                "end": {
                    "endLabel": gettext("end label"),
                    "endNever": gettext("Never end"),
                    "endCountAfter": gettext("Counter after"),
                    "endCountOccurrence": gettext("Count ocurrence end"),
                    "endUntilOn": gettext("Am"),
                },
                "offsetPositions": {
                    "first": gettext("First"),
                    "second": gettext("Second"),
                    "third": gettext("Third"),
                    "fourth":gettext("Fourth"),
                    "last": gettext("Last"),
                }
            }
        }
    });
    
    var scheduler = $("#scheduler").data("kendoScheduler");
                    
        scheduler.wrapper.on("mouseup touchend", ".k-scheduler-table td, .k-event", function(e) {
      var target = $(e.currentTarget);
      
      if (target.hasClass("k-event")) {
        var event = scheduler.occurrenceByUid(target.data("uid"));
        scheduler.editEvent(event);
      } else {
        var slot = scheduler.slotByElement(target[0]);

        scheduler.addEvent({
          start: slot.startDate,
          end: slot.endDate
        });
      }
    });
}