#!/usr/bin/perl

$nacess = "204";
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
$nacess_ti = "";
$nacess_cron = "";
if($dir{dados_ti} ne "" || $dir{cron} ne "")
	{
	$sth = $dbh->prepare("select * from usuario_menu where usuario_menu.usuario = '$LOGUSUARIO' and (usuario_menu.menu = '204' or usuario_menu.menu = '206' or usuario_menu.menu = '902') ");
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
			if($row->{'menu'} eq "206")
				{
				$nacess_procede = $row->{'direito'};
				}
			if($row->{'menu'} eq "902")
				{
				$nacess_cron = $row->{'direito'};
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
	dd, td
		{
		color: black;
		}
	dt
		{
		width: 40% !important;
		}
	dd
		{
		width: 55% !important;
		}
	dd textarea
		{
		width: 100% !important;
		padding-left: 20px;
		}
	dd select
		{
		width: 100% !important;
		}
	#listpcuser, #listpcusersel
		{
		list-style-type: none;
		margin: 0;
		padding: 0;
		float: left;
		}
	#listpcuser li, #listpcusersel li
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
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery-1.4.4.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.core.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.mouse.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.draggable.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.sortable.js"></script>

  <script language='JavaScript'>
	endereco = new Array();
	grupo = new Array();
	n_end = 0;
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
				if(x.indexOf("tblistpc") != -1 && ln == 1)
					{
					linhas[ln].style.background = "#99aec9";
					}
				else if(x.indexOf("tblistpc") == -1 && ln == 0)
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
	function get_pc()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			req = \$("#CAD").serialize();
			$ajax_init \$.ajax({
				type: "POST",
				url: "listpc.cgi",
				dataType: "html",
				data: req,
				success: function(data)
					{
					\$("#listpc").html(data);
					if(document.forms[0].comp_selected.value != "")
						{
						get_pcdetail(document.forms[0].comp_selected.value);
						screenRefresh('tblistpc', document.forms[0].comp_selected.value);
						}
					else
						{
						try
							{
							if(\$('#tblistpc tr:eq(1)').attr('id'))
								{
								get_pcdetail(\$('#tblistpc tr:eq(1)').attr('id'));
	 							screenRefresh('tblistpc', \$('#tblistpc tr:eq(1)').attr('id'));
								}
							}
						catch(err)
							{
							// add_pc();
							}
						}
					top.unLoading();
					},
				error: errojx
				});
			}
		}
	function get_pcdetail(d, s)
		{
		if(d == undefined)
			{
			d = "";
			}
			
		\$('#bbottom').show();
		if(d=="")
			{
			\$('#rboth').hide();
			}
		else
			{
			\$('#rboth').show();
			}
		req = \$("#CAD").serialize();
		req += "&qual="+d;
		top.LoadingObj('bbottom');
		if(s == undefined)
			{
			top.LoadingObj('rtop');
			top.LoadingObj('rbottom');
			}
		$ajax_init \$.ajax({
			type: "POST",
			url: "pc_detail.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#detailpc").html(data);
				try
					{
					\$("#detailpc #c0").focus();
					}
				catch(err)
					{
					// modo apenas leitura
					}
				get_pcusersel();
				\$("#detailpc").height('400');
				\$("#detailpc").height(document.getElementById("detailpc").scrollHeight+10);
				top.unLoadingObj('bbottom');
				},
			error: errojx
			});
		}
	function orderby(q, o)
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			if(q == 'listpc')
				{
				if(document.forms[0].ORDER_LISTPC.value == o)
					{
					document.forms[0].ORDER_LISTPC.value = o+" desc";
					}
				else
					{
					document.forms[0].ORDER_LISTPC.value = o;
					}
				get_pc();
				}
			}
		}
	function get_pcuser()
		{
		req = \$("#CAD").serialize();
		$ajax_init \$.ajax({
			type: "POST",
			url: "listpcuser.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#listpcuser").html(data);
				top.unLoadingObj('rtop');
				},
			error: errojx
			});
		}
	function get_pcusersel(q)
		{
		req = \$("#CAD").serialize();
		if(q != undefined)
			{
			req += q;
			}
		req += "&selected=true",
		$ajax_init \$.ajax({
			type: "POST",
			url: "listpcuser.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#listpcusersel").html(data);
				get_pcuser();
				top.unLoadingObj('rbottom');
				},
			error: errojx
			});
		}
	function add_pc()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			try
				{
				screenRefresh("tblistpc", "0");
				get_pcdetail('');
				}
			catch(err)
				{
				get_pcdetail('');
				}
			}
		}
	function salvar_pc(d)
		{
		if(\$("#CAD input[name=comp_nome]").val() == "" && \$("#CAD input[name=comp_dtag]").val() == "")
			{
			if(\$('[name*=COMP_ITEM_VALOR][value!=""]').length < 1)
				{
				top.alerta('Você não preencheu nenhum dado!', 'top.main.document.getElementById("c0").focus()');
				return false;
				}
			}
		req = \$("#CAD").serialize();
		req += "&ACAO=save&qual="+d;
		top.LoadingObj('bbottom');
		$ajax_init \$.ajax({
			type: "POST",
			url: "listpc.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				parent.block(false);
				\$("#listpc").html(data);
				if(d == '')
					{
					screenRefresh('tblistpc', '0');
					add_pc();
					}
				else
					{
					try
						{
						get_pcdetail(document.forms[0].comp_selected.value, true);
						screenRefresh('tblistpc', document.forms[0].comp_selected.value);
						}
					catch(err)
						{
						get_pcdetail(\$('#tblistpc tr:last').attr('id'), true);
						document.getElementById('listpc').scrollTop=document.getElementById('listpc').scrollHeight-20;
						screenRefresh('tblistpc', \$('#tblistpc tr:last').attr('id'));
						}
					}
				top.unLoadingObj('bbottom');
				},
			error: errojx
			});
		}
	function excluir_confirm_pc(d)
		{
		req = \$("#CAD").serialize();
		req += "&ACAO=delete&qual="+d;
		top.Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "listpc.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				parent.block(false);
				\$('#detailpc').html("");
				\$("#listpc").html(data);
				screenRefresh('tblistpc', '0');
				\$('#bbottom').hide();
				\$('#rboth').hide();
				top.unLoading();
				},
			error: errojx
			});
		}
	function excluir_pc(d)
		{
		top.confirma('Você tem certeza que deseja excluir esse computador?<br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm_pc("'+d+'")', '');
		}
	function voltar()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			if(\$('#VOLTAR').val()==1)
				{
				top.callRegrid('empresas');
				}
			else
				{
				var variaveis =
					{
					COD : '$COD',
					MODO : 'ver',
					SHOW : '$SHOW'
					};
				top.call("empresa/edit.cgi",variaveis);
				}
			}
		}// fim da função voltar
	function checkSubmit(q, e)
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
				if(q == "get_pc")
					{
					get_pc();
					}
				else if(q == "get_pcuser")
					{
					get_pcuser();
					}
				else
					{
					alert(q);
					}
				}
			}
		}

	function checkChange(q, e, v)
		{
		var keycode;
		if(window.event) keycode = window.event.keyCode;
		else if(e) keycode = e.which;
		else return true;
		if(keycode == 13)
			{
			if(q == "get_pc")
				{
				hide("pc_icon_save");
				salvar_user(v);
				}
			}
		else if(keycode == 8 || keycode > 45)
			{
			parent.block(true);
			if(q == "get_pc")
				{
				show("pc_icon_save");
				show("pc_icon_cancel");
				hide("pc_icon_insert");
				hide("pc_icon_delete");
				}
			}
		}

	function checkChange(b, v, d)
		{
		// b = qual o box, v = valor do input, d = valor default do input
		if(d != v)
			{
			parent.block(true);
			show(b+"_icon_save");
			show(b+"_icon_cancel");
			hide(b+"_icon_insert");
			hide(b+"_icon_delete");
			}
		}

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
			document.forms[0].action = "$dir{'dados_ti'}dados_users.cgi";
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
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
if($nacess_cron ne "")
	{
print<<HTML;
	function cron()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			top.Loading();
			document.forms[0].target = "_self";
			document.forms[0].action = "$dir{'cron'}dados_cron.cgi";
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
HTML
	}
print "		top.ac_show(['icon_back','icon_user'";
if($nacess_ti ne "")
	{
	print ",'icon_ti'";
	}
if($nacess_cron ne "")
	{
	print ",'icon_cron'";
	}
if($nacess_procede ne "")
	{
	print ",'icon_procede'";
	}
print "]);"; # fecha funcao cria menu
print<<HTML;
		get_pc();
		get_pcusersel();

		\$("#listpcuser, #listpcusersel").sortable({
			helper: 'clone',
			connectWith: '.connectedSortable',
			items: "tr:not(.state-disabled)",
			}).disableSelection();
		\$("#listpcuser").sortable({
			receive: function(event, ui)
				{
				\$("#listpcuser").html((\$("#listpcuser").html()).replace(/<\\/tbody><\\/table>/, "")+"</tbody></table>");
				top.LoadingObj('rtop');
				order = \$('#listpcusersel').sortable('serialize');
				get_pcusersel("&del="+ui.item.attr('ID')+"&"+order);
				}
			});
		\$("#listpcusersel").sortable({
			update: function(event, ui)
				{
				\$("#listpcusersel").html((\$("#listpcusersel").html()).replace(/<\\/tbody><\\/table>/, "")+"</tbody></table>");
				top.LoadingObj('rbottom');
				order = \$('#listpcusersel').sortable('serialize');
				get_pcusersel("&add="+ui.item.attr('ID')+"&"+order);
				}
			});
		top.unLoading();
		}

  </script>
</head>
<body onLoad="START()" style="overflow-x: hidden; overflow-y: auto;">

<form name='CAD' id='CAD' method='post' action='$dir{empresas}edit.cgi' onSubmit='return false;'>

<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='$MODO'>
<input type='hidden' name='SHOW' value='empresas'>
<input type='hidden' name='cod_empresa' value='$COD'>
<input type='hidden' name='ORDER_LISTPC' value='dtag'>
<input type='hidden' name='ORDER_LISTUSER' value='nome'>
<input type='hidden' name='VOLTAR' id='VOLTAR' value='$VOLTAR'>

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
	$SQL = "select *, empresa.tipo as tipo_emp, empresa.codigo as cod_emp, empresa.nome as nome_emp, case when plano.codigo is not null then 'S' else 'N' end as tem_plano  from empresa left join plano on empresa.codigo = plano.empresa where empresa.codigo = '$COD' order by nome limit 1";
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
			$planosim = "";
			$planonao = "";
			if($row->{'tem_plano'} eq "S")
				{
				$planosim = "checked";
				}
			else
				{
				$planonao = "checked";
				}
			}
		}
	}

$SQL = "select * from empresa_tipo order by descrp";
$sth2 = &select($SQL);
$rv2 = $sth2->rows();
$tipo_emp_list = "";
if($rv2 < 1)
	{
	$tipo_emp_list .= "<option value=''>Nenhum tipo de cadastrado</option>";
	}
else
	{
	while($row2 = $sth2->fetchrow_hashref)
		{
		$tipo_emp_list .= "<option value='$row2->{'codigo'}'";
		if($row2->{'codigo'} eq $tipo_emp)
		      {
		      $tipo_emp_list .= " selected ";
		      }
		$tipo_emp_list .= ">$row2->{'descrp'}</option>";
		}
	}

if($MODO eq "incluir")
	{
	$SQL = "select *, tipo_doc.codigo as cod_doc, tipo_doc.minidescrp as tipo_doc from tipo_doc where tipo_doc.empresa_tipo = '$tipo_emp' ";
	}
else
	{
	$SQL = "select *, tipo_doc.codigo as cod_doc, tipo_doc.minidescrp as tipo_doc, empresa_doc.descrp as empresa_doc from empresa_doc right join tipo_doc on empresa_doc.doc = tipo_doc.codigo and empresa_doc.empresa = '$cod_emp' where tipo_doc.empresa_tipo = '$tipo_emp' ";
	}
$sth3 = &select($SQL);
$rv3 = $sth3->rows();
$n = 0;
if($rv3 > 0)
	{
	while($row3 = $sth3->fetchrow_hashref)
		{
		$cdoc[$n] = $row3->{'cod_doc'};
		$tdoc[$n] = $row3->{'tipo_doc'};
		$doc[$n] = $row3->{'empresa_doc'};
		$n++;
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
	$end_prob[$n] = "";
	$n++;
	}
else
	{
	$SQL = "select *, empresa_endereco.codigo as end_cod, empresa_endereco.endereco as rua, tipo_endereco.descrp as tipo_end, endereco_particularidades.descrp as problemas from empresa_endereco join tipo_endereco on empresa_endereco.tipo = tipo_endereco.codigo left join endereco_particularidades on empresa_endereco.codigo = endereco_particularidades.endereco where empresa_endereco.empresa = '$cod_emp' order by tipo_endereco.codigo, end_cod ";
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
			$end_prob[$n] = $row4->{'problemas'};
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
		$end_prob[$n] = "";
		$n++;
		}
	}


$n = 0;
$SQL = "select * from uf order by codigo";
$sth5 = &select($SQL);
$rv5 = $sth5->rows();
if($rv5 < 1)
	{
	$tipo_ufcod[$n] = "";
	$tipo_uf[$n] = "Nenhum estado cadastrado";
	}
else
	{
	while($row5 = $sth5->fetchrow_hashref)
		{
		$tipo_ufcod[$n] = $row5->{'codigo'};
		$tipo_uf[$n] = $row5->{'descrp'};
		$n++;
		}
	}

$n = 0;
$SQL = "select * from tipo_endereco order by codigo";
$sth5 = &select($SQL);
$rv5 = $sth5->rows();
if($rv5 < 1)
	{
	$tipo_endcod[$n] = "";
	$tipo_end[$n] = "Nenhum tipo de endereço cadastrado";
	}
else
	{
	while($row5 = $sth5->fetchrow_hashref)
		{
		$tipo_endcod[$n] = $row5->{'codigo'};
		$tipo_end[$n] = $row5->{'descrp'};
		$n++;
		}
	}

$n = 0;
$SQL = "select * from tipo_contato order by codigo";
$sth7 = &select($SQL);
$rv7 = $sth7->rows();
if($rv7 < 1)
	{
	$tipo_contcod[$n] = "";
	$tipo_cont[$n] = "Nenhum tipo de contato cadastrado";
	}
else
	{
	while($row7 = $sth7->fetchrow_hashref)
		{
		$tipo_contcod[$n] = $row7->{'codigo'};
		$tipo_cont[$n] = $row7->{'descrp'};
		$n++;
		}
	}


print<<HTML;

<div id='mensagem'>

</div>

<div class='DTouchBoxes' style='width: 99%; margin-left: 0px; margin-bottom: 10px; padding: 6px;'>
	<div style='width: 40%; float: left;'><span style='margin-right: 10px'>Nome:</span> $nome_emp</div>
	<div style='width: 55%; float: right'><span style='margin-right: 10px'>Apelido:</span> $apelido</div>
	<br clear=both>
</div>


<div id='cx2_1' style='width: 100%; margin-right: 2%;' class='DTouchBoxes'>
	<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px;'>
		<div style='float: left; margin-top: 5px;'>Computadores (total: <span id="total_itens">0</span>)</div>
		<div id='aba_pesq' style='float: right; width: 50%;'>
			<table width=100% border=0 cellpadding=0 cellspacing=0>
				<tr>
					<td width=70>Pesquisar:</td>
					<td><input type='text' name='PESQ_PC' id='PESQ_PC' onkeypress='checkSubmit("get_pc", event)'></td>
					<td width=100><nobr><a href='javascript:get_pc()'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 30px'></a><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { document.forms[0].PESQ_PC.value=""; get_pc(); }'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a><a href='javascript:add_pc()'><img src='$dir{'img_syscall'}add_plus.png' border=0 alt='adicionar' style='margin-left: 6px; padding-left: 6px; border-left: inset 1px #ccccff'></a></nobr></td>
				</tr>
			</table>
		</div>
		<br clear=both>
	</div>
	<div id='listpc' class="navigateable_box" style="min-height: 60px; max-height: 150px; overflow-y: auto;"></div>
</div>
<br clear=both>

<div id='bbottom' style='float: left; width: 50%; position: relative;'>

	<div class='DTouchBoxes' style='margin: 0px !important; padding: 8px !important; padding-bottom: 14px !important;'>
		<div style='float: left; padding-bottom: 14px;'>Atributos Completo</div><br clear=both>
		<div id='detailpc' style="position: relative; min-height: 100px; overflow-y: auto; background: url($dir{'img_syscall'}menu_fundo_actions.png) repeat-y #e5e5e5; border: none 0px;"></div>
	</div>
</div>
	
<div id='rboth' style='width: 48%; float: right; padding: 0px; margin: 0px; padding: 0px;'>
	<div id='rtop' style='position: relative; padding: 0px;'>
		<div id='cx2_3' style='float: left; width: 100%; padding: 0px'>
			<div class='DTouchBoxes' style='padding: 0px 2px'>
				<div class='fake_aba' style='width: 90%; margin-left: 0px; padding: 5px;'>
					<div style='float: left; margin-top: 5px;'>Usuários Disponíveis</div>
					<div id='aba_pesq' style='float: right; width: 60%;'>
						<table width=100% border=0 cellpadding=0 cellspacing=0>
							<tr>
								<td width=70>Pesquisar:</td>
								<td><input type='text' name='PESQ_PCUSER' id='PESQ_PCUSER' onkeypress='checkSubmit("get_pcuser", event)'></td>
								<td width=50><nobr><a href='javascript:get_pcuser()'><img src='$dir{'img_syscall'}btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 30px'></a> <a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { document.forms[0].PESQ_PCUSER.value=""; get_pcuser(); }'> <img src='$dir{'img_syscall'}btn_limpar.png' border=0 alt='limpar'></a></nobr></td>
							</tr>
						</table>
					</div><br clear=both>
				</div>
				<div class="navigateable_box" style="height: 195px; overflow: hidden; padding-right: 10px;">
					<ul id="listpcuser" class="connectedSortable" style="width: 100%; height: 100%; padding: 4px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 2px;"></ul>
				</div><br clear=both>
			</div>
		</div><br clear=both>
	</div>
	
	<center> <img src='$dir{'img_syscall'}sort_asc.png' border=0 alt='/\' style='margin: 4px'> <img src='$dir{'img_syscall'}sort_desc.png' border=0 alt='\/' style='margin: 4px'> </cemter>
	
	
	<div id='rbottom' style='height: 265px; position: relative;'>		
		<div id='cx2_4' style='float: left; width: 100%; height: 195px; padding: 0px;'>
			<div class='DTouchBoxes' style='padding: 0px 3px'>
				<div class='fake_aba' style='width: 70%; float: left; margin-left: 0px; padding: 5px; padding-bottom: 10px;'>
					<div style='float: left; margin-top: 5px;'>Usuários selecionados</div><br clear=both>
				</div><br clear=both>
				<div class="navigateable_box" style="height: 195px; overflow: hidden; padding-right: 10px;">
					<ul id="listpcusersel" class="connectedSortable" style="width: 100%; height: 100%; padding: 4px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
				</div><br clear=both>
			</div>
		</div><br clear=both>
	</div>
</div><br clear=both>


</form>

</body></html>
HTML
