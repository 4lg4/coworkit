#!/usr/bin/perl

$nacess = "41' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";

$COD = &get('COD');

if($COD eq "")
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
	parent.hide('icon_edit');
	parent.hide('icon_print');
	parent.hide('icon_insert');
	parent.hide('icon_delete');
	parent.hide('icon_save');
	parent.hide('icon_cancel');
	
	function START()
		{
		return true;
		}
  </script>
</head>
<body onLoad="START()">
HTML

$dbh->begin_work;
if($COD ne "")
	{
	# Apaga o grupo
	$rv = $dbh->do("delete from grupo where codigo = '$COD' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na exclusão do grupo!!!");
		$dbh->rollback;
		exit;
		}

	$dbh->commit;
	print "<br><br><br><center>Atualização efetuada com sucesso!</center>";
	}

print<<HTML;
<script language='JavaScript'>
	function START(){
		top.callGrid('grupo');
	}
</script>
</body></html>
HTML

