$(document).ready(function(e){
    var lang_code = $('#lang_code').val();
    
    if (lang_code == 'zh-hans') {
        console.log(lang_code);
        kendo.culture('zh-CN');
    }else{
        console.log(lang_code);
        kendo.culture('en-US');
    }
    
    $('.datepicker').kendoDatePicker({
    });
})

function change_language(language){
    $.ajax({
        url : '/change_language_ajax/',
        data : {
            'lang' : language,
        },
        type : 'post',
        dataType:'json',
        success:function(e){
            window.location.reload();
        }
    });
}

$(function() {
    $('#languageWrapper').on('mousedown', 'div', function() {
        $(this).addClass('draggable').parents().on('mousemove', function(e) {
            $('.draggable').offset({
                top: e.pageY - $('.draggable').outerHeight() / 2,
                left: e.pageX - $('.draggable').outerWidth() / 2
            }).on('mouseup', function() {
                $(this).removeClass('draggable');
            });
        });
        e.preventDefault();
    }).on('mouseup', function() {
        $('.draggable').removeClass('draggable');
    });
});
