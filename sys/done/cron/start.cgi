#!/usr/bin/perl

$nacess = "902";
require "../../cfg/init.pl";
$SHOW = &get('SHOW');

$n=0;
for($f=29;$f>=0;$f--)
	{
	($sec[$n], $min[$n], $hora[$n], $dia[$n], $mes[$n], $ano[$n], $diaSem[$n], $yday[$n], $isdst[$n]) = localtime(time()-(86400*$f));
	$ano[$n] += 1900;
	$n++;
	}
@Smes = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro");
@wdiaSem = ('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<link rel="stylesheet" href="/css/CSS_syscall/ui.css" rel="stylesheet" type="text/css">
	<link rel="stylesheet" href="/css/loader.css" rel="stylesheet" type="text/css">
	<link rel="stylesheet" href="/css/ui.css" rel="stylesheet" type="text/css">
	
	<style>
		dd, td { color: #092772;  border-bottom: solid 1px white; }
		table tbody tr:last-child td { border: none !important; }
		th { border-bottom: solid 1px white; }
		tr { background-color: #C5C5C5; }
		/* corrige problema de scroll */
		body {
		    overflow : auto !important;
		    padding-top: 0.5%;
		    padding-bottom: 0.5%;
		    padding-right: 0.5%;
		    width: 99.5%;
		    height: 99%;
	}
	</style>
	
	<script type="text/javascript" src="/comum/DPAC_syscall/display.js"></script>
	<script type="text/javascript" src="/comum/DPAC_syscall/iPAC.js"></script>
	
	<script type="text/javascript" src="/comum/jquery/jquery-1.8.3.js"></script>
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.tabs.js"></script>

	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.datepicker.js"></script>
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.datepicker-pt-BR.js"></script>
	<script type="text/javascript" src="/comum/DPAC_syscall/tooltip.js"></script>

	<script type="text/javascript">
		var t1=null;
		var stop=0;
		var nload=0;
		var periodo="7";
		var cron="";
		var detalhe="";
		var status="all";
		var cliente="";
		
		top.Loading();

		\$(document).ready(function() {
			\$('#tabs').tabs({
				select: function(event, ui) {
					if(t1)t1.Hide(event);
					if(parent.bloqueado == true)
						{
						parent.unblock();
						return false;
						}
					//top.Loading();
					//get_analitico();
					}
				});

			\$.datepicker.setDefaults(\$.datepicker.regional["pt-BR"]);
			\$("#wdt_ini").datepicker({
					altField: '#dt_ini',
					altFormat: 'yy-mm-dd',
					dateFormat: 'dd/mm/yy',
					defaultDate: -15,
					maxDate: '-1d',
					onClose: get_analitico
				});
			\$("#wdt_fim").datepicker({
					altField: '#dt_fim',
					altFormat: 'yy-mm-dd',
					dateFormat: 'dd/mm/yy',
					maxDate: '0d',
					onClose: get_analitico
				});
			\$(".ui-datepicker").hide();
			});

		function getElementsByClass(searchClass,node,tag)
			{
			var classElements = new Array();
			if( node == null )
				{
				node = document;
				}
			if( tag == null )
				{
				tag = '*';
				}
			var els = node.getElementsByTagName(tag);
			var elsLen = els.length;
			var pattern = new RegExp('(^|\\\\s)'+searchClass+'(\\\\s|\$)');
			for(i = 0, j = 0; i < elsLen; i++)
				{
				if( pattern.test(els[i].className) )
					{
					classElements[j] = els[i];
					j++;
					}
				}
			return classElements;
			}

	function errojx(XMLHttpRequest, textStatus, errorThrown)
		{
		top.unLoading();
		top.alerta("ERRO!<br><br>"+XMLHttpRequest+" "+textStatus+" "+errorThrown);
		}

	function sleep(milliseconds)
		{
		var start = new Date().getTime();
		for(var i = 0; i < 1e7; i++)
			{
			if((new Date().getTime() - start) > milliseconds)
				{
				break;
				}
			}
		}

	function checkSubmit(e, c, d)
		{
		var keycode;
		if(window.event) keycode = window.event.keyCode;
		else if(e) keycode = e.which;
		else return true;
		if(keycode == 13)
			{
			save_status(c, d);
			t1.Hide(event);
			}
		else if(keycode == 27)
			{
			t1.Hide(event);
			icon_reset();
			}
		else if(keycode == 8 || keycode > 45)
			{
			document.forms[0].ciente.checked=1;
			}
		}

	function get_status_ok(e, c, d, m)
		{
		if(t1)
			{
			t1.Show(e,"<img src='$dir{img_syscall}/ui/cron_close.png' border=0 style='position: absolute; right: 4px; top: 0px;' onClick='t1.Hide(event); icon_reset();'><div class='box' style='text-align: center;'><span style='padding-right: 15px'>"+m+"</span></div><div id='detalhes_adc' style='height: 170px; overflow: auto;'></div><br><div class='box' style='padding-top: 4px; padding-bottom: 4px; font-size: 10px; position: absolute; bottom: 0px;' onClick='t1.Hide(event); icon_reset();'><img src='$dir{img_syscall}/sair.png' border=0 style='float: right'></div>");
			get_detail(c, d);
			}
		}

	function get_status(e, c, d, m)
		{
		if(t1)
			{
			t1.Show(e,"<img src='$dir{img_syscall}/ui/cron_close.png' border=0 style='position: absolute; right: 4px; top: 0px;' onClick='t1.Hide(event); icon_reset();'><div class='box' style='text-align: center; margin-right: 30px;'>"+m+"</div><div id='detalhes_adc' style='height: 115px; overflow: auto;'></div><div id='detalhes_form' class='box' style='font-size: 10px; position: absolute; bottom: 0px;'></div>");
			get_detail(c, d);
			}
		}

	function save_status(c, d)
		{
		if(document.forms[0].obs.value.match(/^\w+\$/) || document.forms[0].ciente.checked == 1)
			{
			top.Loading();
			req = "ID=$ID&cod="+c+"&dt="+d+"&obs="+document.forms[0].obs.value;
			if(document.forms[0].ciente.checked == 1)
				{
				icon_reset_ok();
				req += "&ciente=true";
				}
			else
				{
				icon_reset();
				req += "&ciente=false";
				}
			$ajax_init \$.ajax({
				type: "POST",
				url: "detalhes_save.cgi",
				dataType: "script",
				data: req,
				success: function(data)
					{
					\$("#"+c).html(data);
					},
				error: errojx
				});
			}
		else
			{
			icon_reset();
			}
		}

	function get_detail(c, d)
		{
		if(t1)
			{
			req = "ID=$ID&cod="+c+"&dt="+d;
			$ajax_init \$.ajax({
				type: "POST",
				url: "detalhes_form.cgi",
				dataType: "html",
				data: req,
				success: function(data)
					{
					\$("#detalhes_form").html(data);
					document.forms[0].obs.focus();
					},
				error: errojx
				});
			$ajax_init \$.ajax({
				type: "POST",
				url: "detalhes.cgi",
				dataType: "html",
				data: req,
				success: function(data)
					{
					\$("#detalhes_adc").html(data);
					},
				error: errojx
				});
			}
		}

	function get_sintetico(c, d)
		{
		nload++;
		req = "ID=$ID&cod="+c+"&dt="+d;
		$ajax_init \$.ajax({
			type: "POST",
			url: "sintetico.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#"+c).html(data);
				screenRefresh('#'+c);
				if(nload<2)
					{
					top.unLoading();
					}
				else
					{
					nload--;
					}
				},
			error: errojx
			});
		}

	function get_analitico()
		{
		top.Loading();
		req = \$("#RELAT").serialize();
		if(periodo != "")
			{
			req += "&periodo="+periodo;
			}
		if(cron != "")
			{
			req += "&cron="+cron;
			}
		if(status != "")
			{
			req += "&status="+status;
			}
		if(cliente != "")
			{
			req += "&cliente="+cliente;
			}
		$ajax_init \$.ajax({
			type: "POST",
			url: "analitico.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#analitico_resultado").html(data);
				screenRefresh('#analitico_resultado');
				shw_detalhes(detalhe);
				top.unLoading();
				},
			error: errojx
			});
		}
		
	function tableRefresh(x, y)
		{
		if(! y)
			{
			y=-1;
			}
		var cores = ["#C5C5C5", "#C5C5C5"];
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
				linhas[ln].style.background = "#5D91D9";
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

	function shw_detalhes(x, c)
		{
		if(c)
			{
			var linhas = document.getElementById(c).getElementsByTagName('TBODY');
			}
		else
			{
			var linhas = document.getElementsByTagName('TBODY');
			}
		for(var ln=0;ln<linhas.length;ln++)
			{
			id = linhas[ln].getAttribute('ID');
			if(id)
				{
				if(id.indexOf('ln_') > -1)
					{
					if(x=="resumido")
						{
						\$("#"+id).hide();
						}
					else
						{
						\$("#"+id).show();
						}
					}
				}
			}
		var linhas = document.getElementsByTagName('DIV');
		for(var ln=0;ln<linhas.length;ln++)
			{
			id = linhas[ln].getAttribute('ID');
			if(id)
				{
				if(id.indexOf('dt_') > -1)
					{
					if(x=="super")
						{
						\$("#"+id).show();
						\$("#"+id.replace("dt", "more")).hide();
						}
					else
						{
						\$("#"+id).hide();
						\$("#"+id.replace("dt", "more")).show();
						}
					}
				}
			}
		}
		
	function screenRefresh()
		{
		var cores = ["#bfbfbf", "#f2f2f2"];
		var tabelas = getElementsByClass('navigateable');
		var n=0;
		for(var t=0;t<tabelas.length;t++)
			{
			var linhas = tabelas[t].getElementsByTagName('TR');
			for(var ln=0;ln<linhas.length;ln++)
				{
				linhas[ln].className='';
				cor_fundo = cores[n];
				linhas[ln].style.background = cor_fundo;
				n++;
				if(n>1)
					{
					n=0;
					}
				}
			}
		}

	function icon_reset()
		{
		var img = document.getElementsByTagName('img');
		for(var t=0;t<img.length;t++)
			{
			if(img[t].src.indexOf("ok_clicked.png") > -1)
				{
				img[t].src = '$dir{img_syscall}/ui/ok.png';
				}
			if(img[t].src.indexOf("warning_clicked.png") > -1)
				{
				if(img[t].alt.indexOf('ok')>-1)
					{
					img[t].src = '$dir{img_syscall}/ui/warning_ok.png';
					}
				else
					{
					img[t].src = '$dir{img_syscall}/ui/warning.png';
					}
				}
			if(img[t].src.indexOf("critical_clicked.png") > -1)
				{
				if(img[t].alt.indexOf('ok')>-1)
					{
					img[t].src = '$dir{img_syscall}/ui/critical_ok.png';
					}
				else
					{
					img[t].src = '$dir{img_syscall}/ui/critical.png';
					}
				}
			if(img[t].src.indexOf("stop_clicked.png") > -1)
				{
				if(img[t].alt.indexOf('ok')>-1)
					{
					img[t].src = '$dir{img_syscall}/ui/stop_ok.png';
					}
				else
					{
					img[t].src = '$dir{img_syscall}/ui/stop.png';
					}
				}
			}
		}

	function icon_reset_ok()
		{
		var img = document.getElementsByTagName('img');
		for(var t=0;t<img.length;t++)
			{
			if(img[t].src.indexOf("ok_clicked.png") > -1)
				{
				img[t].src = '$dir{img_syscall}/ui/ok.png';
				}
			if(img[t].src.indexOf("warning_clicked.png") > -1)
				{
				img[t].src = '$dir{img_syscall}/ui/warning_ok.png';
				}
			if(img[t].src.indexOf("critical_clicked.png") > -1)
				{
				img[t].src = '$dir{img_syscall}/ui/critical_ok.png';
				}
			if(img[t].src.indexOf("stop_clicked.png") > -1)
				{
				img[t].src = '$dir{img_syscall}/ui/stop_ok.png';
				}
			}
		}

	function go_empresa(x)
		{
		top.Loading();
		document.forms[0].COD.value = x;
		document.forms[0].target = "_self";
		document.forms[0].action = "$dir{'empresas'}edit.cgi";
		document.forms[0].submit();
		}

	function START()
		{
		top.ac_show([]);
		screenRefresh();
		t1=new ToolTip('detalhes', true);
		tableRefresh('tb_cliente');
		tableRefresh('tb_periodo', '7 days');
		tableRefresh('tb_tarefas', 'all');
		tableRefresh('tb_status', 'all');
		detalhe='resumido';
		//top.unLoading();
		}
	</script>
	<style>
		a
			{
			text-decoration: none;
			}
		tr:hover
			{
			cursor: pointer;
			}
	</style>
</head>
<body onLoad='START()' style='min-width: 800px;'>

<form name='RELAT' id='RELAT' method='POST'>

<div id="tabs">
	<ul>
		<li><a href="#tabs-1">Sintético</a></li>
		<li><a href="#tabs-2">Analítico</a></li>
	</ul>

	<div id="tabs-1" style="clear: both; min-width: 800px; border: 5px solid #3167b3 !important; padding: 0px !important; background-color: #eee;">
HTML

$SQL = "select distinct empresa.codigo as cod_emp, empresa.nome as nome_emp, empresa_endereco.codigo as cod_end, empresa_endereco.endereco as end_descr, empresa_endereco.*, fones_lista.numero as telefone from cron join empresa_endereco on cron.endereco = empresa_endereco.codigo join empresa on empresa.codigo = empresa_endereco.empresa left join fones_lista on empresa_endereco.codigo = fones_lista.endereco ";
$SQL .= " where cron.hidden is false ";
$SQL .= " order by empresa.nome, empresa_endereco.endereco ";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		$endfull = $row->{'end_descr'};
		if($endfull ne "")
			{
			$endfull = "- ".$endfull;
			}
		if($endfull ne "" && $row->{'complemento'} ne "")
			{
			$endfull .= " / ";
			}
		$endfull .= $row->{'complemento'};
		if($endfull ne "" && $row->{'cidade'} ne "")
			{
			$endfull .= " - ";status
			}
		$endfull .= $row->{'cidade'};
		if($endfull ne "" && $row->{'uf'} ne "")
			{
			$endfull .= "/";
			}
		$endfull .= $row->{'uf'};
		if($row->{'telefone'} ne "")
			{
			if($endfull ne "")
				{
				$endfull .= " - ";
				}
			$endfull .=  "Telefone: ".$row->{'telefone'};
			}
print<<HTML;
	<a href='javascript:go_empresa("$row->{'cod_emp'}")'><div class='DTouchBoxes' style='width: 100%; margin-left: 0px; padding: 0px !important;'><div style='padding: 4px; padding-top: 20px;'>$row->{'nome_emp'} $endfull</div></div></a>
		<div id='$row->{'cod_emp'}'>
			<script language='Javascript'>
				get_sintetico("$row->{'cod_emp'}");
			</script>
		</div>
HTML
		}
	}
print<<HTML;
	</div>

	<div id="tabs-2" style="clear: both; min-width: 800px; border: 5px solid #3167b3 !important; border-top: 30px solid #3167b3 !important; padding: 10px !important; background-color: #eee;">
	
		
		<div style='float: left; width: 32%;  height: 117px;' class='DTouchBoxes'>
			<div class='DTouchBoxes' style='width: 40%; margin-left: 0px; padding: 8px;'>Cliente</div>
			<div class="DTouchBoxes" style="height: 75%; overflow-y: auto; overflow-x: hidden;">
				<table width=100% border=0 cellpadding=4 cellspacing=0 id="tb_cliente" class="DTouchRadio">
					<tbody>
					 
HTML
#imprime a tr Todos
print "						<tr id=\"all\" onClick=\"cliente=''; get_analitico(); tableRefresh('tb_cliente', 'all')\"><td style='border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;'>Todos</td></tr>\n";

$sth2 = &select("select distinct empresa.codigo, empresa.nome  from empresa join empresa_endereco ON empresa_endereco.empresa = empresa.codigo join cron ON cron.endereco=empresa_endereco.codigo order by nome");
$rv2 = $sth2->rows();
if($rv2 > 0)
	{
	while($row2 = $sth2->fetchrow_hashref)
		{
		print "						<tr id=\"cliente_".$row2->{'codigo'}."\" onClick=\"cliente='".$row2->{'codigo'}."'; get_analitico(); tableRefresh('tb_cliente', 'cliente_".$row2->{'codigo'}."')\"><td style='border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;'>".ucfirst($row2->{'nome'})."</td></tr>\n";
		}
	}

print<<HTML;
					 
					</tbody>
				</table>
			</div>
		</div>
		
		
		
		
		<div style='float: left; width: 25%; height: 117px; margin-left: 1%;' class='DTouchBoxes'>
			<div class='DTouchBoxes' style='width: 40%; margin-left: 0px; padding: 8px;'>Período</div>
			<div class="DTouchBoxes" style="height: 75%; overflow-y: auto; overflow-x: hidden;">
				<table width=100% border=0 cellpadding=4 cellspacing=0 id="tb_periodo" class="DTouchRadio">
					<tbody>
						<tr id="24 hours" onClick="periodo='1'; get_analitico(); tableRefresh('tb_periodo', '24 hours'); \$('#dt_range').hide();"><td style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Últimas 24 horas</td></tr>
						<tr id="7 days" onClick="periodo='7'; get_analitico(); tableRefresh('tb_periodo', '7 days'); \$('#dt_range').hide();"><td style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Última semana</td></tr>
						<tr id="30 days" onClick="periodo='30'; get_analitico(); tableRefresh('tb_periodo', '30 days'); \$('#dt_range').hide();"><td style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Último mês</td></tr>
						<tr id="range" onClick="periodo='range'; \$('#dt_range').show(); tableRefresh('tb_periodo', 'range');"><td style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Período <span id='dt_range' style='display: none; margin-left: 60px;'>de <input type='text' name='wdt_ini' id='wdt_ini' style='width: 60px; padding: 0px; text-align: center;' readonly> até <input type='text' name='wdt_fim' id='wdt_fim' style='width: 60px; padding: 0px; text-align: center;' readonly><input type='hidden' name='dt_ini' id='dt_ini'><input type='hidden' name='dt_fim' id='dt_fim'></span></td></tr>
					</tbody>
				</table>
			</div>
		</div>

		<div style='float: left; width: 20%; height: 117px; margin-left: 1%;' class='DTouchBoxes'>
			<div class='DTouchBoxes' style='width: 40%; margin-left: 0px; padding: 8px;'>Tarefas</div>
			<div class="DTouchBoxes" style="height: 75%; overflow-y: auto; overflow-x: hidden;">
				<table width=100% border=0 cellpadding=4 cellspacing=0 id="tb_tarefas" class="DTouchRadio">
					<tbody>
						<tr id="all" onClick="cron=''; get_analitico(); tableRefresh('tb_tarefas', 'all')"><td style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Todas</td></tr>
HTML

$sth2 = &select("select * from tipo_cron order by tipo_cron.descrp");
$rv2 = $sth2->rows();
if($rv2 > 0)
	{
	while($row2 = $sth2->fetchrow_hashref)
		{
		print "						<tr id=\"cron_".$row2->{'codigo'}."\" onClick=\"cron='".$row2->{'codigo'}."'; get_analitico(); tableRefresh('tb_tarefas', 'cron_".$row2->{'codigo'}."')\"><td style='border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;'>".ucfirst($row2->{'descrp'})."</td></tr>\n";
		}
	}

print<<HTML;
					</tbody>
				</table>
			</div>
		</div>
		

		
		<div style='float: left; width: 20%;  height: 117px; margin-left: 1%;' class='DTouchBoxes'>
			<div class='DTouchBoxes' style='width: 30%; margin-left: 0px; padding: 8px;'>Status</div>
			<div class="DTouchBoxes" style="height: 75%; overflow-y: auto; overflow-x: hidden;">
				<table width=100% border=0 cellpadding=4 cellspacing=0 id="tb_status" class="DTouchRadio">
					<tbody>
						<tr id="all" onClick="status='all'; get_analitico(); tableRefresh('tb_status', 'all')"><td style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Todos</td></tr>
						<tr id="ok" onClick="status='ok'; get_analitico(); tableRefresh('tb_status', 'ok')"><td  style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Concluídos com Exito</td></tr>
						<tr id="error" onClick="status='error'; get_analitico(); tableRefresh('tb_status', 'error')"><td  style="border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;">Com erro</td></tr>
						<tr id="noexec" onClick="status='noexec'; get_analitico(); tableRefresh('tb_status', 'noexec')"><td style=' border-bottom: 1px dotted #aaa; background-color: #3167b3; color: white;'>Não Executados</td></tr>
					</tbody>
				</table>
			</div>
		</div>

		<br clear=all><br>
		<div id="analitico_resultado" style="width: 98.3%">
		</div>
	</div>

</div>

<div id="detalhes" style="width: 220px; height: 230px; float: right; display: none;"></div>

<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='COD'>

</form>
</body>
</html>
HTML












