#!/usr/bin/perl

$nacess = "";
require "../cfg/init.pl"; #ou "../cfg/init.pl"

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

	// carrega dependencias especificas (css,js e path)
	DLoad("default_avatar");
		
	// quando o documento esta pronto 
	\$(document).ready(function() 
		{
		
		\$("#bloco_upload").DTouchBoxes({title: 'Upload de arquivos Default'});
		\$("#bloco_modulos").DTouchBoxes({title: 'Modulos do sistema'});
		
		\$('#modulos').DTouchRadio(
				{
				orientation:'vertical'
				});
		
		//Upload de arquivo
		\$("#upload").fieldUpload(
			{
			maxsize		: '8000000',  //8 mb
			table		: 'default_avatar',
			field		: 'arquivo',
			editable	: true,
			descrp		: true,
			type		: 'all',
			UploadList	: function UploadList(x)
						{
						var req="&action=list&COD="+x;
						loadingObj('upload');
						DActionAjax('/sys/upload/upload_default.cgi', req, 'body');
						},
			UploadDelete	: function UploadDelete(x)
						{
						var req="&action=delete&arquivo="+x;
						loadingObj('upload');
						DActionAjax('/sys/upload/upload_default.cgi', req, 'body');
						},
			UploadReturn	: function UploadReturn(x)
						{
						var req="&action=insert&arquivo="+x.MD5+"&descrp="+x.nome+"&COD="+\$("#COD").val();
						loadingObj('upload');
						DActionAjax('/sys/upload/upload_default.cgi', req, 'body');
						}
			});
			
		DActionEditDB();
		});
	
	// Função incluir - Exibe o form de inclusão
	function DActionAdd()
		{
		
		}
		
	// Função cancelar - Esconde o form de inclusão
	function DActionCancel()
		{
		
		}
	
	// Função Salvar - Atualizar
	function DActionSave()
		{
		
		// Serializa o formulário
		var req=\$("#CAD").serialize()+"&radios="+radios;
		
		//alert(req);

		Loading();
			
		//Ajax Post
		DActionAjax(page,req,obj)
			{
			unLoading();
			}
		}
		
	// Função Excluir
	function DActionDelete()
		{
		
		//Serializa o formulário
		var req=\$("#CAD").serialize();
		
		// Loader Padrão
		Loading();
		
		//Ajax Post
		DActionAjax(page,req,obj)
			{
			unLoading();
			}
		}
		
	// Função de edição de registro
	function DActionEdit()
		{
		
		//Serializa o formulário
		var req=\$("#CAD").serialize();
		
		// Loader Padrão
		Loading();
		
		//Ajax Post
		DActionAjax(page,req,obj)
			{
			unLoading();
			}
		}
		
	//Zerar formulário]
	function ResetForm()
		{
		// Puxa o arquivo edit_db.cgi
		DActionEditDB();
		}
</script>

</head>
<body>

<form name='CAD' id='CAD'>

<div id="bloco_modulos">
	<div id="modulos"></div>
</div>

<div id="bloco_upload">
	<div id="upload"></div>
</div>

<div id="resultado" class="DDebug"></div>
	<!-- variaveis de ambiente -->
	<input type='hidden' name='ID' value='$ID'>	
	<input type='hidden' name='COD' id="COD" value='$COD'>
	<input type='hidden' name='MODO' id='MODO' value='$MODO'>
</form>

</body>
</html>
HTML



