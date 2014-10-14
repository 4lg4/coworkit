#!/usr/bin/perl

$nacess = '902';
require "../../cfg/init.pl";

$ID = &get('ID');
$COD = &get('COD');
$ENDERECO = &get('cod_endereco');
$MODO = &get('MODO');
$ACAO = &get('ACAO');
$PESQ = &get('PESQ');
$ORDER = &get('ORDER_LISTIT');
if($ORDER eq "")
	{
	$ORDER = "codigo";
	}
$CRON = &get('cron_codigo');
$HIDDEN = &get('cron_hidden');
if($HIDDEN eq "")
	{
	$HIDDEN = "0";
	}
$TIPO = &get('cron_tipo');
$DESCRP = &get('cron_descrp');
$TMIN = &get('cron_tmin');
$TMAX = &get('cron_tmax');

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
	if($CRON ne "" && $ACAO eq "delete")
		{
		$rv = $dbh->do("delete from cron where cron.codigo = '$CRON' and cron.endereco = '$ENDERECO' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na exclusão do monitoramento!!!");
			exit;
			}
		}
	elsif($CRON ne "" && $ACAO eq "save")
		{
		$rv = $dbh->do("update cron set hidden='$HIDDEN', endereco='$ENDERECO', tipo='$TIPO', descrp='$DESCRP', tmin='$TMIN', tmax='$TMAX' where cron.codigo = '$CRON' ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na alteração do monitoramento!!!");
			exit;
			}
		}
	elsif($ACAO eq "save")
		{
		$rv = $dbh->do("insert into cron (endereco, tipo, descrp, tmin, tmax, hidden) values ('$ENDERECO', '$TIPO', '$DESCRP', '$TMIN', '$TMAX', '$HIDDEN') ");
		if($dbh->err ne "")
			{
			&erroDBH("Falha na inclusão do monitoramento!!!");
			exit;
			}
		}

	$SQL = "select *, cron.codigo as cron_codigo, cron.descrp as cron_descrp, to_char(cron.dtcad, 'DD/MM/YYYY às HH24:MI:SSh') as dtcad_formatada, tipo_cron.descrp as tipo_descr from cron left join tipo_cron on cron.tipo = tipo_cron.codigo where cron.endereco = '$ENDERECO' ";
	if($PESQ ne "")
		{
		$SQL .= " and cron.descrp <=> '%$PESQ%' "; 
		}
	$SQL .= " order by cron.$ORDER ";
	$sth3 = &select($SQL);
	$rv3 = $sth3->rows();
	if($rv3 < 1)
		{
		print "Nenhum monitoramento de tarefa cadastrado!";
		}
	else
		{
		print "<table width=100% cellpadding=4 cellspacing=2 border=0 id='tbcron_$ENDERECO' class='navigateable' align='center'><thead><tr>";
		print "<th>Código</th><th>Chave</th><th>Tipo</th><th>Descrição</th><th width=150>Data Cadastro</th>";
		print "</tr></thead><tbody>";
		while($row3 = $sth3->fetchrow_hashref)
			{
			print "<tr id='".$row3->{'cron_codigo'}."' onClick='if(parent.bloqueado == true) { parent.unblock(); } else { get_detail(\"".$row3->{'cron_codigo'}."\", \"$ENDERECO\"); screenRefresh(\"tbcron_$ENDERECO\",\"".$row3->{'cron_codigo'}."\"); }'><td>".$row3->{'cron_codigo'}."</td><td>".$row3->{'chave'}."</td><td>".$row3->{'tipo_descr'}."</td><td>".$row3->{'cron_descrp'}."</td><td>".$row3->{'dtcad_formatada'}."</td></tr>";
			}
		print "</tbody></table>";
		}
	}


print<<HTML;
</body></html>
HTML


exit;
