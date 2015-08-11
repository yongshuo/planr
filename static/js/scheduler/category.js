$(document).ready(function(e){
    load_category();
    load_scheduler();
    
    $('.colorpicker').kendoColorPicker({
        value: '#47f900',
        buttons: false,
    });
    
    set_add_action();
});

function set_add_action(){
    var list_view = $('#category').data('kendoListView');
    
    $('#add_new_category').click(function(e) {
        list_view.add();
        e.preventDefault();
    });
}

function load_category_datasource(){
    var dataSource = new kendo.data.DataSource({
        transport: {
            read:  {
                url: "/load_category_ajax/",
                dataType: "json" ,
            },
            update: {
                url: "/update_category_ajax/",
                dataType: "json" ,
                type: 'post',
            },
            destroy: {
                url: "/delete_category_ajax/",
                dataType: "json",
                type: 'post',
            },
            create: {
                url: "/create_category_ajax/",
                dataType: "json",
                type: 'post',
            },
            parameterMap: function(options, operation) {
                if (operation !== "read" && options.models) {
                    return {models: kendo.stringify(options.models)};
                }
            }
        },
        batch: true,
        schema: {
            data : 'details',
            model: {
                id: "categoryId",
                fields: {
                    name: "name",
                    color: "color",
                    owner : 'owner'
                }
            },
            
        },
        error: function (e) {
            console.log(e);
            $('#category_error').find('span.errormsg').html(e.errorThrown);
            $('#category_error').show();
        },
        change: function (e) {
            if (e.action == 'sync') {
                load_scheduler();
            }
        },
        requestStart: function (e) {
            $('#category_error').hide();
        }
    });
    
    return dataSource;
}

function load_category(){
    
    if ($("#category").data("kendoListView") ){
        
        $("#category").data("kendoListView").destroy();
    }
    
    var list_view = $("#category").kendoListView({
        dataSource: load_category_datasource(),
        template: kendo.template($('#category_template').html()),
        editTemplate: kendo.template($('#edit_category_template').html()),
    });
}
