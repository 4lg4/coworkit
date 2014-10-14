#!/usr/bin/perl

$nacess = '204';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('COD');
if($COD eq "undefinied")
	{
	$COD = "";
	}
$ENDERECO = &get('cod_endereco');
$BOX = &get('box');
if($BOX eq "")
	{
	$BOX = $ENDERECO;
	}
$MODO = &get('MODO');
$GRUPO = &get('grupo');
if($GRUPO eq "undefined")
	{
	$GRUPO = "";
	}
$PESQ = &get('PESQEMP');
$ORDER = &get('ORDER_LISTEMP');
if($ORDER eq "" || $ORDER eq "linha")
	{
	$ORDER = "nome_emp";
	}

print "Content-type: text/html\n\n";
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
</head>
<body>

HTML

if($GRUPO ne "")
	{
	$SQL = "select *, empresa.codigo as cod_emp, empresa.nome as nome_emp, empresa_endereco.codigo as end_cod, empresa_endereco.endereco as rua, tipo_endereco.descrp as tipo_end from grupo_empresa join empresa_endereco on grupo_empresa.empresa = empresa_endereco.empresa and grupo_empresa.endereco = empresa_endereco.codigo join empresa on empresa.codigo = empresa_endereco.empresa join tipo_endereco on empresa_endereco.tipo = tipo_endereco.codigo ";
	$sth9 = &select("select * from pg_tables where tablename='parceiro_empresa'");
	$rv9 = $sth9->rows();
	if($rv9 > 0)
		{
		$SQL .= " join parceiro_empresa on empresa.codigo = parceiro_empresa.empresa and parceiro_empresa.parceiro = '$LOGEMPRESA' ";
		}
	$SQL .= " where grupo_empresa.grupo = '$GRUPO' ";
	if($PESQ ne "")
		{
		$SQL .= " and (empresa.nome <=> '%$PESQ%' or empresa.apelido <=> '%$PESQ%') ";
		}
	$SQL .= "order by ".$ORDER;
	if($ORDER ne "rua")
		{
		if($ORDER =~ /desc/)
			{
			$SQL .= ", rua desc";
			}
		else
			{
			$SQL .= ", rua";
			}
		}
        
    
	$sth = &select($SQL);
	$rv = $sth->rows();
	if($rv < 1)
		{
		print "Nenhum item cadastrado!";
		}
	else
		{
		print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tbemp_$BOX' class='navigateable' align='center'><thead><tr>";
		print "<th ";
		if($ORDER eq "cod_emp")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "cod_emp desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print "onClick=\"orderbyemp('$GRUPO', '$ENDERECO', 'cod_emp')\">Código</th><th ";
		if($ORDER eq "nome_emp")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "nome_emp desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print "onClick=\"orderbyemp('$GRUPO', '$ENDERECO', 'nome_emp')\">Nome</th><th ";
		if($ORDER eq "apelido")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "apelido desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print "onClick=\"orderbyemp('$GRUPO', '$ENDERECO', 'apelido')\">Apelido</th><th ";
		if($ORDER eq "rua")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "rua desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print "onClick=\"orderbyemp('$GRUPO', '$ENDERECO', 'rua')\">Endereço</th><th ";
		if($ORDER eq "cidade")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "cidade desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print "onClick=\"orderbyemp('$GRUPO', '$ENDERECO', 'cidade')\">Cidade</th><th ";
		if($ORDER eq "uf")
			{
			print " class='asc'";
			}
		elsif($ORDER eq "uf desc")
			{
			print " class='desc'";
			}
		else
			{
			print " class='thor'";
			}
		print "onClick=\"orderbyemp('$GRUPO', '$ENDERECO', 'uf')\">Estado</th>";
		print "</tr></thead><tbody>";
		
		$last = "";
		while($row = $sth->fetchrow_hashref)
			{
			if($last ne $row->{'end_cod'})
				{
				print "<tr id='".$row->{'end_cod'}."' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_item(\"$GRUPO\", \"".$row->{'end_cod'}."\", \"".$row->{'cod_emp'}."\"); screenRefresh(\"tbemp_$BOX\",\"".$row->{'end_cod'}."\"); }'>";
				print "<td>$row->{'cod_emp'}</td><td>$row->{'nome_emp'}</td><td>$row->{'apelido'}</td><td>$row->{'rua'}</td><td>$row->{'cidade'}</td><td>".uc($row->{'uf'})."</td>";
				print "</tr>";
				}
			if($last eq "")
				{
				print "<script language='JavaScript'>\n";
				print "get_item(\"$GRUPO\", \"".$row->{'end_cod'}."\", \"".$row->{'cod_emp'}."\"); screenRefresh(\"tbemp_$BOX\",\"".$row->{'end_cod'}."\");\n";
				print "</script>\n";
				}
			$last = $row->{'end_cod'};
			}

		print "</tbody></table>";
		}
	}
print<<HTML;

<script>

</script>
</body></html>
HTML


exit;
