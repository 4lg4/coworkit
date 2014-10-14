#!/usr/bin/perl

$nacess = "903";
require "../cfg/init.pl";

use POSIX;

$endereco = &get('endereco');
$host = &get('host');
$div = &get('div');
$monitor = &get('monitor');
$descr = &get('descr');
$item = &get('item');
$intervalo = &get('intervalo');

print $query->header({charset=>utf8});
	
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<script language='JavaScript'>
	DLoad("monitoramento"); // carrega dependencias especificas
HTML

# Limpa a área do gráfico
print "\$('#".$div."').html('');\n";
if($monitor ne "" && $descr ne "")
	{
	my $sql = "select to_char(dt, 'YYYYMMDDHH24MI') as dth, to_char(dt, 'YYYY-MM-DD HH24:MI') as dthm, to_char(dt+interval '1 min', 'YYYY-MM-DD HH24:MI') as dthp, to_char(dt-interval '1 min', 'YYYY-MM-DD HH24:MI') as dtha, valor, valor_max from ";
	if($intervalo eq '1a' || $intervalo eq '3m' || $intervalo eq '2m')
		{
		$sql .= "monitor_historico";
		}
	else
		{
		$sql .= "monitor_historico_last";
		}
	$sql .= " where monitor='$monitor' and descrp='$descr' and item='$item' ";
	if($intervalo eq '1a')
		{
		$sqlb .= " and dt > now() - interval '1 year' ";
		$sqlc = " now() - interval '1 year' ";
		}
	elsif($intervalo eq '3m')
		{
		$sqlb .= " and dt > now() - interval '90 days' ";
		$sqlc = " now() - interval '90 days' ";
		}
	elsif($intervalo eq '2m')
		{
		$sqlb .= " and dt > now() - interval '60 days' ";
		$sqlc = " now() - interval '60 days' ";
		}		
	elsif($intervalo eq '1m')
		{
		$sqlb .= " and dt > now() - interval '30 days' ";
		$sqlc = " now() - interval '30 days' ";
		}
	elsif($intervalo eq '7d')
		{
		$sqlb .= " and dt > now() - interval '7 days' ";
		$sqlc = " now() - interval '7 days' ";
		}		
	elsif($intervalo eq '1d')
		{
		$sqlb .= " and dt > now() - interval '1 day' ";
		$sqlc = " now() - interval '1 day' ";
		}
	elsif($intervalo eq '6h')
		{
		$sqlb .= " and dt > now() - interval '6 hours' ";
		$sqlc = " now() - interval '6 hours' ";
		}
	else
		{
		$sqlb .= " and dt > now() - interval '1 hour' ";
		$sqlc = " now() - interval '1 hour' ";
		}
		
	
	$sql .= $sqlb." order by dthm desc, valor, valor_max";
	$DB2 = &DBE($sql);
	$vlr_max = 0;
	$dth_ant = "";
	$vlr = "[";
	while($v=$DB2->fetchrow_hashref)
		{
		if($v->{valor_max} > $vlr_max)
			{
			$vlr_max = $v->{valor_max};
			}
		if($dth_ant ne "" && $v->{dth} < $dth_ant-60)
			{
			$vlr .= "['".$v->{dthp}."', 0], ";
			$vlr .= "['".$dthm_ant."', 0], ";
			}
		if($dth_ant ne $v->{dth})
			{
			$vlr .= "['".$v->{dthm}."', ".$v->{valor}."], ";
			if($vlr_max < $v->{valor})
				{
				$vlr_max = $v->{valor}+10;
				}
			$dth_ant = $v->{dth};
			$dthm_ant = $v->{dtha};
			}
		}
		
	if($dth_ant ne "")
		{
		my $sql3 = "select to_char(($sqlc), 'YYYYMMDDHH24MI') as dth, to_char(($sqlc), 'YYYY-MM-DD HH24:MI') as dthm, to_char(($sqlc + interval '1 min'), 'YYYY-MM-DD HH24:MI') as dthp ";
		$DB3 = &DBE($sql3);	
		while($v3=$DB3->fetchrow_hashref)
			{
			if($v3->{dth} < $dth_ant-10)
				{
				$vlr .= "['".$v3->{dthp}."', 0], ";
				$vlr .= "['".$dthm_ant."', 0], ";
				}
			if($dth_ant ne $v->{dth})
				{		
				$vlr .= "['".$v3->{dthm}."', 0], ";
				}
			}
		}
		
	$vlr .= "]";

	if($vlr ne "[]")
		{
		print "	var ".$div." = \$.jqplot('".$div."', [$vlr], ";
		}
	}
if($vlr ne "[]")
	{
	&drawline;

	print<<HTML;
// Corrige BUG do gráfico 
var minY = $div.axes.xaxis._dataBounds.min;
var maxY = $div.axes.xaxis._dataBounds.max;
$div.axes.xaxis.min = minY;
$div.axes.xaxis.max = maxY;
$div.replot();

\$(".jqplot-axis, .jqplot-title").css("color","#fff");
</script>
</head>
<body>
</body>
</html>
HTML
	}
exit;

	
sub drawline
	{
print<<HTML;
	{
	grid:{borderColor:'transparent',drawBorder:false,shadowColor:'transparent',background:'transparent'},
	gridPadding: {top:10, bottom:40, left:60, right:20},	
	axes:	{
		xaxis:	{
			pad: 0,
			renderer:\$.jqplot.DateAxisRenderer,
			tickOptions:
				{
				formatString:'<center>\%H:\%Mh<br>%#d/%#m</center>'
				}
			},
		yaxis: 	{
			pad: 0,
			min: 0,
			max:$vlr_max
			}
		},
	seriesColors:[ '#FF9700', '#00CC00'],
HTML
	if($item eq "5" || $item eq "6")
		{
		print "series:[{lineWidth:2, showMarker:false, fill: true}]";
		}
	else
		{
		print "series:[{lineWidth:2, showMarker:false}]";
		}
print<<HTML;
	});
HTML
	}

