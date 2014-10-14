#!/usr/bin/perl

use Time::Local;

$nacess = "902";
require "../../cfg/init.pl";
$COD = &get('cod');
$DT = &get('dt');

print $query->header({charset=>utf8});

if($COD eq "" || $DT eq "")
	{
	print "";
	exit;
	}

print "<table width=100% border=0 cellpadding=4 cellspacing=0 class='navigateable' style='margin-top: 1px;'>";
#print "<tr><td colspan=2 align=right onClick='if(t1)t1.Hide(event)'>fechar</td></tr>";
$SQL3 = "select *, to_char(cron_historico.dt, 'HH24:MI:SS') as dt_hora, cron_historico.descrp as historico from cron_historico join cron on cron_historico.cron = cron.codigo ";
$SQL3 .= " where to_char(cron_historico.dt, 'YYYY-MM-DD') = '".$DT."' and cron.codigo = '".$COD."' ";
$SQL3 .= " order by dt ";
$sth3 = &select($SQL3);
$rv3 = $sth3->rows();
if($rv3 > 0)
	{
	$cor = "#bfbfbf";
	while($row3 = $sth3->fetchrow_hashref)
		{
		print "<tr><td style='width: 60px; font-size: 9px;'><nobr><b>".$row3->{'dt_hora'}."&nbsp;h</b></nobr></td><td style='font-size: 9px;'>".$row3->{'historico'}."</td></tr>";
		}
	}
elsif($rv3 == 0)
	{
	print "<tr><td align=center colspan=2 style='border: none 0px'><br><br><br><nobr><b>Não executado</b></nobr><br><br></td></tr>";
	}
print "</table><br>";
