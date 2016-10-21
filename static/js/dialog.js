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



$("#addbounty-form").on('submit', function() {
	add_bounty();
	return false;
});



var dialog_edit = document.querySelector('#edit-dialog');
	var showDialogButton = $('.show-edit_dialog');
	if (! dialog_edit.showModal) {
		dialogPolyfill.registerDialog(dialog_edit);
	}


	showDialogButton.on('click', function() {

		//dialog_edit.showModal();
		//$('._dialog_overlay').css('z-index',0);
		//console.log("Value: " + showDialogButton.attr('v'));
		//edit_bounty(showDialogButton.attr('v'));
		//edit_entry($("#table"), )
	});
		
	dialog_edit.querySelector('.close').addEventListener('click', function() {
		dialog_edit.close();
});

/*
var dialog_edit_target = document.querySelector('#edittarget-dialog');
	var showDialogButton = $('.show-edit_dialog');
	if (! dialog_edit_target.showModal) {
		dialogPolyfill.registerDialog(dialog_edit_target);
	}


	showDialogButton.on('click', function() {
		dialog_edit_target.showModal();
		$('._dialog_overlay').css('z-index',0);
		console.log("Value: " + showDialogButton.attr('v'));
		edit_bounty(showDialogButton.attr('v'));
	});
		
	dialog_edit_target.querySelector('.close').addEventListener('click', function() {
		dialog_edit_target.close();
});
*/

function show_dialog(dialog) {
	$("#"+dialog).show();
}

function reload_list(type) {
	$.get("/ajax/"+ type +"/reload", function(data) {
		$("#content_page").html(data);
	})
}

function login() {
	var ele = $("#login-form :input").serialize();
	$.post("/ajax/login", ele, function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			document.location.href="/";
		}else {
			notif('error', data.msg);
		}
	});
}

function logout() {
	
	$.get("/ajax/logout", function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			document.location.href="/";
		}else {
			notif('error', data.msg);
		}
	});
}

function add_entry(table) {
	// get all elements from submited form and serialize them
	if (table == 'bounties')
		var ele = $("#addbounty-form :input").serialize();
	else if (table == 'targets')
		var ele = $("#addtarget-form :input").serialize();
	else return;
	//
	$.post("/ajax/"+ table +"/add", ele, function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			reload_list( (table=='bounties') ? 'bounty' : 'target' );
			$(".backdrop").hide();
			dialog.close();
			notif('success', data.msg);
			
		}else {
			notif('error', data.msg);
		}

	});
}

function edit_entry_dialog(table, id) {
	dialog_edit.showModal();
	$('._dialog_overlay').css('z-index',0);
	$.get("/ajax/"+table+"/show/"+id, function(data) {
		// get entry info
		var d = jQuery.parseJSON(data);
		if (table == 'bounties') {
			$("#bountyid").val(d.id);
			// Set option as selected
			$("#evuln").val(d.vuln);
			$("#ereward").val(d.award);
			if (d.status == 'close')
				$("#estatus").val('closed');
			else
				$("#estatus").val('open');
			$("#etitle").val(d.title);
			$("#edescription").html(d.description);
		}
		else if(table == 'targets') {
			$("#targetid").val(d.id);
			$("#epriority").val(d.priority);
			$("#etitle").val(d.title);
			$("#edescription").html(d.description);
		}
		else return;

	});

}

function edit_entry(table) {
	if (table == 'bounties')
		var ele = $("#editbounty-form :input").serialize();
	else if (table == 'targets')
		var ele = $("#edittarget-form :input").serialize();
	//
	$.post("/ajax/"+table+"/edit", ele, function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			reload_list( (table == 'bounties' ? 'bounty' : 'target') );
			$(".backdrop").hide();
			dialog_edit.close();
			notif('success', 'Entry edited');
			
		}else {
			notif('error', data.msg);
		}

	});
}

function bounty_status(id, new_status) {
	$.get("/ajax/bugbounty/"+id+"/"+new_status, function(data) {
		data = jQuery.parseJSON(data);
		if (data.error == 'n') {
			reload_list('bounty');
			notif('success', data.msg);
		}else {
			notif('error', data.msg)
		}
	});
}

function delete_entry(table, id) {
	var r = confirm("Delete entry #"+id+" from "+ table +"  ?");
	if (r) {
		$.get("/ajax/"+table+"/delete/"+id, function(data) {
			
			data = jQuery.parseJSON(data);
			if (data.error == 'n') {
				reload_list((table=='bounties') ? 'bounty' : 'target');
				notif('success', data.msg);
			}else {
				notif('error', data.msg)
			}
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


$("#addtarget-form").on('submit', function() {
	add_entry('targets');
	return false;
});

$("#editbounty-form").on('submit', function() {
	edit_entry('bounties');
	return false;
});


$("#edittarget-form").on('submit', function() {
	edit_entry('targets');
	return false;
});
