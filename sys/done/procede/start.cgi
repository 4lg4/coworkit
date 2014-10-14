#!/usr/bin/perl


$nacess = "206";
require "../../cfg/init.pl";


$COD = &get('COD');
$MODO = &get('MODO');
# variável de transição de página, para saber quando voltar duas ou uma pagina por causa dos botoes de atalho no grid.
$VOLTAR = &get('VOLTAR');

#para acesso direto
# $COD=82;
# $MODO="ver";

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
$nacess_user = "";
$nacess_cron = "";
if($dir{dados_ti} ne "" || $dir{dados_user} ne "" || $dir{dados_cron} ne "")
	{
	$sth = $dbh->prepare("select * from usuario_menu where usuario_menu.usuario = '$LOGUSUARIO' and (usuario_menu.menu = '204' or usuario_menu.menu = '205' or usuario_menu.menu = '206' or usuario_menu.menu = '902') ");
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
	dd, td { color: black; }
  </style>

  <script type="text/javascript" src="/comum/DPAC_syscall/iPAC.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery-1.4.2.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.tabs.js"></script>


  <link rel="stylesheet" href="/css/CSS_syscall/form.css" rel="stylesheet" type="text/css">
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.ui.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.ui.timepicker.js"></script>

  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.meiomask.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/dtips.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.validate.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/tiny_mce/jquery.tinymce.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/tiny_mce/tiny_mce.js"></script>

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
	procede = new Array();
	descricao_vlr = new Array();
	n_end = 0;
	n_procede = 0;
	function screenRefresh(x, y)
		{
		if(! y)
			{
			y=-1;
			}
		var cores = ["#fbfbfb", "#f2f2f2"];
		if(x)
			{
			try
				{
				var linhas = document.getElementById(x).getElementsByTagName('TR');
				}
			catch(err)
				{
				var linhas = new Array();
				}
			}
		else
			{

			try
				{
				var linhas = getElementsByClass('navigateable')[0].getElementsByTagName('TR');
				}
			catch(err)
				{
				var linhas = new Array();
				}
			}
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].className='';
			cor_fundo = cores[ln % 2];
			if(linhas[ln].id == y)
				{
				linhas[ln].style.background = "#99aec9";
				}
			else
				{
				linhas[ln].style.background = cor_fundo;
				}
			}
		}
	function orderby(e, o)
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
			get_lista(e);
			}
		}
	function get_lista(e)
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			req = \$("#CAD").serialize();
			req += "&cod_endereco="+e;
			$ajax_init \$.ajax({
				type: "POST",
				url: "lista.cgi",
				dataType: "html",
				data: req,
				success: function(data)
					{
					\$("#listaprocede_"+e).html(data);
					if(procede[e] != "")
						{
						screenRefresh('tbitem_'+e, procede[e]);
						}
					else
						{
						screenRefresh('tbitem_'+e, '0');
						}
					top.unLoading();
					},
				error: errojx
				});
			}
		}
	function get_detail(l, e, c)
		{
		// l = código procedimento, e = código endereço, c = código empresa
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			if(l == undefined)
				{
				l = "";
				}
			if(e == undefined)
				{
				e = "";
				}
			if(c == undefined)
				{
				c = document.forms[0].COD.value;
				}
			req = \$("#CAD").serialize();
			req += "&procede="+l+"&cod_endereco="+e;

			if(l)
				{
				screenRefresh('tbitem_'+e, l);
				}
			procede[e]=l;
			top.Loading();

			$ajax_init \$.ajax({
				type: "POST",
				url: "procede_detail.cgi",
				dataType: "html",
				data: req,
				success: function(data)
					{
					show('cx2_'+e);
					\$("#detailprocede_"+e).html(data);
					try
						{
						\$("#detailprocede_"+e+" #c0").focus();
						}
					catch(err)
						{
						// modo apenas leitura
						}

					// inicializa a caixa de editor      
					\$('#descricao_'+e).tinymce(
						  {
						  // detecta se houve alteração no campo 
						  setup : function(ed) {
							  ed.onKeyUp.add(function(ed, ev) {
								  checkChange(e, ed.getContent(), "+descricao_vlr[e]+");
								  });
							  },

						  // General options
						  theme : "advanced",
						  skin : "o2k7",
						  skin_variant : "black",
						  plugins : "inlinepopups,fullscreen,print,table",
						  theme_advanced_buttons1 : "code,|,fullscreen,|,print,|,undo,redo,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect,|,search,replace,|,forecolor,backcolor,|,bullist,numlist,|,|,tablecontrols,|,link,unlink,image",
						  theme_advanced_buttons2 : "",
						  theme_advanced_buttons3 : "",
						  theme_advanced_toolbar_location : "top",
						  theme_advanced_toolbar_align : "left",
						  theme_advanced_resizing : false,
						  force_br_newlines : true,
						  force_p_newlines : false,
						  forced_root_block : '',

						  // Example content CSS (should be your site CSS)
						  content_css : "css/content.css",

						  // Drop lists for link/image/media/template dialogs
						  template_external_list_url : "lists/template_list.js",
						  external_link_list_url : "lists/link_list.js",
						  external_image_list_url : "lists/image_list.js",
						  media_external_list_url : "lists/media_list.js",
						  });

					// parent.block(false);
					top.unLoading();
					\$("#titulo_"+e).focus();
					},
				error: errojx
				});
			}
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
			get_detail('', e, c);
			}
		}
	function salvar(l, e, c)
		{
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
		// parent.block(false);
		req = \$("#CAD").serialize();
		req += "&ACAO=save&cod_endereco="+e;
		top.Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "lista.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("#listaprocede_"+e).html(data);
				if(l == '')
					{
					screenRefresh('tbitem_'+e, '0');
					add(e, c);
					}
				else
					{
					get_detail(l, e, c);
					document.getElementById('listaprocede_'+e).scrollTop=1;
					screenRefresh('tbitem_'+e, l);
					top.unLoading();
					}
				},
			error: errojx
			});
		}
	function excluir_confirm(l, e, c)
		{
		if(c == undefined)
			{
			c = document.forms[0].COD.value;
			}
		// parent.block(false);
		req = \$("#CAD").serialize();
		req += "&ACAO=delete&procede="+l+"&cod_endereco="+e;
		$ajax_init \$.ajax({
			type: "POST",
			url: "lista.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				hide('cx2_'+e);
				\$("#listaprocede_"+e).html(data);
				document.getElementById('listaprocede_'+e).scrollTop=1;
				screenRefresh('tbitem_'+e, '0');
				top.unLoading();
				},
			error: errojx
			});
		}
	function excluir(l, e, c)
		{
		top.confirma('Você tem certeza que deseja excluir esse procedimento?<br><br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm("'+l+'", "'+e+'", "'+c+'")', '');
		}
	function editar()
		{
		document.forms[0].target = "_self";
		document.forms[0].action = "start.cgi";
		document.forms[0].MODO.value = 'editar';
		document.forms[0].submit();
		}
	function ver()
		{
		// parent.block(false);
		document.forms[0].target = "_self";
		document.forms[0].action = "start.cgi";
		if(document.forms[0].COD.value == "")
			{
			top.regrid('empresas');
			}
		else
			{
			document.forms[0].MODO.value = 'ver';
			document.forms[0].submit();
			}
		}
	function cancelar()
		{
		top.confirma('Você tem certeza que deseja cancelar?<br>Todos os dados modificados serão perdidos!', 'top.main.ver()', '');
		}
	function voltar()
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			// teste da variável voltar
			if(\$('#VOLTAR').val()==1)
				{
				top.callGrid('empresas');
				}
			else if(document.forms[0].COD.value == "")
				{
				top.callGrid('empresas');
				}
			else
				{
				if(document.forms[0].MODO.value == 'ver')
					{
					var variaveis =
							{
							COD : document.forms[0].COD.value,
							MODO : "ver"
							};
							
					top.call("cad/empresa/edit.cgi",variaveis);
					return true;
					}
				else
					{
					top.callGrid('empresas');
					}
				
				}
			}
		}
	function pesq(e)
		{
		if(parent.bloqueado == true)
			{
			parent.unblock();
			}
		else
			{
			hide('cx2_'+e);
			procede[e]="";
			get_lista(e);
			}
		}
	function checkSubmit(e, d)
		{
		// e = event, d = endereco
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
				pesq(d);
				}
			}
		}
	function checkChange(b, v, d)
		{
		// b = qual o box, v = valor do input, d = valor default do input
		if(d != v)
			{
			// parent.block(true);
			show("detail_icon_save_"+b);
			show("detail_icon_cancel_"+b);
			hide("detail_icon_insert_"+b);
			hide("detail_icon_delete_"+b);
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
HTML
	}
print<<HTML;
	function START()
		{
		// parent.block(false);
HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
		//// parent.block(true);
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			}
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
if($nacess_cron ne "")
	{
	print ",'icon_cron'";
	}
print "]);"; # fecha funcao cria menu
print<<HTML;  
		for(f=0; f<n_end; f++)
			{
			get_lista(endereco[f]);
			}
		top.unLoading();
		}

  </script>
</head>
<body onLoad="START()">

<form name='CAD' id='CAD' method='post' action='$dir{empresas}edit.cgi' onSubmit='return false;'>

<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='$MODO'>
<input type='hidden' name='SHOW' value='empresas'>
<input type='hidden' name='cod_empresa' value='$COD'>
<input type='hidden' name='ORDER_LISTIT' value='titulo'>
<input type='hidden' id='VOLTAR' name='VOLTAR' value='$VOLTAR'>


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
	$SQL = "select ee.codigo AS end_cod , ee.endereco AS rua, et.descrp AS tipo_end, ee.*  
	from empresa_endereco AS ee join empresas_lista_distinct AS ed on ed.emp_codigo=ee.empresa
	join tipo_endereco AS et on et.codigo=ee.tipo where empresa='$cod_emp' order by et.codigo, ee.codigo";
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

print<<HTML;

<div class='DTouchBoxes' style='width: 99%; margin-left: 0px; margin-bottom: 10px; padding: 5px;'>
	<div style='width: 55%; float: left;'><span style='margin-right: 10px'>Nome:</span> $nome_emp</div>
	<div style='width: 40%; float: right'><span style='margin-right: 10px'>Apelido:</span> $apelido</div>
	<br clear=both>
</div>


<div id="tabs" style="clear:both; background-color:transparent;">
HTML

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


for($f=0; $f<@end_endereco; $f++)
	{
	print "	<div id=\"tabs-".($f+1)."\" class='rounded' style='clear: both; min-width: 800px; border:1px solid #959595; padding: 1em !important; background-color:#fff;'>";
print<<HTML;

		<div id='cx1_$end_cod[$f]' style='width: 100%; margin-right: 2%;' class='DTouchBoxes'>
			<div class='fake_aba' style='width: 70%; margin-left: 0px; padding: 5px;'>
				<div style='float: left; margin-top: 5px;'>
					Lista de Procedimentos:
				</div>
				<div id='aba_pesq' style='float: right; width: 50%;'>
					<table width=100% border=0 cellpadding=0 cellspacing=0>
						<tr>
							<td width=70>Pesquisar:</td>
							<td><input type='text' name='PESQ_$end_cod[$f]' id='PESQ_$end_cod[$f]' maxlength='200' onkeypress='checkSubmit(event, "$end_cod[$f]")'></td>
							<td width=100><nobr><a href='javascript:pesq("$end_cod[$f]")'><img src='/img/syscall/btn_pesq.png' border=0 alt='pesquisar' style='margin-left: 10px'></a><a href='javascript:if(parent.bloqueado == true) { parent.unblock(); } else { document.forms[0].PESQ_$end_cod[$f].value=""; get_lista("$end_cod[$f]"); }'> <img src='/img/syscall/btn_limpar.png' border=0 alt='limpar'></a><a href='javascript:add("$end_cod[$f]")'><img src='/img/syscall/add_plus.png' border=0 alt='adicionar' style='margin-left: 6px; padding-left: 6px; border-left: inset 1px #ccccff'></a></nobr></td>
						</tr>
					</table>
				</div>
				<br clear=both>
			</div>
			<div id='listaprocede_$end_cod[$f]' class="navigateable_box" style="min-height: 100px; max-height: 150px; overflow-y: auto;">
				<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbitem_$end_cod[$f]' align='center'>
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

		<div id='cx2_$end_cod[$f]' style='width: 100%; margin-right: 2%; display: none; position: relative;' class='DTouchBoxes'>
			<div id='detailprocede_$end_cod[$f]' style="width: 98%; overflow: hidden"></div>
		</div>


	</div>
	<script language='JavaScript'>
		endereco[n_end] = $end_cod[$f];
		n_end++;
	</script>
HTML
	}
print '</div></form></body></html>';
