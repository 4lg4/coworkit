#!/usr/bin/perl

use Time::Local;

$nacess = "902";
require "../../cfg/init.pl";
require "./status.pl";
$TCRON = &get('cron');
$DETAIL = &get('detalhe');
$PERIODO = &get('periodo');
$STATUS = &get('status');
$CLIENTE = &get('cliente');
if($PERIODO eq "range")
	{
	$DT_INI = &get('dt_ini');
	$DT_FIM = &get('dt_fim');
	}
if($DETAIL eq "detalhado")
	{
	$DT1 = "style='display: none'";
	$DT2 = "";
	$DT3 = "style='display: none'";
	}
elsif($DETAIL eq "super")
	{
	$DT1 = "style='display: none'";
	$DT2 = "";
	$DT3 = "";
	}
else
	{
	$DT1 = "";
	$DT2 = "style='display: none'";
	$DT3 = "style='display: none'";
	}

($sec[$n], $min[$n], $hora[$n], $dia[$n], $mes[$n], $ano[$n], $diaSem[$n], $yday[$n], $isdst[$n]) = localtime(time());
@Smes = ("Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro", "Janeiro");
@wdiaSem = ('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb');

print $query->header({charset=>utf8});


$SQL = "select distinct empresa.codigo as cod_emp, empresa.nome as nome_emp, empresa_endereco.codigo as cod_end, empresa_endereco.endereco as end_descr, empresa_endereco.*, fones_lista.numero as telefone from cron join empresa_endereco on cron.endereco = empresa_endereco.codigo join empresa on empresa.codigo = empresa_endereco.empresa left join fones_lista on empresa_endereco.codigo = fones_lista.endereco ";
$SQL .= " where cron.hidden is false ";
if($CLIENTE ne '')
  {  
      $SQL .=" and empresa.codigo='$CLIENTE'";
  }

  
$SQL .= " order by empresa.nome, empresa_endereco.endereco ";
$sth = &select($SQL);
$rv = $sth->rows();
if($rv > 0)
	{
	while($row = $sth->fetchrow_hashref)
		{
		$endfull = $row->{'end_descr'};
		if($endfull ne "")
			{
			$endfull = "- ".$endfull;
			}
		if($endfull ne "" && $row->{'complemento'} ne "")
			{
			$endfull .= " / ";
			}
		$endfull .= $row->{'complemento'};
		if($endfull ne "" && $row->{'cidade'} ne "")
			{
			$endfull .= " - ";
			}
		$endfull .= $row->{'cidade'};
		if($endfull ne "" && $row->{'uf'} ne "")
			{
			$endfull .= "/";
			}
		$endfull .= $row->{'uf'};
		if($row->{'telefone'} ne "")
			{
			if($endfull ne "")
				{
				$endfull .= " - ";
				}
			$endfull .=  "Telefone: ".$row->{'telefone'};
			}
		
print<<HTML;
	<div id='emp_$row->{'cod_emp'}_$row->{'cod_end'}' class='DTouchBoxes' style='width: 100%; margin-top: 1px; margin-left: 0px; padding: 10px;'>$row->{'nome_emp'} $endfull <div style='float: right'><a href='#' title='Listagem Resumida' onClick="detalhe='resumido'; shw_detalhes('resumido', 'cron_$row->{'cod_emp'}_$row->{'cod_end'}');"><img src='$dir{img_syscall}/cron_resumido.png' border=0></a> <a href='#' title='Listagem Detalhada' onClick="detalhe='detalhado'; shw_detalhes('detalhado', 'cron_$row->{'cod_emp'}_$row->{'cod_end'}');"><img src='$dir{img_syscall}/cron_detalhado.png' border=0></a> <a href='#' title='Listagem Bem Detalhada' onClick="detalhe='super'; shw_detalhes('super', 'cron_$row->{'cod_emp'}_$row->{'cod_end'}');"><img src='$dir{img_syscall}/cron_super.png' border=0></a></div></div>
	<div id='cron_$row->{'cod_emp'}_$row->{'cod_end'}' class='DTouchBoxes' style='width: 100%; padding: 10px;'>
HTML
		if($PERIODO eq "range")
			{
			$SQL2 = "select codigo, cron.descrp as cron_name, ";
			if($DT_INI ne "")
				{
				$SQL2 .= "to_char(date('$DT_INI'), 'YYYY-MM-DD') as dt_ini, ";
				}
			else
				{
				$SQL2 .= "to_char(dtcad, 'YYYY-MM-DD') as dt_ini, ";
				}
			if($DT_FIM ne "")
				{
				if($DT_INI ne "")
					{
					$SQL2 .= "date('$DT_FIM') - date('$DT_INI') as dt_diff ";
					}
				else
					{
					$SQL2 .= "extract(day from '$DT_FIM' - dtcad) as dt_diff ";
					}
				}
			else
				{
				if($DT_INI ne "")
					{
					$SQL2 .= "extract(day from now() - '$DT_INI') as dt_diff ";
					}
				else
					{
					$SQL2 .= "extract(day from now() - dtcad) as dt_diff ";
					}
				}
			$SQL2 .= "from cron where cron.endereco = '$row->{'cod_end'}' ";
			}
		elsif($PERIODO ne "")
			{
			$SQL2 = "select codigo, cron.descrp as cron_name, to_char(now() - interval '".$PERIODO." days', 'YYYY-MM-DD') as dt_ini from cron where cron.endereco = '$row->{'cod_end'}' ";
			}
		else
			{
			$SQL2 = "select codigo, cron.descrp as cron_name, to_char(dtcad, 'YYYY-MM-DD') as dt_ini, extract(day from now() - dtcad) as dt_diff from cron where cron.endereco = '$row->{'cod_end'}' ";
			}
		if($TCRON ne "")
			{
			$SQL2 .= " and cron.tipo = '$TCRON' ";
			}
		$SQL2 .= " and cron.hidden is false ";
		$SQL2 .= " order by cron.descrp ";
		$sth2 = &select($SQL2);
		$rv2 = $sth2->rows();
		if($rv2 > 0)
			{
			$nemp = 0;
			while($row2 = $sth2->fetchrow_hashref)
				{
				if($PERIODO eq "range")
					{
					$diff = $row2->{'dt_diff'}+1;
					}
				elsif($PERIODO ne "")
					{
					$diff = $PERIODO+1;
					}
				else
					{
					$diff = $row2->{'dt_diff'}+1;
					}
				$sth4 = &select("select series.date, *, to_char(cron_historico.dt, 'DD/MM/YYYY às HH24:MI:SS') as dt_hora, to_char(cron_historico.dt, 'HH24:MI:SS') as hora, to_char(series.date, 'YYYY-MM-DD') as dt_us, to_char(series.date, 'DD/MM/YYYY') as dt_iso, cron_historico.descrp as historico from (select generate_series(0,$diff) + (date('".$row2->{'dt_ini'}."')) as date) as series left join cron_historico on date(series.date) = date(cron_historico.dt) and cron_historico.cron = '$row2->{'codigo'}' order by series.date, cron_historico.dt ");
				$rv4 = $sth4->rows();
				$dt = "";
				$n=-1;
				@cron = ();
				if($rv4 > 0)
					{
					while($row4 = $sth4->fetchrow_hashref)
						{
						if($dt ne $row4->{'dt_us'})
							{
							$dt = $row4->{'dt_us'};
							$n++;
							$ROWSTATUS="";
							$GETSTATUS = &check($row2->{'codigo'}, $row4->{'dt_us'}, 'status');
							if($STATUS eq "" || $STATUS eq "all")
								{
								$ROWSTATUS = $GETSTATUS;
								}
							elsif($STATUS eq "ok" && $GETSTATUS =~ /^realizado com sucesso/i)
								{
								$ROWSTATUS = $GETSTATUS;
								}
							elsif($STATUS eq "error")
								{
								if($GETSTATUS =~ /^erro/i)
									{
									$ROWSTATUS = $GETSTATUS;
									}
								elsif($GETSTATUS =~ /^imposs/i)
									{
									$ROWSTATUS = $GETSTATUS;
									}
								}
							elsif($STATUS eq "noexec" && $GETSTATUS =~ /^n.*o executado/i)
								{
								$ROWSTATUS = $GETSTATUS;
								}
							else
								{
								$ROWSTATUS = "";
								$n--;
								}
							}
						if($ROWSTATUS ne "")
							{
							$cron[$n][0] = $row2->{'codigo'};
							$cron[$n][1] = $row2->{'cron_name'};
							if(lc($row4->{'historico'}) eq "iniciado")
								{
								$cron[$n][2] = $row4->{'dt_hora'};
								}
							if(lc($row4->{'historico'}) eq "finalizado")
								{
								$cron[$n][3] = $row4->{'dt_hora'};
								}
							if($cron[$n][4] eq "")
								{
								$cron[$n][4] = &check($row2->{'codigo'}, $row4->{'dt_us'}, 'icon');
								}
							if($cron[$n][6] eq "")
								{
								$cron[$n][6] = $ROWSTATUS;
								}
							if($cron[$n][7] eq "")
								{
								$cron[$n][7] = $row4->{'dt_iso'};
								}
							$cron[$n][5] .= $row4->{'dt_hora'}." ".$row4->{'historico'}."<br>";
							}
						}
					}
				$sth4->finish;

				print "		<table width=100% cellpadding=4 cellspacing=0 border=0 id='analitico_tab' style='margin-bottom: 2px; border: dotted 1px white;'>\n";
				$nome = "";
				for($f=0; $f<$n; $f++)
					{
					if($cron[$f][0] ne "")
						{
						print "			<tr valign=top>";
						if($nome ne $cron[$f][1])
							{
							if($nome ne "")
								{
								print "</tbody>\n";
								}
							print "<td colspan=5 style='background-color: #3167b3; color: white; padding: 5px; border-bottom: none 0px;' onClick=\"\$('#ln_".$cron[$f][0]."').toggle(); \$('#less_".$cron[$f][0]."').toggle(); \$('#more_".$cron[$f][0]."').toggle();\"><span id='less_".$cron[$f][0]."' $DT2>[-]</span><span id='more_".$cron[$f][0]."' $DT1>[+]</span> ".$cron[$f][1]."</td></tr>\n<tbody id='ln_".$cron[$f][0]."' $DT2>";
							print "	<tr><th width=10% style='background-color: #656565; color: white; border-top: solid 1px white;'>Iniciado</th><th width=10% style='background-color: #656565; color: white; border-top: solid 1px white;'>Concluído</th><th width=5% style='background-color: #656565; color: white; border-top: solid 1px white;'>Status</th><th style='background-color: #656565; color: white; border-top: solid 1px white;'>Descrição</th><th width=30% style='background-color: #656565; color: white; border-top: solid 1px white;'>Detalhes</th></tr>\n<tr valign=top>";
							$nome = $cron[$f][1];
							}
						if($cron[$f][2] ne "")
							{
							print "<td style='text-align: left; padding-top: 10px;'><nobr>".$cron[$f][2]."h</nobr></td>";
							}
						elsif($cron[$f][7] ne "")
							{
							print "<td style='text-align: left; padding-top: 10px'><nobr>".$cron[$f][7]."</nobr></td>";
							}
						else
							{
							print "<td></td>";
							}
						if($cron[$f][3] ne "")
							{
							print "<td style='text-align: left; padding-top: 10px'><nobr>".$cron[$f][3]."h</nobr></td>";
							}
						else
							{
							print "<td></td>";
							}
						if($cron[$f][4] ne "")
							{
							print "<td align=center style='margin-top: 0px'>".$cron[$f][4]."</td>";
							}
						else
							{
							print "<td></td>";
							}
						print "<td style='padding-top: 10px'>".$cron[$f][6]."</td>";
						if($cron[$f][5] =~ /[0-9]/)
							{
							print "<td><div id='more_".$cron[$f][0]."_".$f."'><a href='#' onClick='javascript:\$(\"#more_".$cron[$f][0]."_".$f."\").hide(); \$(\"#dt_".$cron[$f][0]."_".$f."\").show();'>[+] mais detalhes</a></div><div id='dt_".$cron[$f][0]."_".$f."'><div id='less_".$cron[$f][0]."_".$f."'><a href='#' onClick='\$(\"#dt_".$cron[$f][0]."_".$f."\").hide(); \$(\"#more_".$cron[$f][0]."_".$f."\").show();' style='float: left'>[-]</a><div style='margin-left: 20px; float: left;'>".$cron[$f][5]."</div></div></td>";
							}
						else
							{
							print "<td></td>";
							}
						print "</tr>";
						}
					}
				if($nome ne "")
					{
					$nemp++;
					}
				print "</tbody>";
				print "		</table>\n";
				}
			if($nemp < 1)
				{
				print "<script language='Javascript'>\$(\"#emp_".$row->{'cod_emp'}."_".$row->{'cod_end'}."\").hide()</script>";
				}
			}
		else
			{
			print "<script language='Javascript'>\$(\"#emp_".$row->{'cod_emp'}."_".$row->{'cod_end'}."\").hide()</script>";
			}
		print "</div>";
		$sth2->finish;
		}
	}






