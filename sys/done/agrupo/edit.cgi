#!/usr/bin/perl

$nacess = '42';
require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');
$SHOW = "agrupo";

print $query->header({charset=>utf8});

if(!$MODO) {
    $MODO = "incluir";
}

$codigo = $COD;
$nome = "";

if($MODO ne "incluir" && $COD ne "")
	{
	$SQL = "select * from agrupo ";
	$sth9 = &select("select * from pg_tables where tablename='agrupo'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		$SQL .= "join parceiro_agrupo on agrupo.codigo = parceiro_agrupo.agrupo and parceiro_agrupo.parceiro = '$LOGEMPRESA' ";
		}
	$SQL .= " where codigo = '$COD' order by codigo limit 1";
	$sth = &select($SQL);
	$rv = $sth->rows();
	while($row = $sth->fetchrow_hashref)
		{
		$codigo = $row->{'codigo'};
		$nome = $row->{'descrp'};
		}
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
	function getElementsByClass(searchClass,node,tag)
		{
		var classElements = new Array();
		if ( node == null )
			{
			node = document;
			}
		if ( tag == null )
			{
			tag = '*';
			}
		var els = node.getElementsByTagName(tag);
		var elsLen = els.length;
		var pattern = new RegExp('(^|\\\\s)'+searchClass+'(\\\\s|\$)');
		for (i = 0, j = 0; i < elsLen; i++)
			{
			if ( pattern.test(els[i].className) )
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
	function clear()
		{
		document.forms[0].PESQ.value = "";
		pesq();
		}
	function pesq(x)
		{
		order = \$('#sortable2').sortable('serialize');
		req = \$("#CAD").serialize();
		req += "&"+order;
		top.Loading();
		$ajax_init \$.ajax({
			type: "POST",
			url: "grupos.cgi",
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
			for(var ln=1;ln<linhas.length;ln++)
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
		top.confirma('Você tem certeza que deseja excluir esse registro?<br>Essa ação é IRREVERSÍVEL!', 'main.excluir_confirm()', '');
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
                top.\$.DDialog({
                    type : "error",
                    message : "'Você não informou o nome do agrupamento!'"
                });
			return false;
			}
			
		order = \$('#sortable2').sortable('serialize');
		req = \$("#CAD").serialize();
		req += "&"+order;
		parent.block(false);
		$ajax_init \$.ajax({
			type: "POST",
			url: "/sys/done/agrupo/edit_submit.cgi",
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
		// top.ac_show(['icon_save', 'icon_cancel']);
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
HTML
	}
print<<HTML;


		top.unLoading();
		}
  </script>
</head>
<body onLoad="START()" style="margin-left: 35px; overflow-x: hidden; overflow-y: auto;">

<form name='CAD' id='CAD' method='POST' action='edit.cgi' onSubmit='return false;'>


<div style='float: left; width: 95.5%; position: absolute; top: 15px; left: 30px; background: #3167B3; padding-bottom: 0.5%;'>
  <dl class=form style="width: 100%; margin-top: 0px;">
	<div>
		<dt style=" color:#fff;">Código</dt>
		<dd><input type='text' name='codigo' value='$codigo' style='width: 50px; font-size: 16px;' disabled></dd>
	</div>
	<div>
		<dt style=" color:#fff;">Nome do Agrupamento</dt>
		<dd><input type='text' name='nome' value='$nome' style='width: 100%; font-size: 16px;'></dd>
	</div>
  <br clear=all></dl>
</div>



HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
	<div style='float: left; width: 47%; position: absolute; top: 95px; left: 30px; background: #3167B3; padding-bottom: 0.5%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Grupos disponíveis</div>
		<div style="padding: 5px; background-color: #31517a; ">
			<div id='grid_pesq'>
				<table width=100% border=0 cellpadding=0 cellspacing=0>
					<tr>
						<td><input type='text' name='PESQ' id='PESQ' style="font-size: 16px; width: 100%;" placeholder="Pesquisar"></td>
					</tr>
				</table>
			</div>
		</div>


		<div class="navigateable_box" style="overflow: hidden; background-color: white; padding: 4px; padding-bottom: 10px; -moz-border-radius: 0 0 5px 0; -webkit-border-top-right-radius: 0px; border-top-right-radius: 0px;">
			<ul id="sortable1" class="connectedSortable" style="width: 100%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
			</ul>
		</div>
	</div>

	<div style='float: right; width: 47%; position: absolute; top: 95px; left: 51%; background: #3167B3; padding-bottom: 0.5%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Grupos selecionados</div>
		<div class="navigateable_box" style="overflow: hidden; background-color: white; padding: 4px; padding-bottom: 10px;">
			<ul id="sortable2" class="connectedSortable" style="width: 101.5%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
HTML
	}
else
	{
print<<HTML;

	<div style='float: right; width: 47%; position: absolute; top: 95px; left: 51%; background: #3167B3; padding-bottom: 0.5%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Grupos selecionados</div>
		<div class="navigateable_box" style="overflow-y: hidden; background-color: white; padding: 4px;">
			<ul id="sortable2" class="connectedSortable" style="width: 101.5%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
HTML
	}

	
if($COD ne "")
	{
	$SQL = "select *, agrupo_grupo.grupo as grupo_cod, grupo.descrp as grupo_descr from agrupo_grupo join grupo on agrupo_grupo.grupo = grupo.codigo ";
	$SQL .= " where agrupo_grupo.agrupo = '$COD' order by agrupo_grupo.seq";
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv > 0)
		{
		while($row = $sth->fetchrow_hashref)
			{
			print "<li class='ui-state-default' id='grupo_";
			print $row->{'grupo_cod'};
			print "'>";
			print $row->{'grupo_descr'};
			print "</li>";
			}
		}
	}

print<<HTML;
			</ul>
		</div>
	</div>
	

<input type='hidden' name='COD' value='$COD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='$MODO'>
</form>

<script>
/* icones v3 */
top.eos.menu.action.hideAll();
top.eos.menu.action.new({ // novo
    id       : "icon_agrupo_new",
    title    : "novo",
    subtitle : "",
    click    : function(){
    
    
        incluir();
        return true;
    
        var conteudo = \$("#PESQ").val(),
            controle = false;
        \$("#sortable1 li").each(function(){
            var valida = \$(this).text();
            if(conteudo.toLowerCase() === valida.toLowerCase()){
                controle = true;
            }
        });

    
        if(!controle) {
            incluir();
        } else {
            top.\$.DDialog({
                type : "error",
                message : "Item ["+conteudo+"] já adicionado !",
                postFunction : function(){
                    pesq();
                }
            });
        }
    }
});

top.eos.menu.action.new({ // pesquisar
    id       : "icon_agrupo_search",
    title    : "item",
    subtitle : "pesquisar",
    click    : function(){
        pesq();
    }
});

top.eos.menu.action.new({ // pesquisar
    id       : "icon_agrupo_search_clean",
    title    : "limpar",
    subtitle : "pesquisar",
    click    : function(){
        \$("#PESQ").val("");
        pesq();
    }
});
    
top.eos.menu.action.new({ // salvar
    id       : "icon_agrupo_save",
    title    : "salvar",
    subtitle : "",
    click    : function(){
        salvar();
    }
});
</script>


HTML
