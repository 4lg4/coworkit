#!/usr/bin/perl

$nacess = "200";
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
		
		
// Popula os formulário
function listTipo()
	{
	unLoading();
	return;
	Loading();
	\$.ajax({
		type: "POST",
		url: "/sys/cad/usuario_cfg/edit_db.cgi",
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
		
	
	var DIR="/sys/cad/usuario_cfg/edit_submit.cgi";
	var MODO=\$('#MODO').val();
	var req=\$("#CAD").serialize()+"&page="+\$("#pages").DTouchRadio("value")+"&grid_num="+\$("#grid_num").DTouchRadio("value");

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
	var MODO=\$('#MODO').val();
	\$("#bloco_grid").hide();
	\$("#bloco_pages").hide();
	
	if("$nacess_tipo" == "a")
		{
		var menu_user = new menu(['icon_save']);
		\$("#bloco_grid").show();
		\$("#bloco_pages").show();
		}
	else
		{
		//Exibe os menus
		var menu_user = new menu(['icon_save']);
		\$("#menu_container").hide();
		\$("#tipo_usuario_container").hide();
		\$("#cliente_container").hide();
		\$("#user_more_container_full").hide();
		\$("#bloco_grid").show();
		\$("#bloco_pages").show();
		}

	
	//Chama o edit_list e popula os campos.
	listTipo();	
	
	// dados pessoais 
	\$("#user_more_container_full").DTouchBoxes({title:"Dados Pessoais"});
	
	// upload de foto
	\$("#bloco_upload").DTouchBoxes({title:"Escolha um avatar"});
	
	// pagina inicial
	\$("#bloco_pages").DTouchBoxes({title:"Página inicial"});
	
	// grid_num
	\$("#bloco_grid").DTouchBoxes({title:"Top Empresas"});
	
	//Upload de arquivo
	\$("#upload").fieldUpload(
		{
		type		: 'new Array(".jpg",".png")',
		maxsize		: '8000000',  //8 mb
		table		: 'usuario',
		field		: 'img',
		list		: true,
		unique		: true,
		crop		: true
		});
		
	\$("#pages").DTouchRadio({ orientation:'horizontal',addItem:[$page_initial] });
	\$("#grid_num").DTouchRadio({ orientation:'vertical',  addItem:[$grid] });
	
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
		
	\$('#grid_num').DTouchRadio('SetValue','$grid_sel->{valor}');
	\$('#pages').DTouchRadio('SetValue','$page_sel->{valor}');
	
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
			
			<div id="bloco_pages">
				<div id="pages"></div>
			</div>
			
			<div id="bloco_grid">
				<div id="grid_num"></div>
			</div>
			
			<div id="bloco_upload">
				<div id="upload"></div>
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
