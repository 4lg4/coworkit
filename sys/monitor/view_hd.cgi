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
	my $sql = "select to_char(dt, 'YYYY-MM-DD HH24:MI') as dthm, valor, valor_max, valor_max-valor as livre from ";
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
		$sql .= " and dt > now() - interval '1 year' ";
		}
	elsif($intervalo eq '3m')
		{
		$sql .= " and dt > now() - interval '90 days' ";
		}
	elsif($intervalo eq '1m')
		{
		$sql .= " and dt > now() - interval '30 days' ";
		}
	elsif($intervalo eq '7d')
		{
		$sql .= " and dt > now() - interval '7 days' ";
		}
	elsif($intervalo eq '1d')
		{
		$sql .= " and dt > now() - interval '1 day' ";
		}
	elsif($intervalo eq '6h')
		{
		$sql .= " and dt > now() - interval '6 hours' ";
		}
	elsif($intervalo eq '1h')
		{
		$sql .= " and dt > now() - interval '1 hour' ";
		}

	$sql .= " order by dthm desc, valor, valor_max ";
	
	if($intervalo eq "0h")
		{
		$sql .= " limit 1";
		}
	

	$DB2 = &DBE($sql);	

	$vlr = "[";
	$vlr_max = 0;
	$dth_ant = "";
	while($v=$DB2->fetchrow_hashref)
		{
		if($DB2->rows() == 1)
			{
			my $usado = convert($v->{valor});
			my $livre = convert($v->{livre});

			$vlr .= "['".$usado." ".$descr."', ".$v->{valor}."], ";
			$vlr .= "['".$livre." livres', ".$v->{livre}."], ";
			}
		else
			{
			if($v->{valor_max} > $vlr_max)
				{
				$vlr_max = $v->{valor_max};
				}
			$vlr .= "['".$v->{dthm}."', ".$v->{valor}."], ";
			}
		}
	$vlr .= "]";

	if($vlr ne "[]")
		{
		print "	var ".$div." = \$.jqplot('".$div."', [$vlr], ";
		if($intervalo eq "0h")
			{
			&drawpie;
			}
		else
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
HTML
			}
		}
	}
	
print<<HTML;
</script>
</head>
<body>
</body>
</html>
HTML

exit;

	
sub drawline
	{
print<<HTML;
	{
	grid:{borderColor:'transparent',drawBorder:false,shadowColor:'transparent',background:'transparent'},
	gridPadding: {top:10, bottom:30, left:60, right:20},	
	axes:	{
		xaxis:	{
			pad: 0,
			renderer:\$.jqplot.DateAxisRenderer,
			tickOptions:
				{
				formatString:'<center>%#d/%#m</center>'
				}
			},
		yaxis: 	{
			pad: 0,
			tickOptions:
				{
				formatter: tickFormatter
				},
			min: 0,
			max:$vlr_max
			}
		},
	seriesColors:[ '#FF9700', '#00CC00', '#FF0000'],	
	series:[{fill: true}]
	});
 
\$(".jqplot-axis, .jqplot-title").css("color","#fff");
HTML
	}

sub drawpie
	{
print<<HTML;
	{
	grid:{borderColor:'transparent',shadow:false,drawBorder:false,shadowColor:'transparent',background:'transparent'},
	gridPadding: {top:0, bottom:0, left:30, right:10},
	seriesDefaults:{
	    renderer:\$.jqplot.PieRenderer, 
	    trendline:{ show:false }, 
	    rendererOptions: { padding: 8, showDataLabels: true, sliceMargin: 2, startAngle: -90 }
	},
	seriesColors:[ '#FF9700', '#00CC00', '#FF0000'],
	legend:{
	    show:true, 
	    location:'se',
	    xoffset: 0,
	    yoffset: 0	    
	}       
});
HTML
	}
	
sub convert
	{
	my ($v) = @_;
	
	if($v > 1048575)
		{
		$v = $v / 1048576;
		$v = sprintf "%.2f", $v;
		$v .= " GB ";
		}
	elsif($v > 1023)
		{
		$v = $v / 1024;
		$v = sprintf "%.2f", $v;
		$v .= " MB ";
		}
	else
		{
		$v .= "kB ";
		}
		
	return $v;
	}

