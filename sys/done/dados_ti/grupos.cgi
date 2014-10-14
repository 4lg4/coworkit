#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_empresa');
$ENDERECO = &get('cod_endereco');
$MODO = &get('MODO');
$AGRUPO = &get('agrupo');

print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>
HTML

if($AGRUPO ne "")
	{
	$SQL = "select distinct grupo.codigo, grupo.descrp, grupo_empresa.empresa from grupo join agrupo_grupo on grupo.codigo = agrupo_grupo.grupo ";
	$sth9 = &select("select * from pg_tables where tablename='parceiro_grupo'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		$SQL .= " join parceiro_grupo on grupo.codigo = parceiro_grupo.grupo and parceiro_grupo.parceiro = '$LOGEMPRESA' ";
		}
	$SQL .= " left join grupo_empresa on grupo.codigo = grupo_empresa.grupo ";
	if($COD > 0)
		{
		$SQL .= " and grupo_empresa.empresa = '$COD' and grupo_empresa.endereco = '$ENDERECO' ";
		}
	if($AGRUPO =~ /[0-9]/)
		{
		$SQL .= " where agrupo_grupo.agrupo = '$AGRUPO' ";
		}

	$SQL = $SQL."order by grupo.descrp";
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	if($rv3 < 1)
		{
		print "Nenhum grupo cadastrado!<br><a href='javascript:top.grid(\"grupo\")'>Clique aqui para cadastrar</a>...";
		}
	else
		{
		print "<table width=100% cellpadding=5 cellspacing=0 border=0 id='tbgrupo_$ENDERECO' align='center'><tbody>";
		$last = "";
		while($row3 = $sth3->fetchrow_hashref)
			{
			if($last ne $row3->{'codigo'})
				{
				if($ENDERECO eq "0")
					{
					print "<tr id='".$row3->{'codigo'}."' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_emp(\"".$row3->{'codigo'}."\", \"$ENDERECO\"); screenRefresh(\"tbgrupo_$ENDERECO\",\"".$row3->{'codigo'}."\"); }'><td";
					}
				else
					{
					print "<tr id='".$row3->{'codigo'}."' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_item(\"".$row3->{'codigo'}."\", \"$ENDERECO\"); screenRefresh(\"tbgrupo_$ENDERECO\",\"".$row3->{'codigo'}."\"); }'><td";
					}
				if($row3->{'empresa'} ne "")
					{
					print " style='font-weight: bold'";
					}
				print ">";
				print $row3->{'descrp'};
				print "</td></tr>";
				}
			$last = $row3->{'codigo'};
			}
		print "</table>";
		}
	}
print<<HTML;
</body></html>
HTML


exit;


