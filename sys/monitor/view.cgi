#!/usr/bin/perl

$nacess = "903";
require "../cfg/init.pl";

use POSIX;

$endereco = &get('endereco');
$host = &get('host');

print $query->header({charset=>utf8});

$n = 0;
# Encontra o que está sendo monitorado no endereço ou host
$sql = "select distinct monitor_grupo.descrp as monitor_titulo, monitor_grupo.codigo, monitor_historico_last.item, monitor_historico_last.descrp as historico_descrp, monitor_item.descrp as monitor_subtitulo, monitor_item.tipo_monitor_grafico from monitor_grupo join monitor_historico_last on monitor_grupo.codigo = monitor_historico_last.monitor join monitor_item on monitor_item.codigo = monitor_historico_last.item where monitor_grupo.endereco = '$endereco' ";
if($host ne "")
	{
	$sql .= "and monitor_grupo.host = '$host' ";
	}
else
	{
	$sql .= "and monitor_grupo.host is null ";
	}
$sql .= "and hidden is not true order by monitor_grupo.descrp, monitor_item.descrp, monitor_historico_last.descrp ";

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
	print "\$('#monitor_".$f."').DTouchBoxes({title:'".$mon_descrfull[$f]."'});";
	print "\$('#graph_".$f."').height(300);";

	# caso seja gráfico de pizza
	if($mon_tipo[$f] eq "2")
		{
		print "\$('#rodape_".$f."').html(\"<a href='javascript:monitor.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"0h\\\")'>0 horas</a> | <a href='javascript:monitor.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"7d\\\")'>7 dias</a> | <a href='javascript:monitor.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1m\\\")'>1 mês</a> | <a href='javascript:monitor.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"3m\\\")'>3 meses</a> | <a href='javascript:monitor.detail_hd(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1a\\\")'>1 ano</a>\");\n";
		}
	else
		{
		print "\$('#rodape_".$f."').html(\"<a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1h\\\")'>1 hora</a> | <a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"6h\\\")'>6 horas</a> | <a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1d\\\")'>1 dia</a> | <a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"7d\\\")'>7 dias</a> | <a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"1m\\\")'>1 mês</a> | <a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"2m\\\")'>2 meses</a> | <a href='javascript:monitor.detail_cpu(\\\"".$f."\\\",\\\"".$mon_cod[$f]."\\\", \\\"".$mon_descr[$f]."\\\",\\\"".$mon_item[$f]."\\\", \\\"3m\\\")'>3 meses</a>\");\n";
		}
	}

print<<HTML;
\$(document).ready(function()
	{
HTML
for($f=0; $f<$n; $f++)
	{
	if($mon_tipo[$f] eq "2")
		{
		print "monitor.detail_hd(\"".$f."\",\"".$mon_cod[$f]."\", \"".$mon_descr[$f]."\",\"".$mon_item[$f]."\", \"0h\");";
		}
	else
		{
		print "monitor.detail_cpu(\"".$f."\",\"".$mon_cod[$f]."\", \"".$mon_descr[$f]."\",\"".$mon_item[$f]."\", \"6h\");";
		}
	}
print<<HTML;
	});
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

	
	
	
	
	
	
	
