#!/usr/bin/perl

$nacess = "66";
require "../../cfg/init.pl";
$SHOW = &get('SHOW');

$n=0;
@Smes = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro");
@wdiaSem = ('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb');

$hoje = timestamp("day").'/'.timestamp("month").'/'.timestamp("year"); # gera data corrente;
$hoje_mes = timestamp("month").'/'.timestamp("year"); # gera mes corrente;

($sec, $min, $hora, $dia, $mes, $ano, $diaSem, $yday, $isdst) = localtime(time()-(86400*(timestamp("day"))));
$ano += 1900;
$mes++;
if($mes < 10) { $mes = "0".$mes; }
if($day < 10) { $day = "0".$day; }
$last_mes_ini = '01/'.$mes.'/'.$ano; # gera mes anterior;
$last_mes_fim = $dia.'/'.$mes.'/'.$ano; # gera mes anterior;


($sec, $min, $hora, $dia, $mes, $ano, $diaSem, $yday, $isdst) = localtime(time()-(86400*7));
$ano += 1900;
$mes++;
if($mes < 10) { $mes = "0".$mes; }
if($day < 10) { $day = "0".$day; }
$last_week = $dia.'/'.$mes.'/'.$ano;

print $query->header({charset=>utf8});





# [INI]  Pega os usuários  ----------------------------------------------------------------------------------------------
	$sth = &select("select * from usuario where usuario.empresa = '$LOGEMPRESA' order by nome asc");
	$usuario_list = "<option value=''>Todos</option>";
	while($users = $sth->fetchrow_hashref)
		{
		$usuario_list .= "<option value='$users->{usuario}'>$users->{nome}</option>";
		}
# [INI]  Pega os usuparios  ---------------------------------------------------------------------------------------------


print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<script type="text/javascript" src="/comum/DPAC_syscall/DPAC.js"></script>
	<link href="/css/CSS_syscall/grid.css" rel="stylesheet" type="text/css">
	<link href="/css/CSS_syscall/comum/flexigrid.css" rel="stylesheet" type="text/css">
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.flexigrid.js"></script>

	<script type="text/javascript">
		var tam = top.document.getElementById('main').scrollHeight-60;
		var empresa_class = 2;
		var periodo = "last";
		var old_cliente_cod = "";
		var old_cliente_descrp = "";

		\$(document).ready(function() {
			\$('#tabs').tabs({
				select: function(event, ui) {
					if(parent.bloqueado == true)
						{
						parent.unblock();
						return false;
						}
					if(ui.panel.id == 'tabs-1')
						{
						top.ac_show(['icon_save']);
						}
					if(ui.panel.id == 'tabs-2')
						{
						get_hist();
						}
					if(ui.panel.id == 'tabs-3')
						{
						get_audit();
						}
					}
				});

			});

	function get_audit()
		{
HTML
if($LOGEMPRESA eq "1")
	{
print<<HTML;
		top.Loading();
		\$("#coletor_logger").hide();
		req = \$("#RELAT").serialize();
		$ajax_init \$.ajax({
			type: "POST",
			url: "auditoria.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#coletor_logger").html(data);
				if(\$("#coletor_logger_tb").height()+20 > tam)
					{
					\$("#coletor_logger").height(tam-\$("#tabs-4 table").height()-20);
					}
				else
					{
					\$("#coletor_logger").height(\$("#coletor_logger_tb").height()+25);
					}
				new grid('coletor_logger_tb');
				top.ac_show([]);
				top.unLoading();
				},
			error: errojx
			});
HTML
	}

print<<HTML;
		}

	function get_hist()
		{
		top.Loading();
		\$("#relatorio_list").hide();
		req = \$("#RELAT").serialize();
		$ajax_init \$.ajax({
			type: "POST",
			url: "historico.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#relatorio_list").html(data);
				if(\$("#relatorio_list_tb").height()+20 > tam)
					{
					\$("#relatorio_list").height(tam-\$("#tabs-3 table").height()-20);
					}
				else
					{
					\$("#relatorio_list").height(\$("#relatorio_list_tb").height()+25);
					}
				new grid('relatorio_list_tb');
				top.ac_show([]);
				top.unLoading();
				},
			error: errojx
			});
		}

	function get_preview()
		{
		req = \$("#RELAT").serialize();
		if(periodo == '7')
			{
			data_ini = "$last_week";
			data_fim = "$hoje";
			}
		else if(periodo == 'last')
			{
			data_ini = "$last_mes_ini";
			data_fim = "$last_mes_fim";
			}
		else if(periodo == 'this')
			{
			data_ini = "01/$hoje_mes";
			data_fim = "$hoje";
			}
		else if(periodo == 'range')
			{
			if(\$("#wdt_ini").val() == "")
				{
				top.alerta("Campo obrigatório no range: <br> <p style='text-align:left'>- Data Inicial</p>");
				return;
				}
			else if(\$("#wdt_fim").val() == "")
				{
				top.alerta("Campo obrigatório no range: <br> <p style='text-align:left'>- Data Final</p>");
				return;
				}
			else
				{
				data_ini = \$("#wdt_ini").val();
				data_fim = \$("#wdt_fim").val();
				}
			}
		else
			{
			top.alerta("Selecione o periodo desejado!", "top.main.document.forms[0].cliente_descrp.focus()");
			return;
			}

		if(empresa_class != 2)
			{
			// mensalistas
			if(\$("#cliente").val() == "")
				{
				top.alerta("Selecione um cliente válido!", "top.main.document.forms[0].cliente_descrp.focus()");
				return;
				}
			if(old_cliente_descrp != \$("#cliente_descrp").val())
				{
				if(old_cliente_cod == \$("#cliente").val())
					{
					top.alerta("Selecione um cliente válido!", "top.main.document.forms[0].cliente_descrp.focus()");
					return;
					}
				}
			old_cliente_cod = \$("#cliente").val();
			old_cliente_descrp = \$("#cliente_descrp").val();
			if(document.forms[0].faturado[0].checked == false && document.forms[0].faturado[1].checked == false)
				{
				top.alerta("Selecione o faturamento desejado!", "top.main.document.forms[0].faturado[0].focus()");
				return;
				}
			}
		req += "&empresa_class="+empresa_class+"&data_ini="+data_ini+"&data_fim="+data_fim;
		top.Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "preview.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				tam2 = \$("#tabs-1 table").height()+70;
  				\$("#relatorio_view").html(data);
				new grid('relatorio_list_tb');
				top.ac_show(['icon_save']);
				top.unLoading();
				},
			error: errojx
			});
		}


	function salvar()
		{
		get_preview();
		}
	function relatorioPrint(cod)
		{
		\$("#RELATORIO").val(cod);
		top.ac_show(['icon_print', 'icon_export']);
		glow('rel_'+cod, 'glow2');
		}
	function imprimir()
		{
		\$("#RELAT").attr({action:'relatorio.pdf'});
		\$("#RELAT").attr({target:'_blank'});
		\$("#RELAT").submit();
		\$("#RELAT").attr({target:'_self'});
		}
	function exportar()
		{
		\$("#RELAT").attr({action:'relatorio.xls'});
		\$("#RELAT").attr({target:'_blank'});
		\$("#RELAT").submit();
		\$("#RELAT").attr({target:'_self'});
		}
	function tableRefresh(x, y)
		{
		if(! y)
			{
			y=-1;
			}
		var cores = ["#bfbfbf", "#f2f2f2"];
		if(x)
			{
			var linhas = document.getElementById(x).getElementsByTagName('TR');
			}
		else
			{
			var linhas = getElementsByClass('navigateable')[0].getElementsByTagName('TR');
			}
		var n=0;
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].className='';
			cor_fundo = cores[n];
			if(linhas[ln].id == y)
				{
				linhas[ln].style.background = "#99aec9";
				}
			else if(y == -1)
				{
				linhas[ln].style.background = cor_fundo;
				}
			else
				{
				linhas[ln].style.background = cor_fundo;
				}
			n++;
			if(n>1)
				{
				n=0;
				}
			}
		}
	function START()
		{
		// campo do cliente
		cliente = new fieldAutoComplete("cliente", "empresa");
		cliente.setSearchField("nome");
		cliente.setSql("ativo is true ");
		cliente.setJoin("join empresa_relacionamento on empresa.codigo = empresa_relacionamento.empresa and empresa_relacionamento.relacionamento = 6");
		cliente.setOrder("nome");
		cliente.setReturnField("nome");
		cliente.setJumpNextField("tipo");
		cliente.show();

		// campo data
		data_ini = new fieldDateTime("wdt_ini","date");
		data_fim = new fieldDateTime("wdt_fim","date");

		// campo data avulsos
		data_ini = new fieldDateTime("avs_data_ini","date");
		data_fim = new fieldDateTime("avs_data_fim","date");

HTML
if($LOGEMPRESA eq "1")
	{
print<<HTML;
		// campos da auditoria
		adt_data_ini = new fieldDateTime("adt_data_ini","date");
		adt_data_fim = new fieldDateTime("adt_data_fim","date");
HTML
	}

print<<HTML;
		// campos do histórico
		hst_data_ini = new fieldDateTime("hst_data_ini","date");
		hst_data_fim = new fieldDateTime("hst_data_fim","date");

		// mostra data inicial
		\$("#wdt_fim").val("$hoje");
		\$("#wdt_ini").val("01/$hoje_mes");
		\$("#avs_data_fim").val("$hoje");
		\$("#avs_data_ini").val("01/$hoje_mes");
		\$("#adt_data_fim").val("$hoje");
		\$("#adt_data_ini").val("01/$hoje_mes");
		\$("#hst_data_fim").val("$hoje");
		\$("#hst_data_ini").val("01/$hoje_mes");

		top.ac_show(['icon_save']);
		for(f=1;f<4;f++)
			\$("#tabs-"+f).height(tam);

		tableRefresh('tb_periodo', 'last');
		tableRefresh('tb_empresa', 'selecionar_avulsosavulsos');

		top.unLoading();
		}
	</script>
	<style>
		a
			{
			text-decoration: none;
			}
	</style>
</head>
<body onLoad='START()'>

<form name='RELAT' id='RELAT' method='POST'>

<div id="tabs">
	<ul>
		<li><a href="#tabs-1">Por empresa</a></li>
		<li><a href="#tabs-2">Histórico</a></li>
HTML
if($LOGEMPRESA eq "1")
	{
print<<HTML;
		<li><a href="#tabs-3">Auditoria</a></li>
HTML
	}
print<<HTML;
	</ul>

	<div id="tabs-1" class='rounded' style='border:1px solid #959595; padding: 1em !important; background-color:#fff;'>


		<div style='float: left; width: 22%; height: 110px;'>
			<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Período</div>
			<div class="navigateable_box" style="width:103%;"  overflow: none; background-color: white; padding: 3px;">
				<table width=100% border=0 cellpadding=4 cellspacing=2 id="tb_periodo">
					<tbody>
						<tr id="7 days" onClick="periodo='7'; tableRefresh('tb_periodo', '7 days'); \$('#dt_range').hide();"><td>Últimos 7 dias</td></tr>
						<tr id="last" onClick="periodo='last'; tableRefresh('tb_periodo', 'last'); \$('#dt_range').hide();"><td>Mês passado</td></tr>
						<tr id="this" onClick="periodo='this'; tableRefresh('tb_periodo', 'this'); \$('#dt_range').hide();"><td>Esse mês</td></tr>
						<tr id="range" onClick="periodo='range'; \$('#dt_range').show(); tableRefresh('tb_periodo', 'range');"><td>Período <span id='dt_range' style='display: none; '>de <input type='text' name='wdt_ini' id='wdt_ini' style='width: 80px !important; padding: 0px !important; text-align: center;'> até <input type='text' name='wdt_fim' id='wdt_fim' style='width: 80px !important; padding: 0px !important; text-align: center;'></span></td></tr>
					</tbody>
				</table>
			</div>
		</div>

		<div style='float: left; width: 48%; height: 110px; margin-left: 2%;'>
			<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Empresa</div>
			<div class="navigateable_box" style="width: 100%;  overflow: hidden; background-color: white; padding: 4px;">
				<table width=100% border=0 cellpadding=4 cellspacing=0 id="tb_empresa">
					<tbody>
						<tr id="selecionar_avulsos" onClick="empresa_class=2; \$('#cliente_sel').hide(); \$('#servidor_inc').hide(); tableRefresh('tb_empresa', 'selecionar_avulsos')"><td colspan=2 height=25>Todos os avulsos</td></tr>
						<tr id="selecionar_cliente" onClick="empresa_class=1; \$('#cliente_sel').show(); \$('#servidor_inc').show(); tableRefresh('tb_empresa', 'selecionar_cliente');" valign=top><td width=15% height=50 rowspan=2>Selecionar cliente mensalista:<input type="hidden" name="cliente" id="cliente"></td><td height=50><span id='cliente_sel' style='display: none;'><input type="text" name="cliente_descrp" id="cliente_descrp" style="width: 95%;"></span><br>
						<span id="servidor_inc" style="display: none"><input type="radio" name="tipo" id="tipo" value="misto" checked=true style="margin-left: 50px"> Misto  <input type="radio" name="tipo" id="tipo" value='servidor' style="margin-left: 20px">Somente Horas Servidor <input type="radio" name="tipo" id="tipo" value='noservidor' style="margin-left: 20px">Sem Horas Servidor
						<span style='float: right;'><input type="checkbox" name="faturado" id="faturado" value='sim' checked> Faturado<br><input type="checkbox" name="faturado" id="faturado" value='nao' checked>  Não faturado</span></span></td></tr>
					</tbody>
				</table>
			</div>
		</div>

		<div style='float: left; width: 27%; height: 110px; margin-left: 1%;'>
			<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Observações</div>
			<div class="navigateable_box" style="width: 100%; overflow: hidden; background-color: white; padding: 4px;">
				<table width=100% height=100% border=0 cellpadding=4 cellspacing=0 id="tb_obs">
					<tbody>
						<tr><td><textarea name="obs" id="obs" style="height:100%; width:100%; border: none 0px;"></textarea></td></tr>
					</tbody>
				</table>
			</div>
		</div><br clear=both>

		<div id='relatorio_view' style="margin-top: 50px; margin-left: 25%; width: 44%;"></div>

	</div>

	<div id="tabs-2" class='rounded' style='border:1px solid #959595; padding: 1em !important; background-color:#fff;'>
			<div id='grid_pesq'>
			<table style="margin-bottom: 10px; padding: 5px; width: 420px;">
				<tr><td>
					<nobr>Data Início: <input type="text" name="hst_data_ini" id="hst_data_ini" style="margin-right:30px;"></nobr>
					<nobr>Data Fim: <input type="text" name="hst_data_fim" id="hst_data_fim"></nobr>
				<td width=10>
					<nobr><a href='javascript:get_hist()'><img src='$dir{'img'}btn_pesq.png' border=0 alt='aplicar'></a></nobr>
				</td></tr>
			</table>
		</div><br clear=both>
		<div id='relatorio_list' class="navigateable_box rounded" style="overflow-y: auto; display: none;"></div>
	</div>

HTML
if($LOGEMPRESA eq "1")
	{
print<<HTML;
	<div id="tabs-3" class='rounded' style='border:1px solid #959595; padding: 1em !important; background-color:#fff;'>
		<div id='grid_pesq'>
			<table style="margin-bottom: 10px; padding: 5px;">
				<tr><td align=right>
					<nobr>
					Data Início: <input type="text" name="adt_data_ini" id="adt_data_ini" style="margin-right:30px;">
					Data Fim: <input type="text" name="adt_data_fim" id="adt_data_fim" style="margin-right:30px;">
					Usuário: <select name="adt_usuario" id="adt_usuario">$usuario_list</select>
					</nobr>
				</td>
				<td>
					<nobr><a href='javascript:get_audit()'><img src='$dir{'img'}btn_pesq.png' border=0 alt='aplicar'></a></nobr>
				</td></tr>
			</table>
		</div><br clear=both>
		<div id='coletor_logger' class="navigateable_box rounded" style="overflow-y: auto; display: none;"></div>
	</div>
HTML
	}
print<<HTML;
</div>


<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='RELATORIO' id='RELATORIO'>
<input type='hidden' name='COD'>

</form>
</body>
</html>
HTML












