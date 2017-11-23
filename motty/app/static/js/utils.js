function select_value(selector, value){
    if(selector == 'undefined' || selector == '') {
        console.error('first parameter cannot be empty');
        return;
    }

    $(selector + " option").each(function(index, elem){
        if($(elem).val() == value)
            $(elem).prop('selected', true);
    });
}

function toast(message){
    $('.toast').remove();
    $("header").after('<div class="toast container fixed">'+
        '<div class="columns">'+
            '<div class="column col-9 col-mx-auto">'+
                '<button class="btn btn-clear float-right"></button>'+
                message +
            '</div>'+
        '</div>'+
    '</div>');

    $('.toast .btn-clear').on('click', function(){
        $('.toast').remove();
    });
}

// activate toast close button to close their toast.
$(function() {
    $('.toast .btn-clear').on('click', function(){
        $('.toast').remove();
    });
});