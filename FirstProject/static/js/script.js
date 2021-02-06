$(document).ready(function() {
    //Helper function to keep table row from collapsing when being sorted
	var fixHelperModified = function(e, tr) {
		var $originals = tr.children();
		var $helper = tr.clone();
		$helper.children().each(function(index)
		{
		  $(this).width($originals.eq(index).width())
		});
		return $helper;
	};

	//Make diagnosis table sortable
	$('table').on('click', function () {
		tableID = '#' + $(this).closest('table').attr('id');
		console.log(tableID)
		$(tableID + " tbody").sortable({
			helper: fixHelperModified,
			stop: function(event,ui) {renumber_table(tableID)}
		}).disableSelection();
	})



	//Delete button in table rows
	$('table').on('click','.btn-delete',function() {
		tableID = '#' + $(this).closest('table').attr('id');
		r = confirm('Delete this item?');
		if(r) {
			$(this).closest('tr').remove();
			renumber_table(tableID);
			}
	});

});

//Renumber table rows
function renumber_table(tableID) {
	$(tableID + " tr").each(function() {
		count = $(this).parent().children().index($(this));
		$(this).find('.priority').html(count);
	});
}


