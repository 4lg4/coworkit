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

$sth = &select("select *, usuario.nome as nome_usuario, to_char(dt_cad, 'DD/MM/YYYY às HH24:MIh') as dt_cad_formatada from cron_historico_check join usuario on cron_historico_check.usuario_cad = usuario.usuario where cron='$COD' and dt='$DT' order by DT desc limit 1 ");
$rv = $sth->rows();
if($rv > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		if($row->{'ciente'})
			{
			if($row->{'obs'} ne "")
				{
				print "Comentários:<br>";
				print "<div style='color: black; background-color: white; padding: 2px; height: 30px; overflow: auto;'>".$row->{'obs'}."<br><br><br></div><br clear=all>";
				}
			print "<div style='float: left; vertical-align: top;'><input type='checkbox' name='ciente' value='true' style='margin-top: 0px' onClick='this.checked=1' checked></div><div style='width: 140px; float: left; vertical-align: top;'>Ciente: ";
			print $row->{'nome_usuario'};
			print " em ".$row->{'dt_cad_formatada'};
			print "</div><br><img src='$dir{img_syscall}/sair.png' border=0 style='float: right; vertical-align: bottom; margin-top: 1px;' onClick='t1.Hide(event); icon_reset();'>";
			}
		else
			{
			print "<span title='".$row->{'nome_usuario'}." em ".$row->{'dt_cad_formatada'}."'><b>Comentários:<b><br><textarea name='obs' style='width: 200px; -moz-border-radius: 5px; -webkit-border-radius: 5px; border-radius: 5px;' onkeyup='checkSubmit(event, \"$COD\",\"$DT\")'>".$row->{'obs'}."</textarea><br></span><nobr><input type='checkbox' name='ciente' value='true' style='vertical-align: sub'>Estou ciente desse erro</nobr> <br><img src='$dir{img_syscall}/sair_salvar.png' border=0 style='float: right' onClick='t1.Hide(event); save_status(\"$COD\",\"$DT\");'>";
			}
		}
	}
else
	{
print<<HTML;
<b>Comentários:<b><br><textarea name='obs' style='width: 215px; margin-left: -5px;' onkeyup='checkSubmit(event, "$COD","$DT")'></textarea><br><nobr><input type='checkbox' name='ciente' value='true' style='vertical-align: sub'>Estou ciente desse erro</nobr> <br><img src='$dir{img_syscall}/sair_salvar.png' border=0 style='float: right' onClick='t1.Hide(event); save_status("$COD","$DT");'>
HTML
	}

exit;


print "<table width=100% border=0 cellpadding=4 cellspacing=0 class='navigateable' style='margin-top: 4px;'>";
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
		print "<tr style='background-color: $cor;'><td style='width: 60px; font-size: 9px;'><nobr><b>".$row3->{'dt_hora'}."&nbsp;h</b></nobr></td><td style='font-size: 9px;'>".$row3->{'historico'}."</td></tr>";
		if($cor eq "#bfbfbf")
			{
			$cor = "#f2f2f2";
			}
		else
			{
			$cor = "#bfbfbf";
			}
		}
	}
elsif($rv3 == 0)
	{
	print "<tr><td align=center colspan=2><br><br><br><nobr><b>Não executado</b></nobr><br><br></td></tr>";
	}
print "</table>";
