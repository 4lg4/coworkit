#!/usr/bin/perl

$nacess = "66";
require "../../cfg/init.pl";
$ID = &get('ID'); 
$COLETOR = &get('COLETOR'); 
$MODO = &get('MODO');

$COLETOREXTERNO = &get('COLETOREXTERNO');

print $query->header({charset=>utf8});

if($MODO eq "editar" || $MODO eq "incluir")
	{
	if($nacess_tipo ne "a" && $nacess_tipo ne "s")
		{
		$MODO = "ver";
		print "<script>top.alerta('Acesso Negado!');</script>";
		exit;
		}
	}

$nacess_rel = 0;
# Verifica se tem acesso aos relatórios do timesheet, para mostrar a quantidade de horas de cada usuário
$sth = $dbh->prepare("select * from usuario_menu where usuario_menu.usuario = '$LOGUSUARIO' and usuario_menu.menu = '66' ");
$sth->execute;
if($rv = $sth->rows > 0)
	{
	$nacess_rel = 1;
	}

# [INI]  Forma de acesso, get data from db  ------------------------------------------------------------------------------------------------------
$sth = $dbh->prepare("select * from coletor_forma order by descrp asc");
$sth->execute;
if($dbh->err ne "") {  &erroDBH($msg{db_select}." lista de formas de atendimento !!!");  &erroDBR;  exit;  } # se erro
while($forma_db = $sth->fetchrow_hashref)
	{
	$forma .= "<option value='$forma_db->{codigo}'>$forma_db->{descrp}</option>";
	}
# [END]  Forma de acesso, get data from db  ------------------------------------------------------------------------------------------------------

# [INI]  Pega todas datas com evento  ------------------------------------------------------------------------------------
	$sth = &select("select solicitante, to_char(data_exec, 'MM/DD/YYYY') as data_exec_ from coletor where coletor.parceiro = '$LOGEMPRESA' order by data_exec asc");
	$rv = $sth->rows();
	while($events = $sth->fetchrow_hashref)
		{
		$events_show  .= "{ Title: '".$events->{solicitante}."', Date: new Date('".$events->{data_exec_}."') },";
		$events_show2 .= "'".$events->{data_exec_}."',";
		}
	$events_show = substr($events_show, 0, -1); # remove ultima ,	
	$events_show2 = substr($events_show2, 0, -1); # remove ultima ,	
# [INI]  Pega todas datas com evento  ------------------------------------------------------------------------------------


$hoje = timestamp("day").'/'.timestamp("month").'/'.timestamp("year"); # gera dia inicial;

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<script type="text/javascript" src="/comum/DPAC_syscall/DPAC.js"></script>
  
<script type="text/javascript">

// quando o documento esta pronto ---------
\$(document).ready(function() 
	{
	// menut = top.menu(['icon_cancel','icon_delete','icon_save']);
	menut = new top.menu(['icon_save','icon_insert']);
	
	/*
	// se for inclusao
	if("$COLETOR" == "")
		{
		\$("#DVTipoUser").hide();
		\$("#DVColetor").css("width","100%");
		}
	// se for edicao
	else
		{
		// menut.btnShow(['icon_cancel']);
		}
	*/
		
	// Forma de atendimento,  popula select
	\$("#forma").html("$forma");
	
	// campo do cliente
	cliente = new fieldAutoComplete("cliente", "empresa");
	cliente.setSearchField("nome");
	cliente.setSql("ativo is true");
	cliente.setOrder("nome");
	cliente.setReturnField("nome");
	cliente.setJumpNextField("forma");
	cliente.show();
	
	// campo data
	data_exec = new fieldDateTime("data_exec","date-time");
	tempo_exec = new fieldDateTime("tempo_exec","time");
	tempo_faturado = new fieldDateTime("tempo_faturado","time");
	
	// inicia tabs
	\$("#coletor_tab").tabs();
	
	// inicia formulario
	resetform();
	
	// mostra data inicial
	// \$("#data_exec").val("$hoje"); 
	\$("#dia_list").text("$hoje"); 
	
	// troca tab por enter
	\$("#cliente_descrp").keydown(function(event) { if(event.which == 9) event.preventDefault(); if(event.which == 13) \$("#solicitante").focus(); }); // desativa tab e ativa enter as tab
	\$("#solicitante").keydown(function(event) { if(event.which == 13) \$("#forma").focus(); }); // ativa enter as tab too
	\$("#forma").change(function(event) { \$("#servidor").focus(); }); // desativa tab e ativa enter as tab
	\$("#servidor").keydown(function(event) { if(event.which == 13) \$("#data_exec").focus(); }); // ativa enter as tab too
	\$("#data_exec").keydown(function(event) { if(event.which == 13) \$("#tempo_exec").focus(); }); // ativa enter as tab too
	\$("#tempo_exec").keydown(function(event) { if(event.which == 13) \$("#tempo_faturado").focus(); }); // ativa enter as tab too
	\$("#tempo_exec").blur(function() { \$("#tempo_faturado").val(\$("#tempo_exec").val()); }); // ativa enter as tab too
	\$("#tempo_faturado").keydown(function(event) { if(event.which == 13) \$("#descrp").focus(); }); // ativa enter as tab too
	// \$("#descrp").keydown(function(event) { if(event.which == 13) salvar(); }); // ativa enter as tab too
	
// DATEPICKER ------------------------------------------------------------
	\$.datepicker.setDefaults(\$.datepicker.regional['pt-BR']); // set regional as PT Brasil	
	
	var events = [ $events_show ]; 
	var events2 = [ $events_show2 ]; 

	\$("#agenda").datepicker(
		{
		beforeShowDay: function(date) 
			{
			var result = [true, '', null];			
					
			var matching = \$.grep(events, function(event) {
				return event.Date.valueOf() === date.valueOf();
			});			
			
			if (matching.length) {
				result = [true, 'highlight', null];
			}
			return result;
			},
		onSelect: function(dateText) {
			var date,
				selectedDate = new Date(dateText),
				i = 0,
				event = null;
			
			while (i < events.length && !event) {
				date = events[i].Date;

				if (selectedDate.valueOf() === date.valueOf()) {
					event = events[i];
				}
				i++;
			}
			if (event) {
				// top.alerta(event.Title);
			}
		}
		});

	\$("#agenda").click(function()
		{
		var day = \$("#agenda").datepicker('getDate').getDate();
		day = day.toString();
		if(day.length == 1)
			day = "0"+day;
			
		var month = \$("#agenda").datepicker('getDate').getMonth() + 1;
		month = month.toString();
		if(month.length == 1)
			month = "0"+month;
		var year = \$("#agenda").datepicker('getDate').getFullYear();
		
		if(events2.indexOf(month+"/"+day+"/"+year) > -1)
			{
			// top.alerta(month+"/"+day+"/"+year+" Com Coletores");
			\$("#dia_list").text(day+"/"+month+"/"+year);
			coletorShowDay(year+''+month+''+day);
			
			// muda valor da data exec
			\$("#data_exec").val(day+"/"+month+"/"+year);
			}
		else
			{
			// top.alerta(month+"/"+day+"/"+year+" Sem Coletores");
			\$("#coletor_day > table > tbody").html("<tr><td colspan=7><b>Sem registro nessa data</b></td></tr>");

			// muda valor da data exec
			\$("#data_exec").val(day+"/"+month+"/"+year);
			}
		});
// DATEPICKER ------------------------------------------------------------
	
	// carrega lista de coletores
	coletor();
	
	// acesso externo direto no modo de edicao vindo pela tela de relatorio
	if("$COLETOREXTERNO" != "")
		coletorEdit("$COLETOREXTERNO");
	
	var tam = top.document.getElementById('main').scrollHeight-(\$("#DVColetor").height()+80);
	\$("#coletor_day").height(tam);
	\$("#coletor_month").height(tam);
	\$("#coletor_user").height(tam);
	\$("#coletor_empresa").height(tam);
HTML
if($nacess_rel == 1)
	{
print<<HTML;
	\$("#relatorio_usuario").height(tam);
HTML
	}
print<<HTML;
	top.unLoading(); // remove loader ---	
	});

/* Coletor ------------------------------------------------------------------------------------------------------------ */
function coletor(req)
	{
	// loading
	top.Loading();
	
	// ajusta hora servidor
	if(!\$("#servidor").attr('checked'))
		servidor = 0;
	else
		servidor = 1;
	
	// prepara post
	req += "&servidor="+servidor+"&"+\$("#CAD").serialize();
	//alert(req); // debug
	
	// executa
	$ajax_init \$.ajax(
		{
		type: "POST",
		url: "coletor.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("body").append(data);
			
			// marca coletor que esta em edicao
			if(\$("#COLETOR").val() != "")
				{
				glow('day_'+\$("#COLETOR").val(), 'glow2');
				menut.btnShow('icon_delete');
				}
				
			top.unLoading();
			},
		error: errojx
		});
	}

/* Coletor Edit ------------------------------------------------------------------------------------------------------  */
function coletorEdit(cod)
	{
	menut.btnHide("icon_edit");
	\$("#COLETOR").val(cod);
	// envia string para mostrar
	coletor("ACAO=show");
	}

/* Coletor Show Day / Month ------------------------------------------------------------------------------------------  */
function coletorShowDay(dat)
	{
	resetform();
	
	// seta variavel do dia
	\$("#SHOWDAY").val(dat);
	
	// envia string para mostrar
	coletor("&SHOWDAY="+dat);
	}

/* Coletor Edit BTN --------------------------------------------------------------------------------------------------  */
function coletorEditBtn(cod)
	{
	// resetform();
	// \$("#COLETORTMP").val(cod);
	// menut.btnShow("icon_edit");
	}

/* Excluir Coletor ----------------------------------------------------------------------------------------------------  */
function excluir(valida)
	{
	if(!valida)
		{
		top.confirma("Deseja realmente excluir ?","main.excluir(1)");
		return;
		}
		
	coletor("&ACAO=delete");
	}
	
/* Editar Coletor ----------------------------------------------------------------------------------------------------  */
function editar()
	{
	// coletorEdit(\$("#COLETORTMP").val());
	}

/* Salvar ------------------------------------------------------------------------------------------------------------  */
function salvar()
	{
	// ajusta tempo faturado
	if(\$("#tempo_faturado").val() == "")
		\$("#tempo_faturado").val(\$("#tempo_exec").val());
		
	// || \$("#solicitante").val() == ""
	if(\$("#cliente").val() == "" || \$("#cliente_descrp").val() == "" || \$("#data_exec").val() == "" || \$("#tempo_exec").val() == "" || \$("#tempo_faturado").val() == "" || \$("#descrp").val() == "")
		{
		top.alerta("Campos obrigatórios: <br> <p style='text-align:left'>- Cliente, Solicitante <br> - Forma, Data, Duração, <br> - Faturado, Descrição.</p>");
		return;
		}
	
	// envia string para salvar
	coletor("ACAO=salvar");
	}
	
/* Novo  --------------------------------------------------------------------------------------------------------------  */
function incluir()
	{
	resetform();
	}
	
/* Limpa Formulario ---------------------------------------------------------------------------------------------------  */
function resetform()
	{
	\$("#COLETOR").val("");
	\$("#cliente").val("");
	\$("#cliente_descrp").val("");
	\$("#solicitante").val("");
	\$("#data_exec").val("$hoje");
	\$("#tempo_exec").val("");
	\$("#tempo_faturado").val("");
	\$("#descrp").val("");
	\$("#forma").val("1");
	\$("#servidor").attr('checked', false);
	\$("#profissional").text("$USER->{nome}");
	}
</script>
</head>

<body style="min-width:1024px;">

<form name='CAD' id='CAD' method='post'>
<input type='hidden' name='ID' id='ID' value='$ID'>
<input type='hidden' name='COLETOR' id='COLETOR'>
<input type='hidden' name='COLETORTMP' id='COLETORTMP'>
<input type='hidden' name='SHOWDAY' id='SHOWDAY'>
<input type='hidden' name='MODO' id='MODO' value='$MODO'>

<table style="width:100%;" border=0><tr valign="top"><td style="width:17%; padding:0.5%; padding-left:0px;">
	
<!-- Agenda v v ***************************************************************************************** -->	
	<div class="rounded" style="background:#fff; width:200px; overflow:none; padding-right:5px;" align="center" valign="center">
		<span id='agenda'><span>
	</div>
	
</td>

<td id='DVColetor' style="width:80%; padding:0.5% 0 0.5% 0.5%;">
		
<!-- Coletor Formulario v v ************************************************************************************** -->			
	<div class="rounded" style='width:100%; float:left; height:199px; overflow:hidden; border: 1px solid rgb(128,128,128);'>
		
		<table style="width:97%; margin:0.5%;">
		<tr>
			<td align="right">Cliente </td>
			<td colspan="3"><input type="hidden" name="cliente" id="cliente"> 
			    <input type="text" name="cliente_descrp" id="cliente_descrp" style="width:90%;"> </td>
			<td align="right">Solicitante </td>
			<td><input type="text" name="solicitante" id="solicitante" style="width: 100%"> </td>
		</tr>
		<tr>	
			<td align="right">Forma </td>
			<td><select name="forma" id="forma" style="min-width: 250px"></select> </td>
			<td align="right">Hora Servidor </td>
			<td><input type="checkbox" name="servidor" id="servidor"> </td>
			<td colspan="2">Profissional: <span id="profissional"></span></td>
		</tr>
		<tr>
			<td align="right">Data </td>	
			<td><input type="text" name="data_exec" id="data_exec"> </td>
			<td align="right">Duração </td>
			<td><input type="text" name="tempo_exec" id="tempo_exec"> </td>
			<td align="right">Faturado </td>
			<td><input type="text" name="tempo_faturado" id="tempo_faturado"> </td>
		</tr>	
		<tr>
			<td align="right" valign="top">Descrição </td>
			<td colspan="5"><textarea name="descrp" id="descrp" style="height:90px; width: 100%;"></textarea> </td>
		</tr>
		</table>
		
	</div>	
	
</td></tr></table>

	<!-- Tabs das coletores -->
	<div style='width: 100%;'>		
		<div id="coletor_tab" style="clear:both; top:0px;" align="right" >
			<ul style='border-bottom:0px;'>
				<li style='margin-top: 2px'><a href="#tabs-0">Dia <b id="dia_list" style="font-size:10px;"></b></a></li>				
				<li style='margin-top: 2px'><a href="#tabs-1">Mês</a></li>
				<li style='margin-top: 2px'><a href="#tabs-2">Total Minhas Horas Mês <span id="total_mes"></a></li>
				<li style='margin-top: 2px'><a href="#tabs-3">Total Clientes <span id="total_cliente"></a></a> </li>
HTML
if($nacess_rel == 1)
	{
print<<HTML;
				<li style='margin-top: 2px;'><a href="#tabs-4">Total Funcionários </a></li>
HTML
	}
print<<HTML;
			</ul>

			<!-- Coletores da solicitacao DIA -->
			<div id="tabs-0" style='min-height:200px;'>
				<div id='coletor_day' class="navigateable_box rounded_u" style="height:310px; overflow-y: auto;"></div>
			</div>
			
			<!-- Coletores da solicitacao MES -->
			<div id="tabs-1" style='min-height:200px;'>
				<div id='coletor_month' class="navigateable_box rounded_u" style="height:300px; overflow-y: auto;"></div>
			</div>

			<!-- Coletores da solicitacao MES por usuário -->
			<div id="tabs-2" style='min-height:200px;'>
				<div id='coletor_user' class="navigateable_box rounded_u" style="height:300px; overflow-y: auto;"></div>
			</div>

			<!-- Coletores da solicitacao MES por cliente -->
			<div id="tabs-3" style='min-height:200px;'>
				<div id='coletor_empresa' class="navigateable_box rounded_u" style="height:300px; overflow-y: auto;"></div>
			</div>

HTML
if($nacess_rel == 1)
	{
print<<HTML;
			<!-- Coletores da solicitacao MES por usuario -->
			<div id="tabs-4" style='min-height:200px;'>
				<div id='relatorio_usuario' class="navigateable_box rounded_u" style="height:300px; overflow-y: auto; text-align:left;"></div>
			</div>
HTML
	}
print<<HTML;
		</div>
	<br clear=both>
	</div>
</form>


</body></html>
HTML
