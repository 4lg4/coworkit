#!/usr/bin/perl

$nacess = "301";
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('COD');
$MODO = &get('MODO');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">	
<script language='JavaScript'>
	// carrega dependencias especificas
	\$('link[rel=stylesheet][href="/css/modulos/usuarios.css"]').remove();
	DLoad("usuario_tipo");

	// Popula os formulário
	function DActionEdit()
		{
		Loading();
		
		\$.ajax({
			type: "POST",
			url: "$dir{usuario_tipo}/edit_list.cgi",
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
		
	// quando o documento esta pronto 
	\$(document).ready(function() 
		{
		\$("#descrp_container").DTouchBoxes({title:"Descrição"});
		
		var MODO=\$('#MODO').val();
		
		if(MODO=="editar")
			{
			//Exibe os menus
			var menu_chamado = new menu(['icon_save','icon_delete']);
			}
		else
			{
			//Exibe os menus
			var menu_chamado = new menu(['icon_save']);
			}
		
		//Chama o edit_list e popula os campos.
		DActionEdit();
		});
	
	// salvar - atualizar, funcoes
	function DActionSave()
		{
		var DIR="$dir{usuario_tipo}/edit_submit_insert.cgi";
		var MODO=\$('#MODO').val();
		
		if(MODO=="editar")
			{
			DIR="$dir{usuario_tipo}/edit_submit_update.cgi";
			}
		
		var tipo_descrp=\$("#tipo_descrp").val();
		var radios=\$("#RADIOS").val();
		
		// testa campos obrigatorios
		if( tipo_descrp == "" ||radios =="" )
			{
			alerta("Campo descrição é obrigatório!");
			return false;
			}
		
		var req=\$("#CAD").serialize()+"&radios="+radios;
		
		//alert(req);

		Loading();
			
		\$.ajax({
			type: "POST",
			url: DIR,
			dataType: "html",
			data: req,
			success: function(data)
				{
				if(MODO=="incluir")
					{
					formularioReset();
					}
				\$("#resultado").html(data);
				unLoading();
				},
			error: errojx
			});
		}
		
	// Excluir, funcoes
	function DActionDelete()
		{
		
		var req=\$("#CAD").serialize();
		
		Loading();

		\$.ajax({
			type: "POST",
			url: "$dir{usuario_tipo}/edit_submit_delete.cgi",
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
		
		/* zera formulario */
		function formularioReset()
			{
			\$("#COD").val("");
			\$("#tipo_descrp").val("");
			
			// ajusta botoes
			var menu_chamado = new menu(['icon_save']);
			
			// reload nos dados que vem do banco
			DActionEdit();
			}
</script>

</head>
<body>

<form name='CAD' id='CAD'>

<div id="descrp_container">
	<input type='text' id="tipo_descrp" name='tipo_descrp' value='' />
</div>

<div id="menu_container">
	<div id="menu_boxes"></div>
</div>


<div id="resultado" class="DDebug"></div>
	<!-- variaveis de ambiente -->
	<input type='hidden' name='ID' value='$ID'>	
	<input type='hidden' name='COD' id="COD" value='$COD'>
	<input type='hidden' name='MODO' id='MODO' value='$MODO'>
	<input type='hidden' name='RADIOS' ID='RADIOS'>
</form>
</body>
</html>
HTML



