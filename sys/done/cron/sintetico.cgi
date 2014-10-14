#!/usr/bin/perl

use Time::Local;

$nacess = "902";
require "../../cfg/init.pl";
require "./status.pl";
$COD = &get('cod');
$qtdias = 7;
$DT = &get('dt');
if($DT eq "")
	{
	$DT = 0;
	}
if($DT == 0)
	{
	$MANT = -$qtdias;
	$MPOS = 0;
	}
else
	{
	$MANT = $DT-$qtdias;
	$MPOS = $DT+$qtdias;
	}

$n=0;

$inidia = 0;
for($f=$qtdias;$f>=0;$f--)
	{
	($sec[$n], $min[$n], $hora[$n], $dia[$n], $mes[$n], $ano[$n], $diaSem[$n], $yday[$n], $isdst[$n]) = localtime(time()+(86400*$DT)-(86400*$f));
	$ano[$n] += 1900;
	$rmes[$n] = $mes[$n]+1;
	if($rmes[$n] < 10)
		{
		$rmes[$n] = "0".$rmes[$n];
		}
	$rdia[$n] = $dia[$n];
	if($rdia[$n] < 10)
		{
		$rdia[$n] = "0".$rdia[$n];
		}
	$n++;
	}

@Smes = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro", "Janeiro");
@wdiaSem = ('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb');

print $query->header({charset=>utf8});


$SQL = "select distinct empresa.codigo as cod_emp, empresa.nome as nome_emp, empresa_endereco.codigo as cod_end, empresa_endereco.endereco || empresa_endereco.complemento as endfull_emp from cron join empresa_endereco on cron.endereco = empresa_endereco.codigo join empresa on empresa.codigo = empresa_endereco.empresa where empresa.codigo = '$COD' ";
$SQL .= " and cron.hidden is false ";
$SQL .= " order by empresa.nome, endfull_emp ";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		print "		<table width=100% cellpadding=4 cellspacing=0 border=0 align='center' id='".$row->{'cod_end'}."'>\n			<tr><td width=25% rowspan=2 style='background-color: #3167b3; color: white; border-top: solid 1px white; font-size: 14px; font-weight: bold;'><nobr><a href='javascript:nload=0; top.Loading(); get_sintetico(\"".$row->{'cod_emp'}."\", \"".$MANT."\");' id='rew".$row->{'cod_end'}."' style='color: white'><</a> ";
		#if($DT < 0)
		#	{
		#	print $Smes[$mes[($qtdias)-1]];
		#	}
		#else
		#	{
		#	print $Smes[$mes[($qtdias)]];
		#	}
		print $qtdias." dias ";
		if($DT != 0)
			{
			print "<a href='javascript:nload=0; top.Loading(); get_sintetico(\"".$row->{'cod_emp'}."\", \"".$MPOS."\")' style='color: white'>></a></td>";
			}
		else
			{
			print "</nobr></td>";
			}
		for($f=$inidia;$f<=$qtdias;$f++)
			{
			print "<td style='background-color: #3167b3; color: white; border-top: solid 1px white; font-weight: bold; text-align: center; border-bottom: none 0px !important;";
			#if($rdia[$f] eq "01")
			#      {
			#      print " border-left: solid 1px #808080";
			#      }
			print "'>";
			print $wdiaSem[$diaSem[$f]]."</td>";
			}
		print "</tr>\n			<tr>";
		for($f=$inidia;$f<=$qtdias;$f++)
			{
			print "<td style='background-color: #3167b3; color: white; font-weight: bold; text-align: center;";
			#if($rdia[$f] eq "01")
			#      {
			#      print " border-left: solid 1px #808080";
			#      }
			print "'>".$rdia[$f]."/".$rmes[$f]."</td>";
			}
		print "</tr>";
		$SQL2 = "select codigo, cron.descrp as cron_name, to_char(dtcad, 'YYYYMMDD') as dt_ini, cron.tipo as cron_tipo from cron where cron.endereco = '$row->{'cod_end'}' ";
		$SQL2 .= " and cron.hidden is false ";
		$SQL2 .= " order by cron.descrp ";
		$sth2 = &select($SQL2);
		$rv2 = $sth2->rows();
		if($rv2 > 0)
			{
			$tcron = 0;
			while($row2 = $sth2->fetchrow_hashref)
				{
				print "			<tr><td>".$row2->{'cron_name'}."</td>";
				for($f=$inidia;$f<=$qtdias;$f++)
					{
					print "<td width=2% align='center'";
					if($rdia[$f] eq "01")
						{
						print " style='border-left: solid 1px #808080'";
						}
					print ">";
					if($row2->{'dt_ini'} < $ano[$f].$rmes[$f].$rdia[$f])
						{
						$tcron++; 
						if($row2->{'cron_tipo'} eq "3")
							{
							print &check_msn("$row2->{'codigo'}", $ano[$f]."-".$rmes[$f]."-".$rdia[$f]);
							}
						elsif($row2->{'cron_tipo'} eq "2")
							{
							print &check_mirror("$row2->{'codigo'}", $ano[$f]."-".$rmes[$f]."-".$rdia[$f]);
							}
						else
							{
							print &check("$row2->{'codigo'}", $ano[$f]."-".$rmes[$f]."-".$rdia[$f]);
							}
						}
					else
						{
						print "<img src='$dir{img_syscall}/none.png' border=0 width=25 alt='Sem Backup' title='Sem Backup'>";
						}
					print "</td>";
					}
				print "</tr>\n";
				}
			if($tcron == 0)
				{
				print "<script language='Javascript'>hide('rew".$row->{'cod_end'}."');</script>";
				}
			}
		print "		</table>\n";
		}
	}








