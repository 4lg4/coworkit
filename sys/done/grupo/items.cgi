#!/usr/bin/perl

$nacess = '41';
require "../../cfg/init.pl";

$ID = &get('ID');
$PESQ = &get('PESQ');
$ADD = &get('ADD');
@item = &get_array('item[]');


print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML

if($ADD ne "")
	{
	$dbh->begin_work;
	$rv = $dbh->do("insert into tipo_grupo_item (descrp) values ('$ADD') ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão do atributo do grupo !!!");
		$dbh->rollback;
		exit;
		}
	$sth = $dbh->prepare("select currval('tipo_grupo_item_codigo_seq') ");
	$sth->execute;
	if($dbh->err ne "")
		{
		&erroDBH("Falha ao locallizar codigo sequencial do atributo do grupo!!!");
		$dbh->rollback;
		&erroDBR;
		}
	else
		{
		$rv4 = $sth->rows;
		if($rv4 == 1)
			{
			$row = $sth->fetch;
			$grupo_item_cod = @$row[0];
			}
		else
			{
			&erroDBH("Falha ao identificar o id do atributo do grupo!!!");
			$dbh->rollback;
			&erroDBR;
			}
		}
	$sth->finish;
	$rv = $dbh->do("insert into parceiro_tipo_grupo_item (parceiro, tipo_grupo_item) values ('$LOGEMPRESA', '$grupo_item_cod') ");
	if($dbh->err ne "")
		{
		&erroDBH("Falha na inclusão do atributo do grupo no parceiro!!!");
		$dbh->rollback;
		exit;
		}
	$dbh->commit;
	}

$SQL = "select * from tipo_grupo_item ";
$sth9 = &select("select * from pg_tables where tablename='parceiro_tipo_grupo_item'");
$rv9 = $sth9->rows();
if($rv9 > 0)
	{
	$SQL .= " join parceiro_tipo_grupo_item on tipo_grupo_item.codigo = parceiro_tipo_grupo_item.tipo_grupo_item and parceiro_tipo_grupo_item.parceiro = '$LOGEMPRESA' ";
	}


$SQL1 = "";
for($f=0; $f<@item; $f++)
	{
	if($item[$f] ne "")
		{
		$SQL1 .= "tipo_grupo_item.codigo != '$item[$f]' and "
		}
	}

if($SQL1 ne "")
	{
	$SQL1 = " where (".$SQL1;
	$SQL1 =~ s/ and $/)/;
	}

if($PESQ ne "")
	{
	if($SQL1 eq "")
		{
		$SQL1 .= " where ";
		}
	else
		{
		$SQL1 .= " and ";
		}
	$SQL1 .= " tipo_grupo_item.descrp <=> '%$PESQ%' ";
	}

$SQL = $SQL.$SQL1."order by descrp";
$sth3 = &select($SQL);
$rv3 = $sth3->rows();
$tipo_direito_list = "";
if($rv3 > 0)
	{
	while($row3 = $sth3->fetchrow_hashref)
		{
		print "<li class='ui-state-default' id='item_";
		print $row3->{'codigo'};
		print "'>";
		print $row3->{'descrp'};
		print "</li>";
		}
	}
print<<HTML;
</body></html>
HTML


exit;


