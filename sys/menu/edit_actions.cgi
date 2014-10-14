#!/usr/bin/perl

$nacess = "3";
require "../cfg/init.pl";
$ID = &get('ID'); 
$MODO = &get('MODO');

print $query->header({charset=>utf8});

# if($MODO eq "editar" || $MODO eq "incluir")
#	{
#	if($nacess_tipo ne "a" && $nacess_tipo ne "s")
#		{
#		$MODO = "ver";
#		print "<script>top.alerta('Acesso Negado!');</script>";
#		exit;
#		}
#	}
	
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
	// parent.block(true);
	menu = new top.menu(['icon_insert']);
	
	// inicia tabs
	\$("#menu_tabs").tabs();
	
	// inicia dboxes
	frmbox = new dbox("menu_form","Edição de Menus");
	// frmbox.setSize("100%","150px");
	frmbox.show();
		
	// esconde formulario
	\$("#hold_frm").hide();
	
	// carrega lista dos menus
	menus();
	
	\$("#id").focusout(function()
		{
		\$("#nome").val(\$("#id").val());
		});
	
	top.unLoading();
	});
/* [END] ON START ------------------------------------------------------------------------------------------------------------------  */

/*  Executa  */
function menus(opt)
	{
	top.Loading();
			
	req = \$("#CAD").serialize()+"&opt="+opt+"&";
	
	// Executa wizard submits
	$ajax_init \$.ajax(
		{
		type: "POST",
		url: "menu_actions.cgi",
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
	// menu.btnHide('icon_insert');
	menu.btnShow(['icon_save','icon_cancel']);
	}

/* BTN salvar */
function salvar()
	{
	if(\$("#ID").val() == "" || \$("#descrp").val() == "")
		{
		top.erro("Erro: Campo(s) deve(m) ser preenchido(s): <hr> ID / Descrição ","descrp");
		return;
		}
		
	if(\$("#MENU").val() == "")
		menus("insert");
	else
		menus("update");	
	}

/* BTN cancelar */
function cancelar()
	{
	\$("#hold_frm").hide();
	menu.btnShow(['icon_insert']);
	}
	

		
/* funcao CLICK - funcoes do grid */
function gridClick(x)
	{
	\$("#MENU").val(x);
	menu.btnShow(['icon_save','icon_delete','icon_cancel']);
	\$("#hold_frm").show();
	
	menus("select");
	// alert("Click - "+x);
	}

/* funcao Duplo CLICK - funcoes do grid */
function gridDblClick(x)
	{
	// alert("DBL Click - "+x);
	}

/* BTN excluir */
function excluir(opt)
	{
	if(!opt)
		{
		top.confirma("Deseja realmente excluir essa ação é irreversível! ","main.excluir(1)","");
		return;
		}	
		
	menus("delete");
	menu.btnShow(['icon_insert']);
	\$("#hold_frm").hide();
	}
	
/* limpa formulario */
function formClean()
	{
	\$("#MENU, #descrp, #descrp_sub, #id, #nome, #funcao, #funcao_2, #classe, #ordem").val("");
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
			<dl>
				<div>
					<dt>ID</dt>
					<dd>
						<input type="text" name="id" id="id" style="margin-right:40px; width:40%;">
						
						Nome
						<input type="text" name="nome" id="nome" style="width:40%; float:right;">
					</dd>
				</div>
				<div>
					<dt>Descrição</dt>
					<dd>
						<input type="text" name="descrp" id="descrp" style="margin-right:40px; width:40%;">
						
						Secundária
						<input type="text" name="descrp_sub" id="descrp_sub" style="width:40%; float:right;">
					</dd>
				</div>
				<div>
					<dt>Função OnClick</dt>
					<dd>
						<input type="text" name="funcao" id="funcao" style="margin-right:40px; width:40%;">
						
						OnDblClick
						<input type="text" name="funcao_2" id="funcao_2" style="width:40%; float:right;">
					</dd>
				</div>
				<div>
					<dt>Classe</dt>
					<dd>
						<input type="text" name="classe" id="classe" style="margin-right:40px; width:40%;">
						
						Ordem
						<input type="text" name="ordem" id="ordem" style="width:20%; float:right;">
					</dd>
				</div>
			</dl>
	</div>
	
</div>

<!-- Abas -->
<div style="width:100%; margin-bottom:20px;">
			
		<div id="menu_tabs" style="clear:both; margin-top:5px; margin-right:10px;" align="right" >
			<ul style='border-bottom:0px;'>
				<li style='margin-top: 2px'><a href='#tabs-0'>Ativos</a></li>
				<!-- <li style='margin-top: 2px'><a href='#tabs-1'>Não Ativos / Escondidos</a></li> -->
				<li style='margin-top: 2px'><a href='#tabs-2'>Visualizar</a></li>
			</ul>

			<!-- Ativos -->
			<div id="tabs-0"  style='width:100%;' class="grid_bg">
				<div id='menu_active'></div>
			</div>
			
			<!-- Inativos 
			<div id="tabs-1"  style='width:100%;' class="grid_bg">
				<div id='menu_inactive'></div>
			</div>
			-->
			
			<!-- Visualizar -->
			<div id="tabs-2"  style='width:100%;' class="grid_bg">
				<div id='menu_view' style="text-align:left; background:#fff; padding-top:20px; padding-bottom:20px;">
					<div id="menu_view_int" align="center" style="text-align:center; margin-left:60px; padding-top:25px; border:1px dotted #ccc; width:53px; padding-left:7px; padding-bottom:20px"></div>
				</div>
			</div>
		</div>
			
</div>





</form>

</body></html>
HTML

