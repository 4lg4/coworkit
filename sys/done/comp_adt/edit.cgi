#!/usr/bin/perl

# $nacess = '404';
$nacess = "27";
require "../../cfg/init.pl";
$SHOW = "empresa_comp_adicional";
$MODO = &get('MODO');
if($MODO eq "")
	{
	$MODO = "editar";
	}

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/CSS_syscall/form.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="/css/jquery.css" type="text/css">
  
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

  <script type="text/javascript" src="/comum/display.js"></script>
  <script type="text/javascript" src="/comum/iPAC.js"></script>
  <script type="text/javascript" src="/comum/jquery/jquery-1.6.4.js"></script>
  <script type="text/javascript" src="/comum/jquery/jquery-ui-1.8.18.custom.min.js"></script>
   
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
		document.forms[0].MODO.value = 'ver';
		document.forms[0].submit();
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
		top.START('force');
		}
	function cancelar()
		{
		top.confirma('Você tem certeza que deseja cancelar?<br>Todos os dados modificados serão perdidos!', 'top.main.ver()', '');
		}
	function salvar()
		{
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
		action = "top.confirma('Você tem certeza disso?<br><br>Haverá perda de dados irreversível!!!', 'top.main.salvar_del()', '');";
		setTimeout(action, 250);
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
            
            /* icones v3 */  
            top.eos.menu.action.new({ // novo
                id       : "icon_comp_adt_new",
                title    : "adicio.",
                subtitle : "item",
                click    : function(){
                
                    var conteudo = \$("#PESQ").val(),
                        controle = false;
                    \$("#sortable1 li").each(function(){
                        var valida = \$(this).text();
                        if(conteudo.toLowerCase() === valida.toLowerCase()){
                            controle = true;
                        }
                    });
            
                
                    if(!controle) {
                        add();
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
                id       : "icon_comp_adt_search",
                title    : "item",
                subtitle : "pesquisar",
                click    : function(){
                    pesq();
                }
            });
        
            top.eos.menu.action.new({ // pesquisar
                id       : "icon_comp_adt_search_clean",
                title    : "limpar",
                subtitle : "pesquisar",
                click    : function(){
                    \$("#PESQ").val("");
                    pesq();
                }
            });
                
            top.eos.menu.action.new({ // salvar
                id       : "icon_comp_adt_save",
                title    : "salvar",
                subtitle : "",
                click    : function(){
                    salvar();
                }
            });
            
            
            
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
	# print "top.ac_show(['icon_back','icon_edit'";
	# print "]);\n";
	}
print<<HTML;
		top.unLoading();
		}
  </script>
</head>
<body onLoad="START()" style="margin-left: 35px; overflow-x: hidden; overflow-y: auto;">

<form name='CAD' id='CAD' method='POST' action='edit.cgi' onSubmit='return false;'>

HTML
if($MODO eq "editar" || $MODO eq "incluir")
	{
print<<HTML;
	<div style='float: left; width: 47%; position: absolute; top: 2%; left: 30px; background: #3167B3; padding-bottom: 0.5%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Atributos disponíveis</div>
		<div style="padding: 5px; background-color: #31517a; -moz-border-radius: 0 5px 5px 5px; -webkit-border-top-right-radius: 5px; border-top-right-radius: 5px;">
			<div id='grid_pesq'>
				<table width=100% border=0 cellpadding=0 cellspacing=0>
					<tr>
						<td><input type='text' name='PESQ' id='PESQ' style="font-size: 16px; width: 100%;" placeholder="Pesquisar / Adicionar"></td>
					</tr>
				</table>
			</div>
		</div>


		<div class="navigateable_box" style="height: 90%; overflow-x: hidden; overflow-y: hidden; background-color: white; padding: 4px; padding-bottom: 10px; -moz-border-radius: 0 0px 5px 5px; -webkit-border-top-right-radius: 0px; border-top-right-radius: 0px;">
            <ul id="sortable1" class="connectedSortable" style="width: 99.5%; height: 99.5%; padding: 0px; overflow-y: auto; border: none 0px; margin: 1%;">
			</ul>
		</div>
	</div>

	<div style='float: right; width: 47%; position: absolute; top: 2%; left: 51%; background: #3167B3; padding-bottom: 0.5%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Atributos selecionados</div>
		<div class="navigateable_box" style="height: 90%; overflow-x: hidden; overflow-y: hidden; background-color: white; padding: 4px; padding-bottom: 10px;">
			<ul id="sortable2" class="connectedSortable" style="width: 100%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
HTML
	}
else
	{
print<<HTML;

	<div style='float: right; width: 47%; position: absolute; top: 2%; left: 51%; background: #3167B3; padding-bottom: 0.5%;'>
		<div class='fake_aba' style='width: 40%; margin-left: 0px; padding: 5px;'>Atributos selecionados</div>
		<div class="navigateable_box" style="height: 90%; overflow-y: hidden; background-color: white; padding: 4px;">
			<ul id="sortable2" class="connectedSortable" style="width: 100%; height: 100%; padding: 0px; overflow-y: auto; border: none 0px; margin: 0px; margin-top: 3px;">
HTML
	}

	
$SQL = "select * from comp_item join tipo_grupo_item on comp_item.tipo = tipo_grupo_item.codigo ";
$sth9 = &select("select * from information_schema.columns where table_name = 'comp_item' and column_name = 'parceiro' ");
$rv9 = $sth9->rows();
if($rv9 > 0)
	{
	$SQL .= " join parceiro_tipo_grupo_item on tipo_grupo_item.codigo = parceiro_tipo_grupo_item.tipo_grupo_item and parceiro_tipo_grupo_item.parceiro = comp_item.parceiro and parceiro_tipo_grupo_item.parceiro = '$LOGEMPRESA' ";
	}
$SQL .= "order by seq";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		print "<li class='ui-state-default' id='item_";
		print $row->{'tipo'};
		print "'>";

		$SQL4 = "select * from empresa_comp_adicional where comp_item = '".$row->{'tipo'}."' ";


		$sth4 = &select($SQL4);
		$rv4 = $sth4->rows();
		if($rv4 > 0)
			{
			print "<font style='color: #31517a; font-weight: bold;'>$row->{'descrp'}</font>";
			$list_items_blocked .= "##item_$row->{'tipo'}##";
			}
		else
			{
			print $row->{'descrp'};
			}
		$sth4->finish;
		print "</li>";
		}
	}

print<<HTML;
			</ul>
		</div>
	</div>
	

<input type='hidden' name='ADD'>
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='MODO' value='$MODO'>
<input type='hidden' name='FORCE' value='N'>
</form>

<script language='JavaScript'>
	blk_items = "$list_items_blocked";
</script>
HTML
