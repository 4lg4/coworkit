#!/usr/bin/perl

$nacess = "4";
require "../cfg/init.pl";

$ID = &get('ID');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	
<script language='JavaScript'>
// carrega dependencias especificas
DLoad("agenda");

// Edit DB
function chamado()
	{
	Loading();
	
	\$.ajax({
		type: "POST",
		url: "$dir{dashboard}/chamado.cgi",
		dataType: "html",
		data: \$("#CAD").serialize(),
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});	
	}

function agendaConfig()
	{
	Loading();

	\$.ajax({
		type: "POST",
		url: "$dir{dashboard}/agenda_config.cgi",
		dataType: "html",
		data: \$("#CAD").serialize(),
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});	
	}
	
function calendarRefresh(user)
	{
	Loading();
	
	if(!user)
		user = "";
	else
		user = "&USUARIO="+user;
	
	\$.ajax({
		type: "POST",
		url: "$dir{dashboard}/agenda.cgi",
		dataType: "html",
		data: \$("#CAD").serialize()+user,
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});	
	}

function calendarRefresh2()
	{
	Loading();

	\$.ajax({
		type: "POST",
		url: "$dir{dashboard}/agenda_google.cgi",
		dataType: "html",
		data: \$("#CAD").serialize(),
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});	
	}	

// troca de pagina
function dashboardChange(page)
	{
	\$(".dashboard_container").removeClass("dashboard_container_active");
	\$("#dashboard_container_"+page).addClass("dashboard_container_active");
	}
	
// quando o documento esta pronto 
\$(document).ready(function() 
	{ 
	menu_dashboard = new menu();
	menu_dashboard.btnNew("icon_dashboard_dashboard","ir","call('dashboard/edit.cgi',1)","dashboard");
	menu_dashboard.btnNew("icon_dashboard_call_ag","novo","call('chamado/edit.cgi',1)","agendam.");
	menu_dashboard.btnNew("icon_dashboard_call","novo","call('chamado/edit.cgi',1)","chamado");
	
	// cria pagina touch padrao
	\$("#DTouchPages_agenda").DTouchPages({ postFunctionRight:function(){ agendaConfig(); } });
	
	// users
	\$("#dashboard_users_container").DTouchBoxes({title:"Filtrar:"});
	
	calendarRefresh();
	// calendarRefresh2(); // google
	// unLoading();
	});
</script>
</head>
<body>

<form name='CAD' id='CAD'>

<div id="DTouchPages_agenda">
	
	<div id="DTouchPages_agenda_center">
		<div id="dashboard_calendar_container">
			<div id="dashboard_calendar"></div>
		</div>
	</div>
	
	<div id="DTouchPages_agenda_right">
		<div id="dashboard_users_container">
			<div id="dashboard_agenda_users"></div>
		</div>
	</div>
</div>

<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='ID' value='$ID'>	
	<input type='hidden' name='COD' id="COD" value='$COD'>
</form>
</body></html>
HTML


