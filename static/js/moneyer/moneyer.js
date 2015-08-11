$(document).ready(function(e){
    load_moneyer();
})

function load_moneyer(){
    var from_date = $('#from_date').val();
    var to_date = $('#to_date').val();
    
    var dataSource = new kendo.data.DataSource({
        transport: {
            read:  {
                url: '/load_moneyer/',
                dataType: "json",
                type: 'post',
            },
            update: {
                url: '/update_moneyer/',
                dataType: "json",
                type: 'post',
            },
            destroy: {
                url: '/delete_moneyer/',
                dataType: "json",
                type: 'post',
            },
            create: {
                url: '/create_moneyer/',
                dataType: "json",
                type: 'post',
            },
            parameterMap: function(options, operation) {
                if (operation !== "read" && options.models) {
                    console.log(options.models);
                    return {models: kendo.stringify(options.models)};
                }else if (operation == "read") {
                    return {from_date: from_date, to_date:to_date};
                }
            }
        },
        batch: true,
        
        schema: {
            data: "details",
            model: {
                id: "transactionID",
                fields: {
                    transactionID: { from: "transactionID", type: "number" },
                    category: { defaultValue: { categoryID: -1, categoryName: "Others"} },
                    date: {type: "date"},
                    credit: { type: "number", default: "0" , validation: { min: 0}},
                    debit: {type: "number",  default: "0" ,validation: {  min: 0}},
                    remarks: {from: "remarks", default: ""},
                }
            }
        },
        aggregate: [ { field:"credit", aggregate: "sum"}, {field: "debit", aggregate: "sum"}],
        error: function (e) {
            console.log(e);
            $('#moneyer_error').find('span.errormsg').html(e.errorThrown);
            $('#moneyer_error').show();
        },
        change: function (e) {
            if (e.action == "sync") {
                load_moneyer();
            }
        },
        requestStart: function (e) {
            $('#moneyer_error').hide();
        }
    });
    
    if ($("#moneyer").data("kendoGrid") ){
        
        $("#moneyer").data("kendoGrid").destroy();
    }
    
    $("#moneyer").kendoGrid({
        dataSource: dataSource,
        pageable: false,
        height: 550,
        toolbar: [{name:"create", text: gettext("Add a record")}],
        columns: [
            { field: "category", title: gettext("Category"), width: "200px", editor: categoryDropDownEditor, template: "#=category.categoryName#" },
            { field: "credit", footerTemplate:"#= kendo.toString(sum, 'C') # ",title:gettext("Credit"), format: "{0:c}",type: "number", width: "150px" },
            { field: "debit", footerTemplate:"#= kendo.toString(sum, 'C') # ", title: gettext("Debit"), format: "{0:c}",type: "number", width: "150px" },
            { field: "date", title: gettext("Date"), width: "150px" ,format:"{0:yyyy-MM-dd}" },
            { field: "remarks", title: gettext("Remarks"), width: "200px;" },
            
            {
                command: [
                {
                    name: "edit",
                    text: { // sets the text of the "Edit", "Update" and "Cancel" buttons
                        edit: gettext("Edit"),
                        update: gettext("Update"),
                        cancel: gettext("Cancel"),
                    }
                },
                { name: "destroy", text: gettext("Delete") },
                
                ],
                title: "&nbsp;",
                width: "200px",
                
            },
            
        ],
        editable: "inline",
    });
    
}

function categoryDropDownEditor(container, options){
    $('<input data-text-field="categoryName" data-value-field="categoryID" data-bind="value:' + options.field + '"/>')
    .appendTo(container)
    .kendoDropDownList({
        autoBind: false,
        dataSource: {
            type: "json",
            transport: {
                read: "/load_moneyer_category/",
            },
            schema: {
                data: "category",
            }
        }
    });
}