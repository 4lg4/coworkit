#!/usr/bin/perl

$nacess = '42';
require "../../cfg/init.pl";

$ID = &get('ID');
$PESQ = &get('PESQ');
@grupo = &get_array('grupo[]');


print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML

$SQL = "select * from grupo ";
$sth9 = &select("select * from pg_tables where tablename='parceiro_grupo'");
$rv9 = $sth9->rows();
if($rv9 > 0)
	{
	$SQL .= "join parceiro_grupo on grupo.codigo = parceiro_grupo.grupo and parceiro_grupo.parceiro = '$LOGEMPRESA' ";
	}

$SQL1 = "";
for($f=0; $f<@grupo; $f++)
	{
	if($grupo[$f] ne "")
		{
		$SQL1 .= "grupo.codigo != '$grupo[$f]' and "
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
	$SQL1 .= " grupo.descrp <=> '%$PESQ%' ";
	}

$SQL = $SQL.$SQL1."order by descrp";
$sth3 = &select($SQL);
$rv3 = $sth3->rows();
$tipo_direito_list = "";
if($rv3 < 1)
	{
	print "Nenhum grupo cadastrado!";
	}
else
	{
	while($row3 = $sth3->fetchrow_hashref)
		{
		print "<li class='ui-state-default' id='grupo_";
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


