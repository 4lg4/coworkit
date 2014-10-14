#!/usr/bin/perl

$nacess = "902";
require "../../cfg/init.pl";
$COD = &get('cod');
$DT = &get('dt');
$OBS = &get('obs');
$CIENTE = &get('ciente');
if(lc($CIENTE) ne "true")
	{
	$CIENTE = "false";
	}

print "Content-type: text/javascript\n\n";

if($COD eq "" || $DT eq "")
	{
	print "top.alerta('Acesso Negado!');";
	exit;
	}

$sth = &select("select * from cron_historico_check where cron='$COD' and dt='$DT' ");
$rv = $sth->rows();
if($rv > 0)
	{
	$rv = $dbh->do("update cron_historico_check set usuario_cad='$LOGUSUARIO', dt_cad=now(), obs='$OBS', ciente='$CIENTE' where cron='$COD' and dt='$DT' ");
	}
else
	{
	$rv = $dbh->do("insert into cron_historico_check (cron, dt, usuario_cad, dt_cad, obs, ciente) values ('$COD', '$DT', '$LOGUSUARIO',  now(), '$OBS', '$CIENTE')");
	}
if($dbh->err ne "")
	{
	print "top.alerta('Erro!\\n".$dbh->errstr."\\n');";
	}
else
	{
	print "top.unLoading();";
	}
exit;

