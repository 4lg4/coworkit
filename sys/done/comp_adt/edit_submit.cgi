#!/usr/bin/perl

#$nacess = "404' and usuario_direitos.tipo = 'a";
$nacess = "27";
require "../../cfg/init.pl";
$ID = &get('ID');
$FORCE = &get('FORCE');
@item = &get_array('item[]');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="stylesheet" href="/css/form.css" rel="stylesheet" type="text/css">
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
$SQL = "";
$c = 1;
$sth9 = &select("select * from information_schema.columns where table_name = 'comp_item' and column_name = 'parceiro' ");
$rv9 = $sth9->rows();
if($rv9 > 0)
	{
	$SQL2 .= " and parceiro = '$LOGEMPRESA' ";
	}
else
	{
	$SQL2 = "";
	}
for($f=0; $f<@item; $f++)
	{
	if($item[$f] ne "")
		{
		$SQL .= " and tipo != '$item[$f]' ";

		$sth = $dbh->prepare("select * from comp_item where tipo = '$item[$f]' $SQL2 ");
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
				if($SQL2 ne "")
					{
					$rv = $dbh->do("insert into comp_item (parceiro, tipo, seq) values ('$LOGEMPRESA', '$item[$f]', '$c') ");
					}
				else
					{
					$rv = $dbh->do("insert into comp_item (tipo, seq) values ('$item[$f]', '$c') ");
					}
				if($dbh->err ne "")
					{
					&erroDBH("Falha na alteração dos itens do grupo!!!");
					$dbh->rollback;
					exit;
					}
				}
			else
				{
				$rv = $dbh->do("update comp_item set seq='$c' where tipo = '$item[$f]' $SQL2 ");
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
	$SQL =~ s/^ and//;
	# Exclui itens do grupo removidos
	if($FORCE eq "S")
		{
		$sth2 = $dbh->prepare("select * from comp_item where $SQL $SQL2 ");
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
						$rv = $dbh->do("delete from empresa_comp_adicional where comp_item = '".$row2->{'tipo'}."' ");
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

	$rv = $dbh->do("delete from comp_item where $SQL $SQL2 ");
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
	function START()
		{
		top.call('/sys/done/comp_adt/edit.cgi');
		}
	START();
</script>
</body></html>
HTML

