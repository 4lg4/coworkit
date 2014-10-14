#!/usr/bin/perl

$nacess = "42' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";
$ID = &get('ID');
$COD = &get('COD');
$codigo = &get('codigo');
$nome = &get('nome');
@grupo = &get_array('grupo[]');

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
	# Update Dados do agrupo
	$rv = $dbh->do("update agrupo set descrp='$nome' where codigo = '$COD' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na alteração do agrupamento!!!");
		$dbh->rollback;
		exit;
		}
	}
else
	{
	# Insert Dados do grupo
	$rv = $dbh->do("insert into agrupo (descrp) values ('$nome') ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão do agrupamento!!!");
		$dbh->rollback;
		exit;
		}
	$sth = $dbh->prepare("select currval('agrupo_codigo_seq') ");
	$sth->execute;
	if($dbh->err ne "")
		{
		&erroDBH("Falha ao identificar o código do agrupamento!!!");
		$dbh->rollback;
		&erroDBR;
		}
	else
		{
		$rv = $sth->rows;
		if($rv == 1)
			{
			$row = $sth->fetch;
			$COD = @$row[0];
			}
		else
			{
			&erroDBH("Falha ao identificar o código do agrupamento!!!");
			$dbh->rollback;
			&erroDBR;
			}
		}
	$sth->finish;

	$sth9 = &select("select * from pg_tables where tablename='parceiro_agrupo'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		# Cria vínculo com parceiro
		$rv = $dbh->do("insert into parceiro_agrupo (parceiro, agrupo) values ('$LOGEMPRESA', '$COD') ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inclusão do agrupamento parceiro!!!");
			$dbh->rollback;
			exit;
			}
		}

	}

# Itens do grupo
$rv = $dbh->do("delete from agrupo_grupo where agrupo = '$COD' ");
if($dbh->err ne "")
	{
	&erroDBH("Falha na inicialização dos grupos do agrupamento!!!");
	$dbh->rollback;
	exit;
	}

$c=0;
for($f=0; $f<@grupo; $f++)
	{
	if($grupo[$f] ne "")
		{
		$rv = $dbh->do("insert into agrupo_grupo (agrupo, grupo, seq) values ('$COD', '$grupo[$f]', '$c') ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na alteração dos grupos do agrupamento!!!");
			$dbh->rollback;
			exit;
			}
		$c++;
		}
	}

	
$dbh->commit;
print<<HTML;
<script>
    console.log("agrupo salvo");
    top.callGrid('agrupo');
</script>
</body></html>
HTML

