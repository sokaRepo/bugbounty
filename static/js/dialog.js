// Add modal
var dialog = document.querySelector('dialog');
var showDialogButton = document.querySelector('#show-dialog');
if (! dialog.showModal) {
	dialogPolyfill.registerDialog(dialog);
}

showDialogButton.addEventListener('click', function() {
	dialog.showModal();
	$('._dialog_overlay').css('z-index',0);
});
	 
dialog.querySelector('.close').addEventListener('click', function() {
	dialog.close();
});


function reload_list() {
	$.get("/ajax/reload", function(data) {
		$("#bounty_list").html(data);
	})
}

function add_bounty() {
	// get all elements from submited form and serialize them
	var ele = $("#addbounty-form :input").serialize();
	//
	$.post("/ajax/bugbounty/add", ele, function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			reload_list();
			$(".backdrop").hide();
			dialog.close();
			notif('success', 'Bug Bounty added');
			
		}else {
			notif('error', data.msg);
		}

	});
}

function bounty_status(id, new_status) {
	$.get("/ajax/bugbounty/"+id+"/"+new_status, function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			reload_list();
			notif('success', data.msg);
		}else {
			notif('error', data.msg)
		}
	});
}

function delete_bounty(id) {
	var r = confirm("Delete Bounty #"+id+" ?");
	if (r) {
		$.get("/ajax/bugbounty/delete/"+id, function(data) {
			
			data = jQuery.parseJSON(data);
			if (data.error == 'n') {
				reload_list();
				notif('success', data.msg);
			}else {
				notif('error', data.msg)
			}
			
			//alert("Bounty #1 deleted");
		});
	}
}



function notif(type, msg) {
	notify({

	//alert | success | error | warning | info
	type: type, 
	title: "Information",

	//custom message
	message: msg,

	position: {

	  //right | left | center
	  x: "right", 

	  //top | bottom | center
	  y: "top" 
	},


	//normal | full | small
	size: "normal", 

	overlay: false, 
	closeBtn: true, 
	overflowHide: false, 
	spacing: 20, 

	//default | dark-theme
	theme: "dark-theme", 

	//auto-hide after a timeout
	autoHide: true, 

	// timeout
	delay: 10000, 

	// callback functions
	onShow: null, 
	onClick: null, 
	onHide: null, 

	//custom template
	template: '<div class="notify"><div class="notify-text"></div></div>'

	});	
}

$("#addbounty-form").on('submit', function() {
	add_bounty();
	return false;
});
