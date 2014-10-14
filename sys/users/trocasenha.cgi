#!/usr/bin/perl

# define acesso ao modulo -----------------------------------------------------
$nacess = "801";
require "../../cfg/init.pl";

if($LOGUSUARIO eq "")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

# Recupera dados usuario -----------------------------------------------------
# $SQL = "select nome from usuario where usuario = '$COD'";
$SQL = "select nome, senha from usuario where usuario = '$LOGUSUARIO'";
$sth = &select($SQL);
$rv = $sth->rows();
$usuario_ = $sth->fetchrow_hashref;	
	
print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/CSS_syscall/form.css" rel="stylesheet" type="text/css">
  <link rel="stylesheet" href="/css/CSS_syscall/jquery/base/jquery.ui.all.css" type="text/css">
  
  <script type="text/javascript" src="/comum/DPAC_syscall/iPAC.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery-1.4.2.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.core.js"></script>
  <script type="text/javascript" src="/comum/DPAC_syscall/jquery/ui/jquery.ui.widget.js"></script>
  
  
<script language='JavaScript'>  

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
		
	function salvar()
		{
		with(document.forms[0])
			{
			if(isNULL(senha_atual.value) == true)
				{
				erro('Você não informou a "senha atual"!', 'senha_atual');
				return false;
				}
			if(isNULL(senha_nova.value) == true)
				{
				erro('Você não informou a "nova senha"!', 'senha_nova');
				return false;
				}
			if(isNULL(senha_nova_prova.value) == true)
				{
				erro('Você não informou "repetir nova senha"!', 'senha_nova_prova');
				return false;
				}
			if(senha_nova.value != senha_nova_prova.value)
				{
				erro('Novas Senhas não conferem!', 'senha_nova');
				return false;
				}				
			if(senha_atual.value == senha_nova.value)
				{
				erro('A senha nova não pode ser igual a atual!', 'senha_atual');
				return false;
				}
			}
		document.forms[0].method = "post";
		document.forms[0].action = "trocasenha_submit.cgi";
		document.forms[0].submit();
		}
		
	function cancelar()
		{
		top.confirma('Você tem certeza que deseja cancelar?', 'top.grid("usuarios")', '');
		}
		
	function START()
		{
		// Limpa campos -----------------------------------------------------------
		linhas = document.body.getElementsByTagName('INPUT');
		for(var ln=0;ln<linhas.length;ln++)
			{
			linhas[ln].setAttribute('onchange', 'limpa(this.name)');
			linhas[ln].setAttribute('onblur', 'limpa(this.name)');
			}
			
		// Define Icones -----------------------------------------------------------
		top.ac_show(['icon_save', 'icon_cancel']);
		top.unLoading();
		}
</script>

<style>
.form dt{
	width:150px;
}
.form dd{
	width:200px;
}
.navigateable_box {
	min-height: 20px; 
	overflow-y: auto; 
	background-color: white; padding: 10px; 
	padding-top:0px;
}
.fake_aba {
	width: 70%; 
	margin-left: 0px; 
	padding: 5px;
}
.DVmain {
	width: 500px; 
	margin: 2%; 
	margin-right: 3%;
}
</style>
  
</head>

<body onLoad="START()">

<div class='DVmain'>
	<div class='fake_aba'>Trocar Senha: $usuario_->{'nome'} ($LOGUSUARIO) </div>
		<div class="navigateable_box">
		
		<form onSubmit='return false;'>
		<dl class=form>
			<div>
				<dt>Senha Atual</dt>
				<dd><input type='password' name='senha_atual' maxlength=500></dd>
			</div>
			<div>
				<dt>Nova Senha</dt>
				<dd><input type='password' name='senha_nova' maxlength=500></dd>
			</div>
			<div>
				<dt>Repetir Nova Senha</dt>
				<dd><input type='password' name='senha_nova_prova' maxlength=500></dd>
			</div>
		</dl>
		<input type="hidden" name="usuario" value="$LOGUSUARIO">
		</form>
		
		</div>
</div>
	
</body></html>
HTML

