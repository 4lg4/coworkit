#!/usr/bin/perl

$nacess = "2";
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
	DLoad("dashboard");

// Edit DB
function chamado()
	{
	Loading();
	
	\$.ajax({
		type: "POST",
		url: "$dir{dashboard}/chamado.cgi",
		dataType: "html",
		data: "&ID="+\$("#AUX input[name=ID]").val()+"&"+\$("#CAD").serialize(),
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});	
		
	}

// Edit DB
function dashboardTotais()
	{
	LoadingObj('dashboard_totais_container');
			
	\$.ajax({
		type: "POST",
		url: "$dir{dashboard}/totais.cgi",
		dataType: "html",
		data: "&ID="+\$("#AUX input[name=ID]").val()+"&dashboard_filter_date="+\$("#dashboard_filter_date").fieldDateTime("fieldDateTimeGetValue"),
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoadingObj();
			},
		error: errojx
		});	
		
	}

// troca de pagina
/*
function dashboardChange(page)
	{
	\$(".dashboard_container").removeClass("dashboard_container_active");
	\$("#dashboard_container_"+page).addClass("dashboard_container_active");
	}
*/
	
// quando o documento esta pronto 
\$(document).ready(function() 
	{ 
	// menu_dashboard = new menu(['icon_save','icon_cancel','icon_insert','icon_delete','icon_edit']);
	menu_dashboard = new menu();
	menu_dashboard.btnNew("icon_dashboard_agenda","ir","call('dashboard/agenda_edit.cgi',1)","agenda");
	menu_dashboard.btnNew("icon_dashboard_call_ag","novo","call('chamado/edit.cgi',1)","agendam.");
	menu_dashboard.btnNew("icon_dashboard_call","novo","call('chamado/edit.cgi',1)","chamado");
	
	// chamados
	\$("#dashboard_container_chamados_owner").DTouchBoxes({title:"ADOTE um Chamado..."});
			
	// chamados
	\$("#dashboard_container_chamados").DTouchBoxes({title:"Chamados Pendentes: Executor"});
	
	// chamados
	\$("#dashboard_container_chamados_resp").DTouchBoxes({title:"Chamados Pendentes: Responsável"});
	
	// users
	// \$("#dashboard_users_container").DTouchBoxes({title:"Abrir Chamado para:"});
	\$("#dashboard_users_container").DTouchBoxes({title:"Adicionar ENGATE para:"});
	
	// totais horas
	\$("#dashboard_totais_container").DTouchBoxes({title:"Estatisticas"});	
	
	// graficos
	\$("#dashboard_graphics").DTouchBoxes({title:"Participação equipe"});	
	
	// estatus filter (totais)
	// $R  = "<div>Período: ".&timestamp('yearmonth')."</div>";
	\$("#dashboard_filter_date").fieldDateTime(
			{ 
			type: "month-year",
			postFunction: function()
				{
				dashboardTotais();
				}
			});

	// lista de chamados		
	chamado();
	
	// estatus total dos lancamentos
	dashboardTotais();
	
	// dashboardChange("chamados");
	
	DActionEditDB();

	// unLoading();
	});
</script>
</head>
<body>

<form name='CAD' id='CAD'>

<div id="dashboard_left_container">
	<div id="dashboard_users_container">
		<div id="dashboard_users"></div>
	</div>

	<div id="dashboard_totais_container">
		<div id="dashboard_totais_filter">
			<input type="text" name="dashboard_filter_date" id="dashboard_filter_date">
		</div>
		<div id="dashboard_totais"></div>
	</div>
</div>

<div id="dashboard_right_container">
	<div id="dashboard_container_chamados_owner">
		<div id="chamados_list_container_owner"></div>
	</div>
	
	<div id="dashboard_container_chamados">
		<div id="chamados_list_container"></div>
	</div>
	
	<div id="dashboard_container_chamados_resp">
		<div id="chamados_list_container_resp"></div>
	</div>
	
	<div id="dashboard_graphics" style="overflow: auto">
		<div id="graph_user" class="dashboard_graphics"></div>
		<div id="graph_empresa" class="dashboard_graphics"></div>
	</div>
</div>


<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='COD' id="COD" value='$COD'>
</form>
</body></html>

HTML


