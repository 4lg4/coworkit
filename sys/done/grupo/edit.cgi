#!/usr/bin/perl

$nacess = "41";
require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');
$SHOW = "grupo";


if($COD eq "" && $MODO ne "incluir")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

print $query->header({charset=>utf8});

$codigo = $COD;
$nome = "";

if($MODO ne "incluir" && $COD ne "")
	{
	$SQL = "select * from grupo where codigo = '$COD' order by codigo limit 1";
	$sth = &select($SQL);
	$rv = $sth->rows();
	while($row = $sth->fetchrow_hashref)
		{
		$codigo = $row->{'codigo'};
		$nome = $row->{'descrp'};
		$exportar = $row->{'exportar'};
		if($exportar == 1)
			{
			$wexportar = "checked";
			}
		else
			{
			$wexportar = "";
			}
		}
	}

if($LOGEMPRESA eq "1")
	{
	$sexportar = "<input type='checkbox' name='exportar' value='1' $wexportar> Permitir importação desse grupo pelos parceiros</span>";
	}


print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/CSS_syscall/form.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="/css/CSS_syscall/comum/jquery.css" type="text/css">
  
  <style>
	#sortable1, #sortable2
		{
		list-style-type: none;
		margin: 0;
		padding: 0;
		float: left;
		margin-right: 10px;
		}
	#sortable1 li, #sortable2 li
		{
		font-family: Tahoma, sans-serif;
		font-size: 13px;
		margin-bottom: 5px;
		margin-right: 10px;
		line-height: 150%;
		}
	.ui-state-default
		{
		padding-left: 10px;
		}
  </style>


  <script type="text/javascript" src="/comum/DPAC_syscall/display.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/iPAC.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery-1.4.2.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.core.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.mouse.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.sortable.js"></script>  

  <script language='JavaScript'>
	function errojx(XMLHttpRequest, textStatus, errorThrown)
		{
		top.unLoading();
		top.alerta("ERRO!<br><br>"+XMLHttpRequest+" "+textStatus+" "+errorThrown);
		}
	function clear()
		{
		document.forms[0].ADD.value = "";
		document.forms[0].PESQ.value = "";
		gopesq();
		}
	function add()
		{
		document.forms[0].ADD.value = document.forms[0].PESQ.value;
		gopesq();
		}
	function pesq()
		{
		document.forms[0].ADD.value = "";
		gopesq();
		}
	function gopesq()
		{
		order = \$('#sortable2').sortable('serialize');
		req = \$("#CAD").serialize();
		req += "&"+order;
		top.Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "items.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#sortable1").html(data);
				top.unLoading();
				},
			error: errojx
			});
		}
	function screenRefresh()
		{
		var cores = ["#dfdfdf", "#ffffff"];
		grids = getElementsByClass('navigateable');
		for(var gd=0;gd<grids.length;gd++)
			{
			linhas = grids[gd].getElementsByTagName('TR');
			for(var ln=0;ln<linhas.length;ln++)
				{
				cor_fundo = cores[ln % 2];
				linhas[ln].style.background = cor_fundo;
				}
			}
		}
	function editar()
		{
		document.forms[0].MODO.value = 'editar';
		document.forms[0].submit();
		}
	function ver()
		{
		parent.block(false);
		if(document.forms[0].COD.value == "")
			{
			top.regrid('$SHOW');
			}
		else
			{
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
			}
		}
	function imprimir()
		{
		alert('não implementado!');
		}
	function incluir()
		{
		document.forms[0].MODO.value = 'incluir';
		document.forms[0].submit();
		}
	function excluir()
		{
		action = "top.confirma('Você tem certeza que deseja excluir esse registro?<br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm()', '');";
		setTimeout(action, 250);
		}
	function excluir_confirm()
		{
		parent.block(false);
		document.forms[0].action = "del_submit.cgi";
		document.forms[0].submit();
		}
	function voltar()
		{
		top.regrid('$SHOW');
		}
	function cancelar()
		{
		top.confirma('Você tem certeza que deseja cancelar?<br>Todos os dados modificados serão perdidos!', 'top.main.ver()', '');
		}
	function salvar()
		{
		if(isNULL(document.forms[0].nome.value) == true)
			{
			erro('Você não informou o nome do grupo!', 'nome');
			return false;
			}

		var ck_items = \$('#sortable2').sortable('toArray');
		tmp_items = blk_items;
		for(f=0; f < ck_items.length; f++)
			{
			tmp_items = tmp_items.replace("##"+ck_items[f]+"##", "");
			}
		if(tmp_items.length > 0)
			{
			top.confirma('Alguns atributos já tem dados cadastros...<br><br>Confirma a exclusão desses dados?', '"top.main.salvar_reconfirm()"', '');
			}
		else
			{
			salvar_submit();
			}
		}
	function salvar_reconfirm()
		{
		top.confirma('Você tem certeza disso?<br><br>Haverá perda de dados irreversível!!!', 'top.main.salvar_del()', '');
		}
	function salvar_del()
		{
		document.forms[0].FORCE.value = 'S';
		salvar_submit();
		}
	function salvar_submit()
		{			
		order = \$('#sortable2').sortable('serialize');
		req = \$("#CAD").serialize();
		req += "&"+order;
		parent.block(false);
		$ajax_init \$.ajax({
			type: "POST",
			url: "edit_submit.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("body").html(data);
				top.unLoading();
				},
			error: errojx
			});
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
		parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
		top.ac_show(['icon_save', 'icon_cancel']);
		document.forms[0].elements[0].focus();
		\$("#sortable1, #sortable2").sortable({
				connectWith: ".connectedSortable"
				}).disableSelection();
		pesq();
		\$('input#PESQ').keypress(function(e) {
			if (e.keyCode == '13') {
				e.preventDefault();
				pesq();
				}
});
HTML
	}
else
	{
print<<HTML;
		linhas = document.body.getElementsByTagName('SELECT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].disabled=true;
			}
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			if(linhas[ln].type.toLowerCase() != 'hidden')
				{
				linhas[ln].disabled=true;
				}
			}
		linhas = document.body.getElementsByTagName('TEXTAREA');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].disabled=true;
			}
		if(blk_items.length == 0)
			{
HTML
	if($nacess_tipo eq "a")
		{
		print "top.ac_show(['icon_back','icon_edit','icon_delete']);\n";
		}
	else
		{
		print "top.ac_show(['icon_back','icon_edit']);\n";
		}
print<<HTML;
			}
		else
			{
			top.ac_show(['icon_back','icon_edit']);
			}
HTML
	}
print<<HTML;
		top.unLoading();
		}
  </script>
</head>
<body onLoad="START()" style="margin-left: 35px; overflow-x: hidden; overflow-y: auto;">

<form name='CAD' id='CAD' method='POST' action='edit.cgi' onSubmit='return false;'>

<div style='margin-bottom: 15px'>
  <dl class=form style="width: 100%; margin-top: 0px;">
	<div>
		<dt>Código</dt>
		<dd><input type='text' name='codigo' value='$codigo' style='width: 50px;' disabled><span style='margin-left: 100px'>$sexportar</dd>
	</div>
	<div>
		<dt>Nome do Grupo</dt>
		<dd><input type='text' name='nome' value='$nome' style='width: 100%'></dd>
	</div>
  <br clear=all></dl>
</div>



HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
	<div style='float: left; width: 47%; position: absolute; top: 85px; bottom: 60px; left: 30px;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Tipos disponíveis</div>
		<div style="width: 95%; padding: 5px; background-color: #31517a; -moz-border-radius: 0 5px 0 0; -webkit-border-top-right-radius: 5px; border-top-right-radius: 5px;">
			<div id='grid_pesq'>
				<table width=100% border=0 cellpadding=0 cellspacing=0>
					<tr>
						<td width=100 align='right' style='padding-right: 15px'>Tipo</td>
						<td><input type='text' name='PESQ' id='PESQ'></td>
						<td width=100><nobr><a href='javascript:pesq()'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 20px'></a><a href='javascript:clear()'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a><a href='javascript:add()'><img src='$dir{'img_syscall'}add_plus.png' border=0 alt='adicionar' style='margin-left: 6px; padding-left: 6px; border-left: inset 1px #ccccff'></a></nobr></td>
					</tr>
				</table>
			</div>
		</div>

		<div class="navigateable_box" style="width: 95%; height: 90%; overflow: hidden; background-color: white; padding: 4px; padding-bottom: 10px; -moz-border-radius: 0 0 5px 0; -webkit-border-top-right-radius: 0px; border-top-right-radius: 0px;">
			<ul id="sortable1" class="connectedSortable" style="width: 100%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
			</ul>
		</div>
	</div>

	<div style='float: right; width: 47%; position: absolute; top: 85px; bottom: 20px; left: 51%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Tipos selecionados</div>
		<div class="navigateable_box" style="width: 95%; height: 90%; overflow: hidden; background-color: white; padding: 4px; padding-bottom: 10px;">
			<ul id="sortable2" class="connectedSortable" style="width: 100%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
HTML
	}
else
	{
print<<HTML;

	<div style='float: left; width: 47%; position: absolute; top: 85px; bottom: 20px; left: 30px;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Tipos selecionados</div>
		<div class="navigateable_box" style="width: 95%; height: 90%; overflow: hidden; background-color: white; padding: 4px;">
			<ul id="sortable2" class="connectedSortable" style="width: 100%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
HTML
	}


$list_items_blocked = "";
if($COD ne "")
	{
	$SQL = "select *, grupo_item.tipo as item_cod, tipo_grupo_item.descrp as item_descr from grupo_item join tipo_grupo_item on grupo_item.tipo = tipo_grupo_item.codigo where grupo = '$COD' order by grupo_item.seq";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv < 1)
		{
		if($MODO eq "ver")
			{
			print "Nenhum tipo de item cadastrado!";
			}
		}
	else
		{
		while($row = $sth->fetchrow_hashref)
			{
			print "<li class='ui-state-default' id='item_";
			print $row->{'item_cod'};
			print "'>";

			$SQL4 = "select * from grupo_empresa where grupo = '$COD' and grupo_item = '".$row->{'item_cod'}."' ";
			$sth4 = &select($SQL4);
			$rv4 = $sth4->rows();
			if($rv4 > 0)
				{
				print "<font style='color: #31517a; font-weight: bold;'>$row->{'item_descr'}</font>";
				$list_items_blocked .= "##item_$row->{'item_cod'}##";
				}
			else
				{
				print $row->{'item_descr'};
				}
			$sth4->finish;
			print "</li>";
			}
		}
	}


print<<HTML;
			</ul>
		</div>
	</div>
	

<input type='hidden' name='ADD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='MODO' value='$MODO'>
<input type='hidden' name='FORCE' value='N'>
</form>

<script language='JavaScript'>
	blk_items = "$list_items_blocked";
</script>
</body></html>
HTML

