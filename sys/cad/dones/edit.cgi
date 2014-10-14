#!/usr/bin/perl

$nacess = "999";
require "../../cfg/init.pl"; #ou "../cfg/init.pl"

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
	var m=0;

	// carrega dependencias especificas (css,js e path)
	DLoad("dones");
	
	//Gera os botões actions
	var menu_dones = new menu();
	
	//Regex que limpa e retirar o que eu não quero By: Kelvyn C.
	function LimpaString (obj)
		{
		if(obj.prop('name')=="usuario")
			{
			var reg =/[^a-z0-9-\@\_\-|\.]/gi;
			var reg2 =/\[|\]|\`/i;
			}
		else
			{
			var reg =/[^a-z0-9-\_\-|\.]/gi;
			var reg2 =/\[|\]|\@|\`/i;
			}
		retirar=obj.val().replace(reg2,"");
		obj.val(retirar);
		retirar=obj.val().replace(reg,"");
		obj.val(retirar);
		
		}
	
	function check_validate()
		{
		var username = \$('#usuario').val();
		if(username != "" && username.length > 2  && user_verifica !=username)
			{
			jQuery.ajax(
				{
				type: "POST",
				url: "/sys/cad/dones/check.cgi",
				data: 'username='+ username,
				cache: false,
				success: function(response)
					{
					if(response == 1)
						{
						\$('#usuario').css('border', '2px #C33 solid');
						}
					else
						{
						\$('#usuario').css('border', '2px #090 solid');
						}
					}
				});
			}
		else
			{
			\$("#usuario").css("border","none");
			}
		}
	
	function check_host()
		{
		var hostname = \$('#hostname').val();
		if(hostname.length > 2 && hostname != "" && host_verifica !=hostname || domain_verifica !=\$('#dones_domains').find(':selected').text())
			{
			hostname = hostname+"."+\$("#dones_domains").find(":selected").text();
			jQuery.ajax(
				{
				type: "POST",
				url: "/sys/cad/dones/check.cgi",
				data: 'hostname='+ hostname,
				cache: false,
				success: function(response)
					{
					if(response == 1)
						{
						\$('#hostname').css('border', '2px #C33 solid');
						}
					else
						{
						\$('#hostname').css('border', '2px #090 solid');
						}
					}
				});
			}
		else
			{
			\$("#hostname").css("border","none");
			}
		} 
	
	// Função Salvar - Atualizar
	function DActionSave()
		{		
		if(\$("#usuario").val()=="" || \$("#hostname").val()=="" || \$("#senha").val()=="" || \$("#descrp").val()=="")
			{
			alerta("Os campos: <br><br> Usuário, <br> Hostname, <br> Senha, <br> Descrição, <br><br> São obrigatórios! ");
			return false;
			}
		
		// Serializa o formulário
		var req="&domain_name="+\$("#dones_domains").find(":selected").text()+"&user_verifica="+user_verifica+"&host_verifica="+host_verifica;
		
		if(\$("#CAD input[name=COD]").val()=="")
			{
			//Ajax Post
			DActionAjax('edit_submit_insert.cgi',req,'bloco_form');
			}
		else
			{
			//Ajax Post
			DActionAjax('edit_submit_update.cgi',req,'bloco_form');
			}
		}
		
	// novo / incluir
	function DActionAdd()
		{
		//Define os icones visiveis
		menu_dones.btnHideAll();
		menu_dones.btnShow(['icon_save','icon_cancel']);
		m=1;
		
		//Limpa o form
		ResetForm();
		
		//Depois de limpo, exibe
		\$("#bloco_form").fadeIn();
			
		//Foca no titulo
		\$("#hostname").focus();
		}
		
	// Função Salvar - Atualizar
	function DActionCancel()
		{
		if(\$('#VOLTAR').val()==1)
			{
			top.callRegrid('empresas');
			}
		else if(\$("#bloco_form").css('display')=='block')
			{
			\$("#bloco_form").fadeOut();
			menu_dones.btnHideAll();
			menu_dones.btnShow(['icon_insert','icon_cancel']);
			\$("#dones_list").DTouchRadio("reset");
			\$("#usuario").css("border","none");
			\$("#hostname").css("border","none");
			}
		else if(\$("#bloco_empresas").css('display')=='none')
			{
			\$("#endereco_list").DTouchRadio("DTouchRadioSetValue",'');
			\$("#bloco_empresas").show("slide");
			\$("#bloco_proced").css('display','none');
			}
		}
		
	// Função Excluir
	function DActionDelete()
		{
		
		//Serializa o formulário
		var req=\$("#CAD").serialize();
		
		//Loader na div
		loadingObj('bloco_form');
			
		//Ajax Post
		DActionAjax('edit_submit_delete.cgi',req,'bloco_form');
		
		}
		
	// Função de edição de registro
	function DActionEdit()
		{
		
		//Serializa o formulário
		var req=\$("#CAD").serialize();
		
		// Loader Padrão
		Loading();
		
		//Ajax Post
		DActionAjax('edit_db',req,'body')
			{
			unLoading();
			}
		}
		
	//Zerar formulário]
	function ResetForm()
		{
		\$("#CAD input[name=MODO]").val("incluir");
		\$("#CAD input[name=COD]").val("");
		\$("#hostname").val("");
		\$("#obs_user").val("");
		\$("#usuario").val("");
		\$("#senha").val("");
		\$("#dones_domains").val("");
		\$("#usuario").css("border","none");
		\$("#hostname").css("border","none");
		host_verifica="";
		user_verifica="";
		}
		
	// Função que puxa empresas
	function procede(x)
		{
		\$("#bloco_proced").fadeIn();
		if(x)
			{
			// Serializa o formulário
			var req=\$("#CAD").serialize()+"&empresa="+x;

			//Ajax Post
			DActionAjax('edit_db.cgi',req,'bloco_empresas')
				{
				\$("#empresa").val(x);
				\$("#search_dones").val("");
				\$("#search_dones").focus();
				\$("#bloco_form").fadeOut();
				menu_dones.btnShow(['icon_insert']);
				}
			}
			
		}
		
	//Função que puxa os enderecos
	function enderecos(x)
		{
		
		// Serializa o formulário
		var req="&empresa="+x;
		
		//Ajax Post
		DActionAjax('edit_db.cgi',req,'bloco_endereco',true)
			{
			\$("#search_endereco").val("");
			\$("#search_endereco").focus();
			\$("#bloco_form").fadeOut();
			}
		}
		
	//Função que puxa os procedimento do endereco
	function proced_list(x)
		{
		menu_dones.btnShow(['icon_insert']);
		
		var req="&endereco="+x;
		// Serializa o formulário
		if(x!="null")
			{
			var req="&endereco="+x;
			}

		//Ajax Post
		DActionAjax('edit_db.cgi',req,'bloco_dones',true)
			{
			\$("#search_dones").val("");
			\$("#search_dones").focus();
			\$("#bloco_form").fadeOut();
			\$("#bloco_dones").fadeIn();
			}
		}
		
	// Função mostra o procedimento
	function detalhe_proced(x)
		{		
		if(x)
			{
			//Exibe o bloco detalhe_proced
			\$("#bloco_form").fadeIn();
			
			menu_dones.btnShow(['icon_insert','icon_save','icon_delete']);
			
			// Serializa o formulário
			var req="&proced="+x;
			
			//Ajax Post
			DActionAjax('edit_db.cgi',req,'bloco_form',true)
				{
				\$("#CAD input[name=COD]").val(x);
				\$("#CAD input[name=MODO]").val("editar");
				}
			}
		}
		
	// quando o documento esta pronto 
	\$(document).ready(function() 
		{		
		
		\$("#usuario").keyup(function(event) { if(event.which == 9) event.preventDefault(); else {  LimpaString(\$("#usuario")); check_validate(); } });
		\$("#hostname").keyup(function(event) { if(event.which == 9) event.preventDefault(); else { LimpaString(\$("#hostname")); check_host(); } });
		
		// Dboxe empresas
		\$("#bloco_empresas").DTouchBoxes({title:"Lista de empresas"});
		
		// Lista de endereços
		\$("#bloco_endereco").DTouchBoxes({title:"Lista de endereços"});
		
		// 
		\$("#bloco_form").DTouchBoxes({title:"Informações Dones"});
		
		// Dboxe procedimentos
		\$("#bloco_dones").DTouchBoxes({title:"Dones"});
		
		LoadingObj('bloco_empresas');
		
		var externo="$COD";
		
		\$("#search_empresas").focus();
		
		//DSearch no grid empresa
		\$("#empresas_list").DSearch({
		linha:'DTouchRadio',
		campo: \$("#search_empresas")
		});
		
		//DSearch nos enderecos
		\$("#endereco_list").DSearch({
		linha:'DTouchRadio',
		campo: \$("#search_endereco")
		});
		
		//DSearch nos enderecos
		\$("#dones_list").DSearch({
		linha:'DTouchRadio',
		campo: \$("#search_dones")
		});
		
		if(externo!="")
			{
			\$("#externo").val(externo);
			\$("#empresa").val(externo);
			\$("#bloco_empresas").hide();
			}
		if("$USER->{empresa}"!=1)
			{
			\$("#empresa").val($USER->{empresa});
			\$("#bloco_empresas").hide();
			}
		
		var req_ext=\$("#CAD").serialize();
		
		//Popula os campos
		DActionEditDB(req_ext);
		
		
		
		});
</script>

</head>
<body>

<form name='CAD' id='CAD'>

<div id="bloco_empresas">
	Pesquisar:<input type="text" id="search_empresas" />
	<div id="empresas_list">
	</div>
</div>

<div id="bloco_endereco">
	Pesquisar:<input type="text" id="search_endereco" />
	<div id="endereco_list">
	</div>
</div>

<div id="bloco_dones">
	Pesquisar:<input type="text" id="search_dones" />
	<div id="dones_list">
	</div>
</div>

<div id="bloco_form">
	<table>
		<tr>
			<td>
				Hostname:
			</td>
			<td>
				<input type="text" name="hostname" id="hostname" value="">
				<campo id="domain"></campo>
			</td>
		</tr>
		<tr>
			<td>
				Usuário:
			</td>
			<td>
				<input type="text" name="usuario" id="usuario" value="">
			</td>
		</tr>
		<tr>
			<td>
				Senha:
			</td>
			<td>
				 <input type="text" name="senha" id="senha" value="">
			</td>
		</tr>
		<tr>
			<td>
				Descrição:
			</td>
			<td>
				 <textarea id="obs_user" name="obs_user"></textarea>
			</td>
		</tr>
	</table>
</div>


<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='ID' value='$ID'>	
	<input type='hidden' name='COD' id="COD" value='$COD'>
	<input type='hidden' name='MODO' id='MODO' value='$MODO'>
	<input type='hidden' name='empresa' id="empresa" value=''>
	<input type='hidden' name='endereco' id='endereco' value=''>
	<input type='hidden' name='externo' id='externo' value=''>
	<input type='hidden' name='VOLTAR' id='VOLTAR' value='$VOLTAR'>
</form>

</body>
</html>
HTML



