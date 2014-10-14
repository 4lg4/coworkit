#!/usr/bin/perl

# define acesso ao modulo -----------------------------------------------------
$nacess = "801' and usuario_menu.tipo = 'a";
require "../../cfg/init.pl";

# pega variaveis ---------------------------------------------------------------
$senha_atual = &get('senha_atual');
$senha_nova = &get('senha_nova');
$usuario = &get('usuario');

if($usuario eq "" || $senha_atual eq "" || $senha_nova eq "")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/CSS_syscall/form.css" rel="stylesheet" type="text/css">
  <script language='JavaScript'>
	top.ac_show();
	
	function START()
		{
		return true;
		}
  </script>
</head>
<body onLoad="START()">
HTML

# Update Senha do usuário --------------------------------------------------
$SQL = "update usuario set senha=password('$senha_nova') where usuario='$usuario' and senha=password('$senha_atual')";
$rv = $dbh->do($SQL);
if($dbh->err ne "")
	{
	&erroDBH("Falha na alteração da senha do usuário");
	exit;
	}
else
	{
	if($rv < 1)
		{
		&erroDBH("Acesso negado");
		exit;
		}
	}
		
print "<br><br><br><center>Atualização efetuada com sucesso!</center>";

print<<HTML;
<script language='JavaScript'>
	function START()
		{
		top.regrid('usuarios');
		}
</script>
</body></html>
HTML

