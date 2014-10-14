loadCSS("/css/relogin.css");
loadCSS("/css/login_round.css");

jQuery.ajax = (function (fn) {
    return function (options) {
        var caller = arguments.callee.caller;
        if(caller.name.indexOf('relogin')==-1 && caller.name != '')
		{
		options.caller = caller;
		lastcall(caller.name, caller.arguments);
		// alert(caller.name);
		// alert(caller.arguments);
		
		// rlastcall = options.caller;
		// options.args = caller.arguments;
		}
        return fn.apply(this, arguments);
    };
})(jQuery.ajax);

// Objeto que armazena a lista de parametros da CGI
cgikey = new Object();

// Guarda última função executada para reexecução em caso de relogon
var slastcall = "";
var blastcall = false;
function lastcall(x, a)
	{
	if(blastcall == false)
		{
		slastcall = x+"(";
		for(var i = 0, j = a.length; i < j; i++)
			{
			if(isObject(a[i]) === true)
				{
				var t = $.param(a[i]).replace(/&/g, "', ");
				t = t.replace(/=/g, ": '");
				slastcall += "{"+t+"'}, ";
				}
			else
				{
				slastcall += "'"+a[i]+"', ";
				}
			}
		slastcall = slastcall.replace(/\, $/, "");
		slastcall += ")";
		}
	}


// Funções referentes ao relogin do sistema, após um timeout de logon do usuário
function relogin(login, empresa)
	{
	// esconde todo a página e mostra apenas a tela de relogin
	$('#lightsoff').hide();
	$('#eye').hide();
	$('#menu_float').hide();
	$('#corpo').hide();
	unLoading();
	$('#relogon').show();
	$('#relogin_form input[name="password"]').val('');
	if(login != "")
		{
		$('#relogin_form input[name="username"]').val(login);
		$('#relogin_form input[name="username"]').attr('readonly', true);
		$('#relogin_form input[name="password"]').focus();
		}
	else
		{
		$('#relogin_form input[name="username"]').attr('readonly', false);
		$('#relogin_form input[name="username"]').focus();
		}
	$('#relogin_form input[name="empresa"]').val(empresa);
	}

function relogin_submit()
	{
	$('#relogin_form input[name="username"]').val($('#relogin_form input[name="username"]').val().toLowerCase());
	
	if(! $('#relogin_form input[name="username"]').val().match(/[a-z]/))
		{
		alerta("<br>Você não informou o usuário de acesso!", "$('#relogin_form input[name=username]').focus();");
		return false;
		}
	if($('#relogin_form input[name="password"]').val() == '')
		{
		alerta("<br>Você não informou a senha!", "$('#relogin_form input[name=password]').focus();");
		return false;
		}
	  
	req = "ID="+document.forms[0].ID.value;
	req += "&username="+$('#relogin_form input[name="username"]').val();
	req += "&password="+$('#relogin_form input[name="password"]').val();
	req += "&"+$.param(cgikey);
	$.ajax({
		type: "POST",
		url: "/sys/logon/relogin.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			$("#relogon_result").html(data);
			},
		error: function(XMLHttpRequest, textStatus, errorThrown)
			{
			top.alerta("ERRO!<br><br>"+XMLHttpRequest+" "+textStatus+" "+errorThrown);
			}
		});
	return false;
	}
	
function reloginoff()
	{
	$('#relogon').hide();
	$('#eye').show();
	$('#corpo').show();
	}