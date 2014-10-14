#!/usr/bin/perl

$nacess = "41' and usuario_menu.direito = 'a";
require "../../cfg/init.pl";
$ID = &get('ID');
$COD = &get('COD');
$FORCE = &get('FORCE');
$codigo = &get('codigo');
$nome = &get('nome');
$exportar = &get('exportar');
if($exportar eq "")
	{
	$exportar = 0;
	}
@item = &get_array('item[]');

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
	# Update Dados do grupo
	$rv = $dbh->do("update grupo set descrp='$nome', exportar='$exportar' where codigo = '$COD' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na alteração do grupo!!!");
		$dbh->rollback;
		exit;
		}
	}
else
	{
	# Insert Dados do grupo
	$rv = $dbh->do("insert into grupo (descrp, exportar) values ('$nome', '$exportar') ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão do grupo!!!");
		$dbh->rollback;
		exit;
		}
	$sth = $dbh->prepare("select currval('grupo_codigo_seq') ");
	$sth->execute;
	if($dbh->err ne "")
		{
		&erroDBH("Falha ao identificar o código do grupo!!!");
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
			&erroDBH("Falha ao identificar o código do grupo!!!");
			$dbh->rollback;
			&erroDBR;
			}
		}

	$sth9 = &select("select * from pg_tables where tablename='parceiro_grupo'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		# Cria vínculo com parceiro
		$rv = $dbh->do("insert into parceiro_grupo (parceiro, grupo) values ('$LOGEMPRESA', '$COD') ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inclusão do grupo parceiro!!!");
			$dbh->rollback;
			exit;
			}
		}

	$sth->finish;
	}

# Itens do grupo
#$rv = $dbh->do("delete from grupo_item where grupo = '$COD' ");
#if($dbh->err ne "")
#	{
#	&erroDBH("Falha na inicialização dos itens do grupo!!!");
#	$dbh->rollback;
#	exit;
#	}
	
$SQL = "";
$c = 1;
for($f=0; $f<@item; $f++)
	{
	if($item[$f] ne "")
		{
		$SQL .= " and tipo != '$item[$f]' ";

		$sth = $dbh->prepare("select * from grupo_item where grupo = '$COD' and tipo = '$item[$f]' ");
		$sth->execute;
		if($dbh->err ne "")
			{
			&erroDBH("Falha ao identificar se o atributo já existe!!!");
			$dbh->rollback;
			&erroDBR;
			}
		else
			{
			$rv = $sth->rows;
			if($rv == 0)
				{
				$rv = $dbh->do("insert into grupo_item (grupo, tipo, seq) values ('$COD', '$item[$f]', '$c') ");
				if($dbh->err ne "")
					{
					&erroDBH("Falha na alteração dos itens do grupo!!!");
					$dbh->rollback;
					exit;
					}
				}
			else
				{
				$rv = $dbh->do("update grupo_item set seq='$c' where grupo = '$COD' and tipo = '$item[$f]' ");
				if($dbh->err ne "")
					{
					&erroDBH("Falha na alteração dos itens do grupo!!!");
					$dbh->rollback;
					exit;
					}
				}
			$c++;
			}
		}
	}

if($SQL ne "")
	{
	# Exclui itens do grupo
	if($FORCE eq "S")
		{
		$sth2 = $dbh->prepare("select * from grupo_item where grupo = '$COD' $SQL ");
		$sth2->execute;
		if($dbh->err ne "")
			{
			&erroDBH("Falha ao identificar os atributos excluídos!!!");
			$dbh->rollback;
			&erroDBR;
			}
		else
			{
			$rv2 = $sth2->rows;
			if($rv2 > 0)
				{
				while($row2 = $sth2->fetchrow_hashref)
					{
					if($row2->{'tipo'} ne "")
						{
						$rv = $dbh->do("delete from grupo_empresa where grupo = '$COD' and grupo_item = '".$row2->{'tipo'}."' ");
						if($dbh->err ne "")
							{
							&erroDBH("Falha na exclusão dos itens do grupo!!!");
							$dbh->rollback;
							exit;
							}
						}
					}
				}
			}
		}

	$rv = $dbh->do("delete from grupo_item where grupo = '$COD' $SQL ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na exclusão dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	}
else
	{
	$rv = $dbh->do("delete from grupo_item where grupo = '$COD' ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na exclusão dos itens do grupo!!!");
		$dbh->rollback;
		exit;
		}
	}


	
$dbh->commit;
print "<br><br><br><center>Atualização efetuada com sucesso!</center>";

print<<HTML;
<script language='JavaScript'>
	function START() {
		top.callGrid('grupo');
	}
	START();
</script>
</body></html>
HTML

