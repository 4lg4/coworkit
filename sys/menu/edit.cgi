#!/usr/bin/perl

$nacess = "5";
require "../cfg/init.pl";
$ID = &get('ID'); 
$MODO = &get('MODO');

print $query->header({charset=>utf8});

# pai do menu
$DB = &select("select m.* from menu as m where m.show is true and acao is NULL and m.codigo <> '2' and m.codigo <> '17' and m.codigo <> '28' and m.codigo <> '29' order by descrp asc");
while($m = $DB->fetchrow_hashref)
	{
	if($m->{pai} eq "")
		{
		$pai_db_pai  .= "<option value='$m->{codigo}'>$m->{descrp}</option>";
		}
	else
		{
		$pai_db  .= "<option value='$m->{codigo}'>$m->{descrp}</option>";
		}
	}
$pai_db = "<optgroup label='Principal' id='principal'>".$pai_db_pai."</optgroup><optgroup label='Interno' id='interno'>".$pai_db."</optgroup>";
# $pai_db = $pai_db_pai."******".$pai_db;	
	
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script type="text/javascript" src="/comum/DPAC.js"></script>
<script type="text/javascript">

/* [INI] -------------------------------------------------------------------------------------------------------------------------------
	ON START 
		quando o documento esta pronto 
------------------------------------------------------------------------------------------------------------------------------------- */
	\$(document).ready(function() 
		{
		parent.block(true);
		menu = new top.menu(['icon_insert']);
		
		// inicia tabs
		\$("#menu_tabs").tabs();
		
		// inicia dboxes
		frmbox = new dbox("menu_form","Edição de Menus");
		// frmbox.setSize("100%","180px");
		frmbox.show();
			
		// esconde formulario
		\$("#hold_frm").hide();
		
		// inicia campos formulario
		fieldOptDisable(["acao","mobile","coluna","nacess"]); // desabilita campos
		
		// definicao do menu pai
		\$("#pai").change(function()
			{
			// se for para criar o menu principal (avo)
			if(\$("#pai :selected").val() == "")
				{
				fieldOptDisable(["acao","mobile","coluna","nacess"]);
				}
			else if(\$("#pai :selected").parent().attr("label").toLowerCase() == "principal") // se for menu interno (pai)
				{
				fieldOptDisable(["acao","mobile","nacess"]);
				fieldOptEnable("coluna");
				}
			else  // se for menu acao (filho)
				{
				fieldOptEnable(["acao","mobile","nacess"]);
				fieldOptDisable("coluna");
				}
			});
		
		// carrega lista dos menus
		menus();
		
		top.unLoading();
		});
	/* [END] ON START ------------------------------------------------------------------------------------------------------------------  */


	/* Função que desabilita campo select */


	/*  Executa  */
	function menus(opt)
		{
		top.Loading();
				
		req = \$("#CAD").serialize()+"&opt="+opt+"&";
		
		//alert(req);
		
		// Executa wizard submits
		$ajax_init \$.ajax(
			{
			type: "POST",
			url: "menu.cgi",
			dataType: "html",
			data: req,
			success: function(data)
				{
				\$("body").append(data);		
				top.unLoading();
				},
			error: errojx
			});
		}
		

	/* BTN novo */
	function incluir()
		{
		formClean();
		\$("#hold_frm").show();
		menu.btnHide('icon_insert');
		menu.btnShow(['icon_save','icon_cancel']);
		fieldOptDisable(["acao","mobile","coluna","nacess"]); // desabilita campos
		}

	/* BTN salvar */
	function salvar()
		{
		if(\$("#descrp").val() == "")
			{
			top.alerta("Campo descrição deve ser preenchido! ");
			return false;
			}
			
		if(\$("#MENU").val() == "")
			{
			menus("insert");
			}
		else
			{
			menus("update");
			}
		}

	/* BTN cancelar */
	function cancelar()
		{
		\$("#hold_frm").hide();
		menu.btnHide('icon_save');
		menu.btnHide('icon_cancel');
		menu.btnHide('icon_delete');
		menu.btnShow('icon_insert');
		}
		
	/* BTN excluir */
	function excluir(tipo)
		{
		if(tipo=="1")
			{
			menus("excluir");
			}
		else
			{
			menus("verificar");
			}
		}
			
	/* funcao CLICK - funcoes do grid */
	function gridClick(x)
		{
		\$("#MENU").val(x);
		menu.btnShow('icon_cancel');
		menu.btnShow('icon_save');
		menu.btnShow('icon_delete');
		\$("#hold_frm").show();
		
		menus(x);
		// alert("Click - "+x);
		}
		
	/* funcao Duplo CLICK - funcoes do grid */
	function DGridDblClick(x)
		{
		// alert("DBL Click - "+x);
		}

	/* limpa formulario */
	function formClean()
		{
		\$("#MENU, #descrp, #acao, #mobile, #pai, #nacess, #ordem, #coluna").val("");
		// selecionar ativo como SIM
		}
</script>

</head>

<body style="min-width:1024px;">

<form name='CAD' id='CAD' method='post'>
<input type='hidden' name='ID' id='ID' value='$ID'>
<input type='hidden' name='MODO' id='MODO' value='$MODO'>
<input type='hidden' name='MENU' id='MENU'>


<!-- Formulario --> 
<div id="hold_frm" style="margin-bottom:20px; margin-right:10px; margin-top:10px;">
		
	<div id="menu_form" style='width:90%; margin-left:2%;'>
	<table>
		<tr>	
			<td>Descrição</td>
			<td>
				<input type="text" name="descrp" id="descrp" style="margin-right:40px; width:40%;">
				
				Num. Acess
				<input type="text" name="nacess" id="nacess" style="width:20%; float:right;">
			</td>
		</tr>
		<tr>
			<td>Ação</td>
			<td>
				<input type="text" name="acao" id="acao"style="margin-right:40px; width:40%;">
				
				Mobile
				<input type="text" name="mobile" id="mobile" style="width:40%; float:right;">
			</td>
		</tr>
		<tr>
			<td>Pai</td>
			<td>
				<select name="pai" id="pai"><option value=""></option>$pai_db</select>
			</td>
		</tr>
		<tr>
			<td>Icone</td>
			<td>
				<input type="text" name="icone" id="icone">
			</td>
		</tr>
		<tr>
			<td>Ordem</td>
			<td>
				<input type="text" name="ordem" id="ordem" style="margin-right:40px; width:40%;">
				
				Coluna
				<select name="coluna" id="coluna" style="width:40%; float:right;">
				<option value="1">1</option>
				<option value="2">2</option>
				<option value="3">3</option>
				<option value="4">4</option>				
				</select>
			</td>
		</tr>
		<tr>
			<td>Ativo</td>
			<td>
				Sim <input type="radio" name="show" id="show" value="1">  Não <input type="radio" name="show" id="show" value="0">
			</td>
		</tr>
	</table>
	</div>
	
</div>

<!-- Abas -->
<div style="width:100%; margin-bottom:20px;">
			
		<div id="menu_tabs" style="clear:both; margin-top:5px; margin-right:10px;" align="right" >
			<ul style='border-bottom:0px;'>
				<li style='margin-top: 2px'><a href='#tabs-0'>Ativos</a></li>
				<li style='margin-top: 2px'><a href='#tabs-1'>Não Ativos / Escondidos</a></li>
				<li style='margin-top: 2px'><a href='#tabs-2'>Visualizar</a></li>
			</ul>

			<!-- Ativos -->
			<div id="tabs-0"  style='width:100%;' class="grid_bg">
				<div id='menu_active'></div>
			</div>
			
			<!-- Inativos -->
			<div id="tabs-1"  style='width:100%;' class="grid_bg">
				<div id='menu_inactive'></div>
			</div>
			
			<!-- Visualizar -->
			<div id="tabs-2"  style='width:100%;' class="grid_bg">
				<div id='menu_view' style="text-align:left; background:#fff;"></div>
			</div>
		</div>
			
</div>





</form>

</body></html>
HTML

