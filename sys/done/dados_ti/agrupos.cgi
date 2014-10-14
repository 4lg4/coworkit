#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_empresa');
$ENDERECO = &get('cod_endereco');
$MODO = &get('MODO');


print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML

$SQL = "select distinct agrupo.codigo, agrupo.descrp, grupo_empresa.empresa as empresa from agrupo ";
$SQL .= " join agrupo_grupo on agrupo.codigo = agrupo_grupo.agrupo ";
$sth9 = &select("select * from pg_tables where tablename='parceiro_agrupo'");
$rv9 = $sth9->rows();
if($rv9 > 0)
	{
	$SQL .= " join parceiro_agrupo on agrupo.codigo = parceiro_agrupo.agrupo and parceiro_agrupo.parceiro = '$LOGEMPRESA' ";
	}
$SQL .= "left join grupo_empresa on agrupo_grupo.grupo = grupo_empresa.grupo ";
if($COD > 0)
	{
	$SQL .= " and grupo_empresa.empresa = '$COD' and grupo_empresa.endereco = '$ENDERECO' ";
	}
$SQL = $SQL."order by descrp, empresa";
$sth3 = &select($SQL);
$rv3 = $sth3->rows();
if($rv3 < 1)
	{
	print "Nenhum agrupamento cadastrado!<br><a href='javascript:top.grid(\"agrupo\")'>Clique aqui para cadastrar</a>...";
	}
else
	{
	print "<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbagrupo_$ENDERECO' align='center'><tbody>";
	$last = "";
	while($row3 = $sth3->fetchrow_hashref)
		{
		if($last ne $row3->{'codigo'})
			{
			$last = $row3->{'codigo'};
			print "<tr id='$row3->{'codigo'}' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_grupo(\"$row3->{'codigo'}\", \"$ENDERECO\"); screenRefresh(\"tbagrupo_$ENDERECO\",\"$row3->{'codigo'}\"); }'><td";
			if($row3->{'empresa'} ne "")
				{
				print " style='font-weight: bold'";
				}
			print ">";
			print $row3->{'descrp'};
			print "</td></tr>";
			}
		}
	for($f=0; $f<1; $f++)
		{
		print "<tr><td>&nbsp;</td></tr>";
		}
	print "</tbody></table>";
	}
print<<HTML;
</body></html>
HTML


exit;


