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
		id = $(this).closest(".btn-delete").attr('id')
		if(r) {
			$(this).closest('tr').remove();
			renumber_table(tableID);
			delete_sas_program(id);
			}
	});

});

//Renumber table rows
function renumber_table(tableID) {
	data = Array();
	$(tableID + " tr").each(function () {
		count = $(this).parent().children().index($(this));
		$(this).find('.priority').html(count);
		data.push({
			"order_number": count,
			"id": $(this).find('.priority').attr('id')
		});
	});
	console.log(data.slice(1));
	change_order(JSON.stringify(data.slice(1)));
}


delete_sas_program = async (sas_program_id) => {
	url = "http://"+location.host+"/sas_program/delete/" + sas_program_id + "/";
	let csrftoken = getCookie('csrftoken');
	await fetch(url, {
		method: 'DELETE',
		headers: {
        	'Content-Type': 'application/json',
			'X-Requested-With': 'XMLHttpRequest',
        	"X-CSRFToken": csrftoken
		}
	}).then(response => console.log("Deleted"))
		.catch((error => console.log(error)))

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

change_order = async (data) => {
	url = "http://" + location.host + "/sas_program/change_order/";
	let csrftoken = getCookie('csrftoken');
	await fetch(url, {
		method: 'POST',
		body: data,
		headers: {
			'Content-Type': 'application/json',
			'X-Requested-With': 'XMLHttpRequest',
        	"X-CSRFToken": csrftoken
		}
	}).then(response => console.log("Changed"))
		.catch((error => console.log(error)))
}