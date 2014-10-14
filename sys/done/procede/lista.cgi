#!/usr/bin/perl

$nacess = '206';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('cod_emp');
if($COD eq "")
	{
	$COD = &get('COD');
	}
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
$ACAO = &get('ACAO');
$CODPROCEDE = &get('codprocede_'.$BOX);
$TITULO = &get('titulo_'.$BOX);
$DESCRP = &get('descricao_'.$BOX);
$DESCRP = &get($DESCRP, 'NEW_LINE');
$DESCRP=~ s/\n/ /gm;
$DESCRP=~ s/"//gm;
$DESCRP=~ s/\r/ /gm;
$PESQ = &get('PESQ_'.$BOX);
$ORDER = &get('ORDER_LISTIT');
if($ORDER eq "")
	{
	$ORDER = "titulo";
	}

if($LOGUSUARIO eq "admin")
	{
	$nacess_tipo = "s";
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

if($ENDERECO ne "")
	{
	if($CODPROCEDE ne "" && $ACAO eq "delete")
		{
		$rv = $dbh->do("delete from endereco_procedimentos where endereco_procedimentos.codigo = '$CODPROCEDE' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do procedimento!!!");
			exit;
			}
		}
	elsif($CODPROCEDE ne "" && $ACAO eq "save" && $TITULO ne "")
		{
		$rv = $dbh->do("update endereco_procedimentos set titulo='$TITULO', descrp='$DESCRP' where endereco_procedimentos.codigo = '$CODPROCEDE' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na alteração do procedimento!!!");
			exit;
			}
		}
	elsif($ACAO eq "save" && $TITULO ne "")
		{
		$rv = $dbh->do("insert into endereco_procedimentos (endereco, titulo, descrp) values ('$ENDERECO', '$TITULO', '$DESCRP') ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inclusão do procedimento!!! insert into endereco_procedimentos (endereco, titulo, descrp) values ('$ENDERECO', '$TITULO', '$DESCRP') ");
			exit;
			}
			
		}


	# Lista os procedimentos
	$SQL = "select * from endereco_procedimentos where endereco_procedimentos.endereco = '$ENDERECO' ";
	if($PESQ ne "")
		{
		$SQL .= " and titulo <=> '%$PESQ%' ";
		}
	$SQL .= "order by ".$ORDER;
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	if($rv3 < 1)
		{
		print "Nenhum item cadastrado!";
		}
	else
		{
		print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tbitem_$BOX' class='navigateable' align='center'><thead><tr>";
		print "<th";
		if($ORDER eq "titulo")
			{
			print " class='asc' onClick=\"orderby('$ENDERECO', 'titulo desc')\">";
			}
		elsif($ORDER eq "titulo desc")
			{
			print " class='desc' onClick=\"orderby('$ENDERECO', 'titulo')\">";
			}
		else
			{
			print " class='thor' onClick=\"orderby('$ENDERECO', 'titulo')\">";
			}
		print "Titulo</th></tr></thead><tbody>";

		while($row3 = $sth3->fetchrow_hashref)
			{
			print "<tr id='$row3->{'codigo'}'><td onClick=\"get_detail('".$row3->{'codigo'}."', '$ENDERECO')\">".$row3->{'titulo'}."&nbsp;</td></tr>";
			}

		print "</tbody></table>";
		if($ACAO ne "delete")
			{
			if($CODPROCEDE eq "" && $TITULO eq "")
				{
				print "<script language='JavaScript'>\n";
				print "get_detail(\$('#tbitem_$ENDERECO tbody tr:first').attr('id'), '$ENDERECO');\n";
				print "screenRefresh('tbitem_$ENDERECO', '0');\n";
				print "</script>\n";
				}
			}
		}
	}
print<<HTML;
</body></html>
HTML

exit;
