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

// activate toast close button to close their toast.
$(function() {
    $('.toast .btn-clear').on('click', function(){
        $('.toast').remove();
    });
});