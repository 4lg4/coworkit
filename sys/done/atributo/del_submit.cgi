#!/usr/bin/perl

$nacess = "27";
require "../../cfg/init.pl";
$COD = &get('COD');
$SHOW = &get('SHOW');
$FORCE = &get('FORCE');

$SHOW = "tipo_grupo_item";
$TABLE = "tipo_grupo_item";
$CHAVE = "codigo";


if($COD eq "" && $MODO ne "incluir")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

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
	if($FORCE eq "S")
		{
		$rv = $dbh->do("delete from grupo_empresa where grupo_item = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do atributo nos dados do grupo!!!");
			$dbh->rollback;
			exit;
			}
		$rv = $dbh->do("delete from grupo_item where tipo = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do atributo no grupo!!!");
			$dbh->rollback;
			exit;
			}

		$rv = $dbh->do("delete from empresa_comp_adicional where comp_item = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do atributo nos dados dos computadores!!!");
			$dbh->rollback;
			exit;
			}
		$rv = $dbh->do("delete from comp_item where tipo = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do atributo no grupo computadores!!!");
			$dbh->rollback;
			exit;
			}

		$rv = $dbh->do("delete from empresa_user_adicional where user_item = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do atributo nos dados dos usuários!!!");
			$dbh->rollback;
			exit;
			}
		$rv = $dbh->do("delete from user_item where tipo = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do atributo no grupo usuários!!!");
			$dbh->rollback;
			exit;
			}

		}

	# Apaga o atributo
	$rv = $dbh->do("delete from $TABLE where $CHAVE = '$COD' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na exclusão do atributo!!!");
		$dbh->rollback;
		exit;
		}

	$dbh->commit;
	print "<br><br><br><center>Atualização efetuada com sucesso!</center>";
	}

print<<HTML;
<script language='JavaScript'>
	function START()
		{
		top.callGrid('$SHOW');
		}
</script>
</body></html>
HTML

