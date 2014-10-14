#!/usr/bin/perl

$nacess = "902";
require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');
# variável de transição de página, para saber quando voltar duas ou uma pagina por causa dos botoes de atalho no grid.
$VOLTAR = &get('VOLTAR');

if($COD eq "" && $MODO ne "incluir")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

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
# seta variaveis de controle
$nacess_user = "";
$nacess_cron = "";
if($dir{dados_user} ne "")
	{
	$sth = $dbh->prepare("select * from usuario_menu where usuario_menu.usuario = '$LOGUSUARIO' and (usuario_menu.menu = '204' or usuario_menu.menu = '205' or usuario_menu.menu = '206') ");
	$sth->execute;
	if($dbh->err ne "")
		  {
		  print $query->header({charset=>utf8});
		  &erroDBH();
		  }
	$rv = $sth->rows;
	if($rv > 0)
		{
		while($row = $sth->fetchrow_hashref)
			{
			if($row->{'menu'} eq "204")
				{
				$nacess_ti = $row->{'direito'};
				}
			if($row->{'menu'} eq "205")
				{
				$nacess_user = $row->{'direito'};
				}
			if($row->{'menu'} eq "206")
				{
				$nacess_procede = $row->{'direito'};
				}
			}
		}
	}

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/CSS_syscall/ui.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="/css/loader.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="/css/ui.css" rel="stylesheet" type="text/css">
 
  <style>
	dd, td { color: black; }
	dt { width: 20% !important; }
	dd { width: 65% !important; }
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
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery-1.4.2.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.tabs.js"></script>


  <script type="text/javascript">
	\$(document).ready(function() {
		\$('#tabs').tabs({
			select: function(event, ui) {
				if(parent.bloqueado == true)
					{
					parent.unblock();
					return false;
					}
				}
			});
		});
  </script>

  <script language='JavaScript'>
	endereco = new Array();
	cron = new Array();
	n_end = 0;
	n_cron = 0;
	function screenRefresh(x, y)
		{
		if(! y)
			{
			y=-1;
			}
		var cores = ["#fbfbfb", "#f2f2f2"];
		if(x)
			{
			var linhas = document.getElementById(x).getElementsByTagName('TR');
			}
		else
			{
			var linhas = getElementsByClass('navigateable')[0].getElementsByTagName('TR');
			}
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].className='';
			cor_fundo = cores[ln % 2];
			if(linhas[ln].id == y)
				{
				linhas[ln].style.background = "#99aec9";
				}
			else if(y == -1)
				{
				if(x.indexOf("tbcron") != -1 && ln == 1)
					{
					linhas[ln].style.background = "#99aec9";
					}
				else if(x.indexOf("tbcron") == -1 && ln == 0)
					{
					linhas[ln].style.background = "#99aec9";
					}
				else
					{
					linhas[ln].style.background = cor_fundo;
					}
				}
			else
				{
				linhas[ln].style.background = cor_fundo;
				}
			}
		}
	function orderby(g, e, o)
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			if(document.forms[0].ORDER_LISTIT.value == o)
				{
				document.forms[0].ORDER_LISTIT.value = o+" desc";
				}
			else
				{
				document.forms[0].ORDER_LISTIT.value = o;
				}
			get_cron(e);
			}
		}
	function get_cron(e)
		{
		hide('cx2_'+e);

		req = \$("#CAD_"+e).serialize();
		req += "&cod_endereco="+e;
		$ajax_init \$.ajax({
			type: "POST",
			url: "crons.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#dadoscron_"+e).html(data);
				if(\$('#tbcron_'+e+' tr:eq(1)').attr('id'))
					{
					get_detail(\$('#tbcron_'+e+' tr:eq(1)').attr('id'), e);
					document.getElementById('dadoscron_'+e).scrollTop=1;
					screenRefresh('tbcron_'+e);
					}
				top.unLoading();
				},
			error: errojx
			});
		}
	function get_detail(c, e)
		{
		req = \$("#CAD_"+e).serialize();
		req += "&cron="+c+"&cod_endereco="+e;
		top.LoadingObj("detailcron_"+e);

		$ajax_init \$.ajax({
			type: "POST",
			url: "cron_detail.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				show('cx2_'+e);
				\$("#detailcron_"+e).html(data);
				try
					{
					\$("#detailcron_"+e+" #c0").focus();
					}
				catch(err)
					{
					// modo apenas leitura
					}
				top.unLoadingObj("detailcron_"+e);
				},
			error: errojx
			});
		}
	function add_cron(e)
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			try
				{
				screenRefresh("tbcron_"+e, "0");
				}
			catch(err)
				{
				// Ignora erro
				}
			get_detail('', e);
			}
		}
	function erro(x,y)
		{
		if(y.indexOf('[') > 0)
			{
			el = y.substring(0,y.indexOf('['));
			pos = y.substring(y.indexOf('[')+1, y.indexOf(']'));
			document.getElementsByName(el)[pos].style.borderColor = 'red';
			top.alerta(x,"main.document.getElementsByName(\\""+el+"\\")["+pos+"].focus()");
			}
		else
			{
			document.getElementsByName(y)[0].style.borderColor = 'red';
			top.alerta(x,"main.document.forms[0]."+y+".focus()");
			}
		}
	function limpa(y, e)
		{
		if(y)
			{
			document.getElementsByName(y)[0].style.borderColor = '';
			}
		}
	function salvar_cron(c, e)
		{
		with(document.forms["CAD_"+e])
			{
			if(isNULL(cron_descrp.value) == true)
				{
				erro('Você não informou a descrição do monitoramento!', 'cron_descrp');
				return false;
				}
			if(isNULL(cron_tmin.value) == true)
				{
				erro('Você não informou a tempo mínimo de execução do monitoramento!', 'cron_tmin');
				return false;
				}
			else
				{
				if(! cron_tmin.value.match(/^\\d{2}:\\d{2}:\\d{2}\$/))
					{
					erro('Você não informou um valor válido para o tempo mínimo de execução!', 'cron_tmin');
					return false;
					}
				}
			if(isNULL(cron_tmax.value) == true)
				{
				erro('Você não informou a tempo máximo de execução do monitoramento!', 'cron_tmax');
				return false;
				}
			else
				{
				if(! cron_tmax.value.match(/^\\d{2}:\\d{2}:\\d{2}\$/))
					{
					erro('Você não informou um valor válido para o tempo máximo de execução!', 'cron_tmax');
					return false;
					}
				}
			}
		top.LoadingObj("detailcron_"+e);
		parent.block(false);
		req = \$("#CAD_"+e).serialize();
		req += "&ACAO=save&cron="+c+"&cod_endereco="+e;
		$ajax_init \$.ajax({
			type: "POST",
			url: "crons.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#dadoscron_"+e).html(data);
				if(c == '')
					{
					try
						{
						screenRefresh('tbcron_'+e, '0');
						}
					catch(err)
						{
						// Ignora no caso de erro
						}
					add_cron(e);
					}
				else
					{
					get_detail(c, e);
					//document.getElementById('dadoscron_'+e).scrollTop=1;
					screenRefresh('tbcron_'+e, c);
					}
				top.unLoadingObj("detailcron_"+e);
				},
			error: errojx
			});
		}
	function excluir_confirm(c, e)
		{
		top.LoadingObj("detailcron_"+e);
		// parent.block(false);
		req = \$("#CAD_"+e).serialize();
		req += "&ACAO=delete&cron="+c+"&cod_endereco="+e;
		hide('cx2_'+e);
		$ajax_init \$.ajax({
			type: "POST",
			url: "crons.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#dadoscron_"+e).html(data);
				document.getElementById('dadoscron_'+e).scrollTop=1;
				try
				      {
				      screenRefresh('tbcron_'+e, '0');
				      }
				catch(err)
				      {
				      // ignora erro
				      }
				top.unLoadingObj("detailcron_"+e);
				},
			error: errojx
			});
		}
	function excluir_cron(c, e)
		{
		top.confirma('Você tem certeza que deseja excluir este monitoramento?<br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm("'+c+'", "'+e+'")', '');
		}
	function voltar()
		{
		// teste da variável voltar
		if(\$('#VOLTAR').val()==1)
			{
			top.callRegrid('empresas');
			}
		else if(document.forms[0].COD.value == "")
			{
			top.callRegrid('empresas');
			}
		else
			{
			var variaveis =
				{
				COD : document.forms[0].COD.value,
				MODO : 'ver',
				SHOW : '$SHOW'
				};
			top.call("cad/empresa/edit.cgi",variaveis);
			}
		}
	function checkSubmit(e, g, d)
		{
		var keycode;
		if(window.event) keycode = window.event.keyCode;
		else if(e) keycode = e.which;
		else return true;
		if(keycode == 13)
			{
			if(parent.bloqueado == true)
				{
				parent.unblock();
				}
			else
				{
				get_cron(e);
				}
			}
		}
	function checkChange(b, v, d)
		{
		// b = qual o box, v = valor do input, d = valor default do input
		if(d != v)
			{
			
			show("cron_icon_save_"+b);
			show("cron_icon_cancel_"+b);
			hide("cron_icon_insert_"+b);
			hide("cron_icon_delete_"+b);
			}
		}
HTML
if($nacess_ti ne "")
	{
print<<HTML;
	function ti()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			top.Loading();
			document.forms[0].target = "_self";
			document.forms[0].action = "$dir{'dados_ti'}dados_ti.cgi";
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
			}
		}
HTML
	}
if($nacess_user ne "")
	{
print<<HTML;
	function users()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			top.Loading();
			document.forms[0].target = "_self";
			document.forms[0].action = "$dir{'dados_user'}dados_users.cgi";
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
			}
		}
	function pcs()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			top.Loading();
			document.forms[0].target = "_self";
			document.forms[0].action = "$dir{'dados_user'}dados_pc.cgi";
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
			}
		}
HTML
	}
if($nacess_procede ne "")
	{
print<<HTML;
	function procede()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			top.Loading();
			// Pega variáveis
			var variaveis =
				{
				COD : \$("#AUX input[name=COD]").val(),
				VOLTAR: 1,
				MODO : 'editar'
				};
			top.call("/cad/procede/edit.cgi",variaveis);
			}
		}
HTML
	}
print<<HTML;





















	function imprimir()
		{
		top.alerta('Não implementado!');
		}
	function limpa(y)
		{
		if(y)
			{
			document.getElementsByName(y)[0].style.borderColor = '';
			}
		}
	function START()
		{
HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
		
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
		top.ac_show(['icon_back']);
HTML
	}
print "		top.ac_show(['icon_back'";
if($nacess_ti ne "")
	{
	print ",'icon_ti'";
	}
if($nacess_user ne "")
	{
	print ",'icon_user','icon_pc'";
	}
if($nacess_procede ne "")
	{
	print ",'icon_procede'";
	}
print "]);"; # fecha funcao cria menu
print<<HTML;
		for(f=0; f<n_end; f++)
			{
			get_cron(endereco[f]);
			}
		//screenRefresh("tbcron","0");
		//screenRefresh("tbcron","0");
		// parent.block(false);
		top.unLoading();
		}

  </script>
</head>
<body onLoad="START()" style="overflow-x: hidden; overflow-y: auto;">

HTML

if($MODO eq "incluir")
	{
	$cod_emp = "";
	$nome_emp = "";
	$apelido = "";
	$obs = "";
	$tipo_emp = "J";
	$planosim = "";
	$planonao = "checked";
	}
else
	{
	$SQL = "select *, empresa.tipo as tipo_emp, empresa.codigo as cod_emp, empresa.nome as nome_emp from empresa where empresa.codigo = '$COD' order by nome limit 1";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		while($row = $sth->fetchrow_hashref)
			{
			$cod_emp = $row->{'cod_emp'};
			$nome_emp = $row->{'nome_emp'};
			$apelido = $row->{'apelido'};
			$obs = $row->{'obs'};
			$tipo_emp = $row->{'tipo_emp'};
			}
		}
	}

if($MODO eq "incluir")
	{
	$n = 0;
	$end_cod[$n] = "";
	$end_tipo[$n] = "Principal";
	$end_endereco[$n] = "";
	$end_complemento[$n] = "";
	$end_bairro[$n] = "";
	$end_cep[$n] = "";
	$end_cidade[$n] = "";
	$end_uf[$n] = "";
	$end_fone[$n] = "";
	$n++;
	}
else
	{
	$SQL = "select *, empresa_endereco.codigo as end_cod, empresa_endereco.endereco as rua, tipo_endereco.descrp as tipo_end, fones_lista.numero as telefone from empresa_endereco join tipo_endereco on empresa_endereco.tipo = tipo_endereco.codigo left join fones_lista on empresa_endereco.codigo = fones_lista.endereco where empresa_endereco.empresa = '$cod_emp' order by tipo_endereco.codigo, end_cod ";
	$sth4 = &select($SQL);
	$rv4 = $sth4->rows();
	$n = 0;
	if($rv4 > 0)
		{
		while($row4 = $sth4->fetchrow_hashref)
			{
			$end_cod[$n] = $row4->{'end_cod'};
			$end_tipo[$n] = $row4->{'tipo_end'};
			$end_endereco[$n] = $row4->{'rua'};
			$end_complemento[$n] = $row4->{'complemento'};
			$end_bairro[$n] = $row4->{'bairro'};
			$end_cep[$n] = $row4->{'cep'};
			$end_cidade[$n] = $row4->{'cidade'};
			$end_uf[$n] = $row4->{'uf'};
			$end_fone[$n] = $row4->{'telefone'};
			$n++;
			}
		}
	else
		{
		$n = 0;
		$end_cod[$n] = "";
		$end_tipo[$n] = "Principal";
		$end_endereco[$n] = "";
		$end_complemento[$n] = "";
		$end_bairro[$n] = "";
		$end_cep[$n] = "";
		$end_cidade[$n] = "";
		$end_uf[$n] = "";
		$end_fone[$n] = "";
		$n++;
		}
	}



if(scalar(@end_endereco) > 1)
	{
	print '<div id="tabs" style="clear:both; background-color:transparent;">';
	print "	<ul style='border-bottom:0px;'>\n";
	for($f=0; $f<@end_endereco; $f++)
		{
		print "		<li><a href=\"#tabs-".($f+1)."\">";
		if($end_endereco[$f] ne "" || $end_cidade[$f] ne "" || $end_uf[$f] ne "")
			{
			if($end_endereco[$f] ne "")
				{
				print $end_endereco[$f];
				}
			if($end_cidade[$f] ne "")
				{
				if($end_endereco[$f] ne "")
					{
					print " - ";
					}
				print $end_cidade[$f];
				}
			if($end_uf[$f] =~ /[a-z]/i)
				{
				if($end_endereco[$f] ne "" || $end_cidade[$f] ne "")
					{
					print " / ";
					}
				print $end_uf[$f];
				}
			}
		if($end_fone[$f] ne "")
			{
			if($end_endereco[$f] ne "" || $end_cidade[$f] ne "" || $end_uf[$f] ne "")
				{
				print " - ";
				}
			print "F.: ".$end_fone[$f];
			}
		print "</a></li>\n";
		}

	print "	</ul>\n";
	}

for($f=0; $f<@end_endereco; $f++)
	{
	if(scalar(@end_endereco) > 1)
		{
		print "	<div id=\"tabs-".($f+1)."\" style='clear: both; min-width: 800px; border: 5px solid #3167b3 !important; border-top: 30px solid #3167b3 !important; padding: 10px !important; background-color: #eee;'>";
print<<HTML;
		<div class='DTouchBoxes' style='position: absolute; top: 25px; left: 0px; right: 0px; margin-bottom: 10px; padding: 6px;'>
			<div style='width: 40%; float: left;'><span style='margin-right: 10px'>Nome:</span> $nome_emp</div>
			<div style='width: 55%; float: right;'><span style='margin-right: 10px'>Apelido:</span> $apelido</div>
			<br clear=both>
		</div><br clear=both>
HTML
		}
	else
		{
print<<HTML;
		<div class='DTouchBoxes' style='width: 99%; margin-left: 0px; margin-bottom: 10px; padding: 6px;'>
			<div style='width: 40%; float: left;'><span style='margin-right: 10px'>Nome:</span> $nome_emp</div>
			<div style='width: 55%; float: right;'><span style='margin-right: 10px'>Apelido:</span> $apelido</div>
			<br clear=both>
		</div><br clear=both>
		<div style='margin-left: -1px;'>
HTML
		}
print<<HTML;
	<form name='CAD_$end_cod[$f]' id='CAD_$end_cod[$f]' method='post' action='$dir{empresas}edit.cgi' onSubmit='return false;'>

		<input type='hidden' name='COD' value='$COD'>
		<input type='hidden' name='ID' value='$ID'>
		<input type='hidden' name='MODO' value='$MODO'>
		<input type='hidden' name='SHOW' value='empresas'>
		<input type='hidden' name='cod_empresa' value='$COD'>
		<input type='hidden' name='ORDER_LISTIT' value='codigo'>

		<div id='cx1_$end_cod[$f]' style='width: 100%; margin-right: 2%; border: solid 1px white !important;' class='DTouchBoxes'>
			<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px;'>
				<div style='float: left; margin-top: 5px;'>
					Tarefas monitoradas:
				</div>
				<div id='aba_pesq' style='float: right; width: 50%;'>
					<table width=100% border=0 cellpadding=0 cellspacing=0>
						<tr>
							<td width=70>Pesquisar:</td>
							<td><input type='text' name='PESQ' id='PESQ' onkeypress='checkSubmit(event, cron[$end_cod[$f]], "$end_cod[$f]")'></td>
							<td width=100><nobr><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { get_cron("$end_cod[$f]"); }'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 10px'></a><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { document.forms[0].PESQ$f.value=""; get_cron("$end_cod[$f]"); }'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a>
HTML
if($nacess_tipo eq "a" || $nacess_tipo eq "s")
	{
print<<HTML;
<a href='javascript:add_cron("$end_cod[$f]")'><img src='$dir{'img_syscall'}add_plus.png' border=0 alt='adicionar' style='margin-left: 6px; padding-left: 6px; border-left: inset 1px #ccccff'></a>
HTML
	}
print<<HTML;
							</nobr></td>
						</tr>
					</table>
				</div>
				<br clear=both>
			</div>
			<div id='dadoscron_$end_cod[$f]' class="navigateable_box" style="min-height: 60px; max-height: 130px; overflow-y: auto;">
				<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbcron_$end_cod[$f]' align='center'>
					<tbody>
HTML
	for($e=0; $e<15; $e++)
		{
		print "<tr><td>&nbsp;<td></tr>\n";
		}
print<<HTML;
					</tbody>
				</table>
			</div>
		</div>

		<br clear=both>

		<div id='cx2_$end_cod[$f]' style='width: 100%; margin-right: 2%; display: none; border: solid 1px white !important;' class='DTouchBoxes'>
			<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Atributos Relatório de Tarefas Automatizadas</div>
			<div id='detailcron_$end_cod[$f]' class="navigateable_box" style="position: relative; min-height: 100px; overflow-y: auto; background: url($dir{'img_syscall'}menu_fundo_actions.png) repeat-y #e5e5e5; padding-bottom: 10px;">
			</div>
		</div>


	</div>

	</form>

	<script language='JavaScript'>
		endereco[n_end] = $end_cod[$f];
		n_end++;
	</script>
HTML
	}
if(scalar(@end_endereco) > 1)
	{
	print "</div></div>";
	}
print<<HTML;

</body></html>
HTML


























