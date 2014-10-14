#!/usr/bin/perl

$nacess = "204";
require "../../cfg/init.pl";
#$COD = &get('COD');
$COD = $USER->{'empresa'};
$MODO = &get('MODO');

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
  <script>
      if(top.eos.device.get() === "mobile"){ console.log("dados ti mobile");
     //     document.getElementById("main").contentDocument.getElementById("dados_ti_body").style.width = "81%";
      }
  </script>
  
  <!-- <script type="text/javascript" src="/comum/DPAC_syscall/display.js"></script> -->
  <script type="text/javascript" src="/comum/DPAC_syscall/iPAC.js"></script>
  
  <script type="text/javascript" src="/comum/jquery/jquery-1.8.3.js"></script>
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
	grupo = new Array();
	agrupo = new Array();
	n_end = 0;
	n_grupo = 0;
	function grupoSelect(x, y)
		{
		n_grupo = 0;
		var linhas = document.getElementById(x).getElementsByTagName('TR');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].id == y)
				{
				linhas[ln].getElementsByTagName('TD')[0].style.fontWeight = "bold";
				n_grupo++;
				}
			}
		}
	function grupoNoSelect(x, y)
		{
		n_grupo = 0;
		var linhas = document.getElementById(x).getElementsByTagName('TR');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].id == y)
				{
				linhas[ln].getElementsByTagName('TD')[0].style.fontWeight = "normal";
				}
			else
				{
				if(linhas[ln].getElementsByTagName('TD')[0].style.fontWeight == "bold")
					{
					n_grupo++;
					}
				}
			}
		}
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
				if(x.indexOf("tbitem") != -1 && ln == 1)
					{
					linhas[ln].style.background = "#99aec9";
					}
				else if(x.indexOf("tbitem") == -1 && ln == 0)
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
	function orderbyemp(g, e, o)
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			if(document.forms[0].ORDER_LISTEMP.value == o)
				{
				document.forms[0].ORDER_LISTEMP.value = o+" desc";
				}
			else
				{
				document.forms[0].ORDER_LISTEMP.value = o;
				}
			get_emp(g, e);
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
			get_item(g, e);
			}
		}
	function get_agrupo(e)
		{
		hide('cx4_'+e);
		req = \$("#CAD").serialize();
		req += "&cod_endereco="+e;
		$ajax_init \$.ajax({
			type: "POST",
			url: "agrupos.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#agrupo_"+e).html(data);
				get_grupo(\$('#tbagrupo_'+e+' tr:first').attr('id'), e);
				agrupo[e]=\$('#tbagrupo_'+e+' tr:first').attr('id');
				screenRefresh('tbagrupo_'+e);
				},
			error: errojx
			});
		}
	function get_grupo(a, e)
		{
		agrupo[0] = a;
		hide('cx4_0');
		req = \$("#CAD").serialize();
		req += "&agrupo="+a+"&cod_endereco="+e+"&box=0";
		$ajax_init \$.ajax({
			type: "POST",
			url: "grupos.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#grupo_0").html(data);
				get_emp(\$('#tbgrupo_0 tr:first').attr('id'), e);
				screenRefresh('tbgrupo_0');
				},
			error: errojx
			});
		}
	function get_emp(g, e)
		{
		req = \$("#CAD").serialize();
		req += "&grupo="+g+"&cod_endereco="+e+"&box=0";
		grupo[0] = g;
		$ajax_init \$.ajax({
			type: "POST",
			url: "empresas.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#dadosemp_0").html(data);
				document.getElementById('dadosemp_0').scrollTop=1;
				},
			error: errojx
			});
		}
	function get_item(g, e, c)
		{
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
		req = \$("#CAD").serialize();
		req += "&grupo="+g+"&cod_endereco="+e+"&cod_emp="+c+"&box=0";
		grupo[0] = g;
		document.forms[0].COD.value = c;
		document.forms[0].ENDERECO.value = e;
		$ajax_init \$.ajax({
			type: "POST",
			url: "itens.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#dadosgrupo_0").html(data);
				if(\$('#tbitem_'+e+' tr:eq(1)').attr('id'))
					{
					// get_detail(\$('#tbitem_'+e+' tr:eq(1)').attr('id'), g, e);
					}
				else
					{
					hide('cx4_'+e);
					}
				document.getElementById('dadosgrupo_0').scrollTop=1;
				},
			error: errojx
			});
		}
	function get_detail_edit(l, g, e, c)
		{
		document.forms[0].MODO.value = "editar";
		get_detail_run(l, g, e, c);
		}
	function get_detail(l, g, e, c)
		{
		document.forms[0].MODO.value = "ver";
		get_detail_run(l, g, e, c);
		}	
	function get_detail_run(l, g, e, c)
		{
		if(e < 1)
			{
			return;
			}
		if(e == undefined)
			{
			e = "";
			}
		if(l == undefined)
			{
			l = "";
			}
		if(c == undefined)
			{
			c = "";
			}
		top.LoadingObj("detailgrupo_0");
		document.forms[0].COD.value = c;
		document.forms[0].ENDERECO.value = e;
		req = \$("#CAD").serialize();
		req += "&grupo="+g+"&linha="+l+"&cod_endereco="+e+"&cod_emp="+c+"&box=0";
		$ajax_init \$.ajax({
			type: "POST",
			url: "item_detail.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				show('cx4_0');
				\$("#detailgrupo_0").html(data);
				try
					{
					\$("#detailgrupo_0 #c0").focus();
					}
				catch(err)
					{
					// modo apenas leitura
					}
				top.unLoadingObj("detailgrupo_0");
				},
			error: errojx
			});
		}
	function add(e, c)
		{
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			screenRefresh("tbitem_0", "0");
			get_detail('', grupo[0], e, c);
			}
		}
	function salvar(l, g, e, c)
		{
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
		// parent.block(false);
		req = \$("#CAD").serialize();
		req += "&ACAO=save&linha="+l+"&grupo="+g+"&cod_endereco="+e+"&cod_emp="+c+"&box=0";
		$ajax_init \$.ajax({
			type: "POST",
			url: "itens.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#dadosgrupo_0").html(data);
				if(l == '')
					{
					screenRefresh('tbitem_0', '0');
					add(e, c);
					}
				else
					{
					get_detail(l, g, e, c);
					document.getElementById('dadosgrupo_0').scrollTop=1;
					screenRefresh('tbitem_0', e+'_'+l);
					}
				if(\$('#tbitem_0 tr').length > 1)
					{
					grupoSelect('tbgrupo_0', grupo[0]);
					if(n_grupo > 0)
						{
						grupoSelect('tbagrupo_0', agrupo[0]);
						}
					}
				else
					{
					grupoNoSelect('tbgrupo_0', grupo[0]);
					if(n_grupo == 0)
						{
						grupoNoSelect('tbagrupo_0', agrupo[0]);
						}
					}
				top.unLoading();
				},
			error: errojx
			});
		}
	function excluir_confirm(l, g, e, c)
		{
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
		// parent.block(false);
		req = \$("#CAD").serialize();
		req += "&ACAO=delete&linha="+l+"&grupo="+g+"&cod_endereco="+e+"&cod_emp="+c+"&box=0";
		$ajax_init \$.ajax({
			type: "POST",
			url: "itens.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				hide('cx4_0');
				\$("#dadosgrupo_0").html(data);
				document.getElementById('dadosgrupo_0').scrollTop=1;
				screenRefresh('tbitem_0', '0');
				if(\$('#tbitem_0 tr').length > 1)
					{
					grupoSelect('tbgrupo_0', grupo[0]);
					if(n_grupo > 0)
						{
						grupoSelect('tbagrupo_0', agrupo[0]);
						}
					}
				else
					{
					grupoNoSelect('tbgrupo_0', grupo[0]);
					if(n_grupo == 0)
						{
						grupoNoSelect('tbagrupo_0', agrupo[0]);
						}
					}
				top.unLoading();
				},
			error: errojx
			});
		}
	function excluir(l, g, e, c)
		{
		top.confirma('Você tem certeza que deseja excluir essa empresa?<br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm("'+l+'", "'+g+'", "'+e+'", "'+c+'")', '');
		}
	function editar()
		{
		document.forms[0].target = "_self";
		document.forms[0].action = "edit.cgi";
		document.forms[0].MODO.value = 'editar';
		document.forms[0].submit();
		}
	function ver()
		{
		// parent.block(false);
		document.forms[0].target = "_self";
		document.forms[0].action = "edit.cgi";
		document.forms[0].MODO.value = 'ver';
		document.forms[0].submit();
		}
	function cancelar()
		{
		top.confirma('Você tem certeza que deseja cancelar?<br>Todos os dados modificados serão perdidos!', 'top.main.ver()', '');
		}
	function voltar()
		{
		if(document.forms[0].COD.value == "")
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
	function checkSubmit_emp(e, g, d, c)
		{
		var keycode;
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
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
				get_emp(g, d);
				}
			}
		}
	function checkSubmit(e, g, d, c)
		{
		var keycode;
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
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
				get_item(g, d, c);
				}
			}
		}
	function checkChange(b, v, d)
		{
		// b = qual o box, v = valor do input, d = valor default do input
		if(d != v)
			{
			parent.block(true);
			\$("#detail_icon_save_"+b).show();
			\$("#detail_icon_cancel_"+b).show();
			\$("#detail_icon_insert_"+b).hide();
			\$("#detail_icon_delete_"+b).show();
			}
		}
	function START()
		{
HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
		//parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
		top.ac_show(['icon_ti_empresa']);
HTML
	}
else
	{
print<<HTML;
		top.ac_show(['icon_ti_empresa']);
HTML
	}
print<<HTML;
		get_agrupo(0);
		// parent.block(false);
		top.unLoading();
		}

  </script>
</head>
<body onLoad="START()" style="overflow-x: hidden; overflow-y: scroll;" id="dados_ti_body">

<form name='CAD' id='CAD' method='post' action='$dir{empresas}edit.cgi' onSubmit='return false;'>

<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='ENDERECO' value='0'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='ver'>
<input type='hidden' name='SHOW' value='empresas'>
<input type='hidden' name='cod_empresa' value='$COD'>
<input type='hidden' name='ORDER_LISTIT' value='linha'>
<input type='hidden' name='ORDER_LISTEMP' value='nome_emp'>

<div style='width: 49%; float: left;' class='DTouchBoxes'>
	<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px 0px;'> &nbsp; Agrupamentos</div>
	<div id='agrupo_0' class="navigateable_box" style="height: 150px; overflow-y: auto;"></div>
</div>

<div id='cx2_0' style='width: 49%; float: right;' class='DTouchBoxes'>
	<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px;'>Grupos</div>
		<div id='grupo_0' class="navigateable_box" style="height: 150px; overflow-y: auto;">
			<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbgrupo_0' align='center'>
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
<div>

	<br clear=both><br>

	<div id='cx5_0' style='width: 100%; margin-right: 2%;' class='DTouchBoxes'>
		<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px;'>
			<div style='float: left; margin-top: 5px;'>
				Empresas com dados no grupo:
			</div>
			<div id='aba_pesq' style='float: right; width: 50%;'>
				<table width=100% border=0 cellpadding=0 cellspacing=0>
					<tr>
						<td width=70>Pesquisar:</td>
						<td><input type='text' name='PESQEMP' id='PESQEMP' onkeypress='checkSubmit_emp(event, grupo[0], "0")'></td>
						<td width=70><nobr><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { get_emp(grupo[0], "0"); }'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 10px'></a><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { document.forms[0].PESQEMP.value=""; get_emp(grupo[0], "0"); }'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a></nobr></td>
					</tr>
				</table>
			</div>
			<br clear=both>
		</div>
		<div id='dadosemp_0' class="navigateable_box" style="min-height: 60px; max-height: 150px; overflow-y: auto;">
			<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbemp_0' align='center'>
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

	<br clear=both><br>

	<div id='cx3_0' style='width: 100%; margin-right: 2%;' class='DTouchBoxes'>
		<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px;'>
			<div style='float: left; margin-top: 5px;'>
				Dados do Grupo:
			</div>
			<div id='aba_pesq' style='float: right; width: 50%;'>
				<table width=100% border=0 cellpadding=0 cellspacing=0>
					<tr>
						<td width=70>Pesquisar:</td>
						<td><input type='text' name='PESQ' id='PESQ' onkeypress='checkSubmit(event, grupo[0], "0")'></td>
						<td width=100><nobr><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { get_item(grupo[0], document.forms[0].ENDERECO.value, document.forms[0].COD.value); }'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 10px'></a><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { document.forms[0].PESQ.value=""; get_item(grupo[0], document.forms[0].ENDERECO.value, document.forms[0].COD.value); }'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a><a href='javascript:add(document.forms[0].ENDERECO.value, document.forms[0].COD.value)'><img src='$dir{'img_syscall'}add_plus.png' border=0 alt='adicionar' style='margin-left: 6px; padding-left: 6px; border-left: inset 1px #ccccff'></a></nobr></td>
					</tr>
				</table>
			</div>
			<br clear=both>
		</div>
		<div id='dadosgrupo_0' class="navigateable_box" style="min-height: 60px; max-height: 150px; overflow-y: auto;">
			<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbitem_0' align='center'>
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

	<div id='cx4_0' style='width: 100%; margin-right: 2%; display: none;' class='DTouchBoxes'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Atributos - Modo Completo</div>
		<div id='detailgrupo_0' class="navigateable_box" style="position: relative; min-height: 100px; overflow-y: auto; background: url($dir{'img_syscall'}menu_fundo_actions.png) repeat-y #e5e5e5; padding-bottom: 10px;">
		</div>
	</div>

</form>

<form name='dfirewall' method='post' target='main'>
	  <input type='hidden' name='usernamefld'>
	  <input type='hidden' name='passwordfld'>
	  <input type='hidden' name='login' value='Login'>
</form>


</body></html>
HTML
