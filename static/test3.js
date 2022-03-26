function incrementValue(e) {
    e.preventDefault();
    update=(document.querySelector(".origin-price").innerHTML)

    var fieldName = $(e.target).data('field');
    var parent = $(e.target).closest('div');
    var currentVal = parseInt(parent.find('input[name=' + fieldName + ']').val(), 10);

    if (!isNaN(currentVal)) {
        parent.find('input[name=' + fieldName + ']').val(currentVal + 1);
        update=parseInt(update ) * (currentVal +1)
    } else {
        parent.find('input[name=' + fieldName + ']').val(0);
        update=0
    }
    document.querySelector(".updated-price").innerHTML = String(update)+"$"

}

function decrementValue(e) {
    e.preventDefault();
    update=(document.querySelector(".origin-price").innerHTML)

    var fieldName = $(e.target).data('field');
    var parent = $(e.target).closest('div');
    var currentVal = parseInt(parent.find('input[name=' + fieldName + ']').val(), 10);

    if (!isNaN(currentVal) && currentVal > 0) {
        parent.find('input[name=' + fieldName + ']').val(currentVal - 1);
        update=parseInt(update ) * (currentVal -1)
    } else {
        parent.find('input[name=' + fieldName + ']').val(0);
        update=0
    }
    document.querySelector(".updated-price").innerHTML = String(update)+"$"
}
$("#increment").click(function(e) {
 incrementValue(e)
  });


$('#decrement').on('click', function(e) {
    decrementValue(e);
});