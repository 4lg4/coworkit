#!/usr/bin/perl

$nacess = '';
require "../../cfg/init.pl";
$COD = &get('COD');
$SHOW = &get('SHOW');
if($SHOW eq "usuarios")
	{
	$TABLE = "usuario";
	$CHAVE = "usuario";
	}
elsif($SHOW =~ /^sac_/)
	{
	$TABLE = "sac";
	$CHAVE = "codigo";
	}
else
	{
	$TABLE = $SHOW;
	$CHAVE = "codigo";
	}

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
	top.ac_show();
	
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
	$sth9 = &select("select * from pg_tables where tablename='parceiro_$TABLE'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		# Apaga o registro no parceiro
		$rv = $dbh->do("delete from $TABLE where $CHAVE = '$COD' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do registro no parceiro!!!");
			$dbh->rollback;
			exit;
			}
		}

	# Apaga o registro
	$rv = $dbh->do("delete from $TABLE where $CHAVE = '$COD' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na exclusão do registro!!!");
		$dbh->rollback;
		exit;
		}

	$dbh->commit;
	print "<script>alerta('Registro excluido com sucesso!');</script>";
	}

print<<HTML;
<script language='JavaScript'>

	top.callRegrid('$SHOW');

</script>
</body></html>
HTML

