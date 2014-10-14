#!/usr/bin/perl

$nacess = "903";
require "../cfg/init.pl";

use POSIX;

$endereco = &get('endereco');
$host = &get('host');

print $query->header({charset=>utf8});

$n = 0;
# Encontra o que está sendo monitorado no endereço ou host
$sql = "select distinct monitor_grupo.descrp as monitor_titulo, monitor_grupo.codigo, monitor_historico.item, monitor_historico.descrp as historico_descrp, monitor_item.descrp as monitor_subtitulo, monitor_item.tipo_monitor_grafico from monitor_grupo join monitor_historico on monitor_grupo.codigo = monitor_historico.monitor join monitor_item on monitor_item.codigo = monitor_historico.item where monitor_grupo.endereco = '$endereco' ";
if($host ne "")
	{
	$sql .= "and monitor_grupo.host = '$host' ";
	}
else
	{
	$sql .= "and monitor_grupo.host is null ";
	}
$sql .= "and hidden is not true order by monitor_grupo.descrp, monitor_item.descrp, monitor_historico.descrp ";

if($endereco ne "")
	{
	$DB = &DBE($sql);
	while($m=$DB->fetchrow_hashref)
		{
		$mon_cod[$n] = $m->{codigo};
		$mon_titulo[$n] = $m->{monitor_titulo};
		$mon_subtitulo[$n] = $m->{monitor_subtitulo};
		$mon_descr[$n] = $m->{historico_descrp};
		$mon_descrfull[$n] = $m->{monitor_titulo}.": ".$m->{monitor_subtitulo}." ".$m->{historico_descrp};
		$mon_item[$n] = $m->{item};
		$mon_tipo[$n] = $m->{tipo_monitor_grafico};

		$n++;
		if($m->{item} eq "51" && $m->{historico_descrp} ne "0")
			{
			$n--;
			}
		}
	}
	
	
print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

<script language='JavaScript'>
	DLoad("monitoramento"); // carrega dependencias especificas
HTML
for($f=0; $f<$n; $f++)
	{
	# caso seja gráfico de pizza
	if($mon_tipo[$f] eq "2")
		{
		# encontra as partições que estão sendo monitoradas
		$DB2 = &DBE("select max(dt) as dtmax, valor, valor_max-valor as livre from monitor_historico where monitor='$mon_cod[$f]' and descrp='$mon_descr[$f]' and item='$mon_item[$f]' group by valor, valor_max order by dtmax desc limit 1");
		$vlr = "";
		while($v=$DB2->fetchrow_hashref)
			{
			my $usado = convert($v->{valor});
			my $livre = convert($v->{livre});

			$vlr .= "[['".$usado." ".$mon_descr[$f]."', ".$v->{valor}."], ";
			$vlr .= "['".$livre." livres', ".$v->{livre}."]], ";
			}
		print "\$('#monitor_".$f."').DTouchBoxes({title:'".$mon_descrfull[$f]."'});";
		print "	var graph_mon".$f." = \$.jqplot('graph_".$f."', [$vlr], ";
		&drawpie;
		print "\$('#rodape_".$f."').html(\"<a href='javascript:procede.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"0h\\\")'>0 horas</a> | <a href='javascript:procede.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"7d\\\")'>7 dias</a> | <a href='javascript:procede.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1m\\\")'>1 mês</a> | <a href='javascript:procede.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"3m\\\")'>3 meses</a> | <a href='javascript:procede.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1a\\\")'>1 ano</a>\");\n";
		}
	else
		{
		# encontra os últimos valores
		if($mon_item[$f] eq "51")
			{
			$DB2 = &DBE("select to_char(dt, 'YYYY-MM-DD HH24:MI') as dth, to_char(dt, 'YYYY-MM-DD HH24:MI') as dthm, valor, valor_max, descrp from monitor_historico where monitor='$mon_cod[$f]' and item='$mon_item[$f]' and dt > now() - interval '1 day' order by dthm, valor, valor_max desc");
			
			%vlr = ();
			$vlr_max = 0;
			$dth_ant = "";
			while($v=$DB2->fetchrow_hashref)
				{
				if($v->{valor_max} > $vlr_max)
					{
					$vlr_max = $v->{valor_max};
					}
				$vlr{$v->{descrp}} .= "['".$v->{dthm}."', ".$v->{valor}."],";
				if($vlr_max < $v->{valor})
					{
					$vlr_max = $v->{valor}+10;
					}
				}

			$vlrt = "";
			while(my ($key, $value) = each(%vlr) )
				{
				$value =~ s/,$//;
				$vlrt .= "[".$value."],";
				}

			print "\$('#monitor_".$f."').DTouchBoxes({title:'".$mon_descrfull[$f]."'});";
			print "	var graph_mon".$f." = \$.jqplot('graph_".$f."', [".$vlrt."], ";
			$div = "graph_mon".$f;
			}
		else
			{
			if($mon_item[$f] < 4)
				{
				$DB2 = &DBE("select to_char(dt, 'YYYY-MM-DD HH24') as dth, to_char(dt, 'YYYY-MM-DD HH24:MI') as dthm, valor, valor_max from monitor_historico where monitor='$mon_cod[$f]' and descrp='$mon_descr[$f]' and item='$mon_item[$f]' order by dthm desc, valor, valor_max limit 1000");
				}
			else
				{
				$DB2 = &DBE("select to_char(dt, 'YYYYMMDDHH24MI') as dth, to_char(dt, 'YYYY-MM-DD HH24:MI') as dthm, to_char(dt+interval '1 min', 'YYYY-MM-DD HH24:MI') as dthp, to_char(dt-interval '1 min', 'YYYY-MM-DD HH24:MI') as dtha, valor, valor_max from monitor_historico where monitor='$mon_cod[$f]' and descrp='$mon_descr[$f]' and item='$mon_item[$f]' and dt > now() - interval '6 hours' order by dthm desc, valor, valor_max limit 1000");
				}
			$vlr = "[";
			if($mon_item[$f] eq "7")
				{
				$vlr_max = 1000;
				}
			else
				{
				$vlr_max = 0;
				}
			$dth_ant = "";
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
			$vlr .= "]";

			print "\$('#monitor_".$f."').DTouchBoxes({title:'".$mon_descrfull[$f]."'});";
			
			if($vlr ne "[]")
				{
				print "	var graph_mon".$f." = \$.jqplot('graph_".$f."', [$vlr], ";
				}
			else
				{
				print "\$('#graph_".$f."').height(300);";
				}
			$div = "graph_mon".$f;
			}
		if($vlr ne "[]")
			{
			&drawline;
			}
		print "\$('#rodape_".$f."').html(\"<a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1h\\\")'>1 hora</a> | <a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"6h\\\")'>6 horas</a> | <a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1d\\\")'>1 dia</a> | <a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"7d\\\")'>7 dias</a> | <a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1m\\\")'>1 mês</a> | <a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"2m\\\")'>2 meses</a> | <a href='javascript:procede.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"3m\\\")'>3 meses</a>\");\n";
print<<HTML;
// Corrige BUG do gráfico 
var minY = $div.axes.xaxis._dataBounds.min;
var maxY = $div.axes.xaxis._dataBounds.max;
$div.axes.xaxis.min = minY;
$div.axes.xaxis.max = maxY;
$div.replot();

\$(".jqplot-axis, .jqplot-title").css("color","#fff");
HTML
		}
	}
print<<HTML;
</script>
</head>
<body>
<div id='monitoramento'>

<!-- Elementos monitorados -->
HTML

for($f=0; $f<$n; $f++)
	{
	print "
<div id='monitor_container_".$f."' class='widget' style='width: 32%; float: left; margin-right: 1%; margin-bottom: 1%;'>
	<div id='monitor_".$f."'>
		<div id='graph_".$f."'></div>
		<div id='rodape_".$f."' class='rodape'>&nbsp;</div>
	</div>
</div>";
	}

print<<HTML;
</div>
</body>
</html>
HTML

exit;


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

sub drawpie
	{
print<<HTML;
	{
	grid:{borderColor:'transparent',shadow:false,drawBorder:false,shadowColor:'transparent',background:'transparent'},
	gridPadding: {top:0, bottom:0, left:20, right:10},
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

sub drawdonut
	{
print<<HTML;
	{
	grid:{borderColor:'transparent',shadow:false,drawBorder:false,shadowColor:'transparent',background:'transparent'},
	gridPadding: {top:0, bottom:0, left:30, right:10},
	seriesDefaults:{
	    renderer:\$.jqplot.DonutRenderer, 
	    trendline:{ show:false }, 
	    rendererOptions: { padding: 8, showDataLabels: true, sliceMargin: 2, startAngle: -90 }
	},
	legend:{
	    show:true, 
	    location:'se'
	}       
});
HTML
	}

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
	if($mon_item[$f] eq "5" || $mon_item[$f] eq "6")
		{
		print "series:[{lineWidth:2, showMarker:false, fill: true}]";
		}
	else
		{
		print "series:[{lineWidth:2, showMarker:false}]";
		}
print<<HTML;
	});
 
\$(".jqplot-axis, .jqplot-title").css("color","#fff");
HTML
	}