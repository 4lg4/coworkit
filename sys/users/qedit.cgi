#!/usr/bin/perl

$nacess = "203";
require "../../cfg/init.pl";
$COD = &get('COD');
$MODO = &get('MODO');

# variavel para controle de troca de pagina direto do menu
# $PAGE = &get('PAGE');

# carrega valores do banco de dados
require "./edit_db.pl";

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">	
<script language='JavaScript'>
// carrega dependencias especificas
\$('link[rel=stylesheet][href="/css/modulos/tipo_usuario.css"]').remove();
DLoad("usuarios");

function DActionCancel()
	{
	callRegrid('usuario');
	}
	
function DActionAdd()
	{
	var variaveis =
		{
		COD : '',
		MODO : 'incluir'
		};
	top.call("cad/usuarios/edit.cgi",variaveis);
	}

function DActionDelete()
	{
	var req=\$("#CAD").serialize();
	
	Loading();

	\$.ajax({
		type: "POST",
		url: "$dir{usuario}/edit_submit_delete.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("#resultado").html(data);
			unLoading();
			},
		error: errojx
		});
	}		
		
// Popula os formulário
function listTipo()
	{
	unLoading();
	return;
	Loading();
	\$.ajax({
		type: "POST",
		url: "$dir{usuario}/edit_db.cgi",
		dataType: "html",
		data: "&COD="+\$("#COD").val(),
		success: function(data)
			{
			\$("#resultado").html(data); // DDebug
			unLoading(); // remove loader

			
			},
		error: errojx
		});
	}

function changeTipo(x)
	{
	Loading();
	
	if(x)
		{
		req = "&USUARIO="+x;
		}
	else
		{
		req = "&COD="+DTouchRadioGetValue(\$("#tipo_usuario_radio"));
		}
  
	\$.ajax({
		type: "POST",
		url: "$dir{usuario_tipo}/edit_list.cgi",
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("#resultado").html(data); // DDebug
			unLoading(); // remove loader
			},
		error: errojx
		});
	}
		
function DActionSave()
	{
	if(\$('#login').val() == '')
		{
		alerta("Você não preencheu o Login do Usuário", "\$('#login').focus()");
		return false;
		}
	if(\$('#nome').val() == '')
		{
		alerta("Você não preencheu o Nome do Usuário", "\$('#nome').focus()");
		return false;
		}
	if(\$('#email').val() == '')
		{
		alerta("Você não informou o e-mail do Usuário", "\$('#email').focus()");
		return false;
		}
	if(isMail(\$('#email').val()) == false)
		{
		alerta("Você não informou o e-mail do Válido", "\$('#email').focus()");
		return false;
		}
	if(\$('#senha').val() == '')
		{
		alerta("Senha do usuário não informada", "\$('#senha').focus()");
		return false;
		}
	if(\$('#senha').val() != \$('#senha2').val())
		{
		alerta("A senha está diferente na confirmação", "\$('#senha2').focus()");
		return false;
		}
	if(\$('#cliente').val() == '' || \$('#cliente_descrp').val() == '')
		{
		alerta("Você não informou a empresa do Usuário", "\$('#cliente').focus()");
		return false;
		}
		
	
	var DIR="$dir{usuario}edit_submit.cgi";
	var MODO=\$('#MODO').val();
	var req=\$("#CAD").serialize();
	Loading();
	
	\$.ajax({
		type: "POST",
		url: DIR,
		dataType: "html",
		data: req,
		success: function(data)
			{
			\$("#resultado").html(data); // DDebug
			unLoading();
			},
		error: errojx
		});
	}		

// quando o documento esta pronto 
\$(document).ready(function() 
	{
	\$("#bloco_grid").hide();
	\$("#bloco_pages").hide();
	
	var MODO=\$('#MODO').val();
	
	if("$nacess_tipo" === "a")
		{
		//Exibe os menus
		if("$login" === "")
			{
			// Modo inclusão esconde o campo senha
			\$("#user_senha_container_full").hide();
			var menu_user = new menu(['icon_cancel', 'icon_delete', 'icon_save']);
			\$("#bloco_upload").hide();
			}
		else
			{
			var menu_user = new menu(['icon_cancel', 'icon_insert', 'icon_delete', 'icon_save']);
			}
		}
	else
		{
		//Exibe os menus
		var menu_user = new menu(['icon_save']);
		\$("#menu_container").hide();
		\$("#tipo_usuario_container").hide();
		\$("#cliente_container").hide();
		\$("#user_senha_container_full").hide();
		\$("#user_more_container_full").hide();
		}

	
	//Chama o edit_list e popula os campos.
	listTipo();	
	
	// dados pessoais 
	\$("#user_more_container_full").DTouchBoxes({title:"Dados Pessoais"});
	
	// senha 
	\$("#user_senha_container_full").DTouchBoxes({title:"Definir uma senha"});
	
	// cliente
	\$("#cliente_container").DTouchBoxes({title:"Empresa"});
	// Define as mascaras dos campos
	\$("#cliente").fieldAutoComplete(
		{ 
		sql_tbl:"empresa",
		sql_sfield:"nome",
		sql_rfield:"nome",
		sql_order:"nome"
		});

	// tipo usuario
	\$("#tipo_usuario_container").DTouchBoxes({title:"Tipo Usuário"});
	\$("#tipo_usuario_radio").DTouchRadio(
		{
		DTouchRadioClick: changeTipo,
		addItem:[$tipo_usuario],
		visibleItems: 7
		});
	
	if("$tipo_usuario_var" != "")
		{
		\$("#tipo_usuario_radio").DTouchRadio('DTouchRadioSetValue', '$tipo_usuario_var')
		}
		
	if("$COD" != "")
		{
		changeTipo('$COD');
		}
	else
		{
		if("$tipo_usuario_var" != "")
			{
			changeTipo();
			}
		}

	
	if("$emp_nome" != "")
		{
		\$("#cliente").val("$emp_codigo");
		\$("#cliente_descrp").val("$emp_nome");
		}
	
	});
</script>

</head>
<body>

<form name='CAD' id='CAD'>
	
		<div id="div">
			<!-- dados principais -->
			<div id="user_more_container_full">
				<div id="user_more_container">
					<div id="nome_container">
						Login <br> <input type="text" name="login" id="login" value="$login"> <br clear=both>
						Nome completo <br> <input type="text" name="nome" id="nome" value="$nome"> <br clear=both>
						E-Mail <br> <input type="text" name="email" id="email" value="$email"> <br clear=both>
					</div>
				</div>
			</div>				

			<!-- senha -->
			<div id="user_senha_container_full">
				<div id="user_senha_container">
					<div id="senha_container">
						Informe <br> <input type="password" name="senha" id="senha" value="no change"> <br>
						Confirme<br> <input type="password" name="senha2" id="senha2" value="no change">
					</div>
				</div>
			</div>
			
			<!-- cliente / empresa -->
			<div id="cliente_container">
				<div id="cliente_holder_search">
					<!-- Cliente -->
					<input type="text" name="cliente" id="cliente">
				</div>
			</div>
		</div>
		
		<!-- tipo de usuário -->
			<div id="tipo_usuario_container">
				<div id="tipo_usuario_radio">
				</div>
				<div id="menu_container"></div>
			</div>

			

	
<div id="resultado" class="DDebug"></div>

<!-- variaveis de ambiente -->
<input type='hidden' name='ID' value='$ID'>
<input type='hidden' name='RADIOS' id="RADIOS" value='0'>
<input type='hidden' name='COD' id="COD" value='$COD'>
<input type='hidden' name='MODO' id='MODO' value='$MODO'>
</form>
</body>
</html>
HTML
