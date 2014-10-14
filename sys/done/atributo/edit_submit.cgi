#!/usr/bin/perl

$nacess = '27';
require "../../cfg/init.pl";
$SHOW = &get('SHOW');
$CODIGO = &get('COD');


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
$TABLE = "tipo_grupo_item";
$SHOW = "tipo_grupo_item";

if($CODIGO eq "")
	{
	$SQL1 = "insert into $TABLE (";
	$SQL2 = " (";
	}
else
	{
	$SQL1 = "update $TABLE set ";
	$SQL2 = "";
	}

if($ID eq "")
	{
	print $query->header({charset=>utf8});
	print "Requisição inválida";
	exit;
	}

@campo = $query->param();
for($f=0;$f<@campo;$f++)
	{
	if($campo[$f] ne "ID" && $campo[$f] ne "THIS" && $campo[$f] ne "COD" && $campo[$f] ne "MODO" && $campo[$f] ne "SHOW" && $campo[$f] ne "FORCE")
		{
		if($CODIGO eq "")
			{
			if(&get($campo[$f]) ne "")
				{
				$SQL1 .= $campo[$f].", ";
				$SQL2 .= "'".&get($campo[$f])."', ";
				}
			}
		else
			{
			$SQL1 .= $campo[$f] .= "='".&get($campo[$f])."', ";
			}
		}
	}

$SQL1 =~ s/, $//;
$SQL2 =~ s/, $//;

if($CODIGO eq "")
	{
	$SQL1 .= ") values ";
	$SQL2 .= ")";
	}
else
	{
	$SQL1 .= "";
	$SQL2 .= " where $CHAVE = '$CODIGO' ";
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
$rv = $dbh->do($SQL1.$SQL2);
if($dbh->err ne "")
	{
	&erroDBH("Falha no processamento da $SHOW ($SQL1.$SQL2)!!!");
	$dbh->rollback;
	exit;
	}
if($CODIGO eq "")
	{
	$sth8 = $dbh->prepare("select currval('".$TABLE."_codigo_seq') ");
	$sth8->execute;
	if($dbh->err ne "")
		{
		&erroDBH("Falha ao identificar o código da $TABLE!!!");
		$dbh->rollback;
		exit;
		}
	else
		{
		$rv8 = $sth8->rows;
		if($rv8 == 1)
			{
			$row8 = $sth8->fetch;
			$CODIGO = @$row8[0];
			}
		else
			{
			&erroDBH("Falha ao encontrar o código da $TABLE!!!");
			$dbh->rollback;
			exit;
			}
		}
	$sth9 = &select("select * from pg_tables where tablename='parceiro_$TABLE'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		# Cria vínculo com parceiro
		$rv = $dbh->do("insert into parceiro_$TABLE (parceiro, $TABLE) values ('$LOGEMPRESA', '$CODIGO') ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inclusão do $TABLE no parceiro!!!");
			$dbh->rollback;
			exit;
			}
		}
	}


$dbh->commit;
print "<br><br><br><center>Atualização efetuada com sucesso!</center>";

print<<HTML;
<script language='JavaScript'>
	function START()
		{
		top.callGrid('$SHOW');
		}
</script>
</body></html>
HTML

