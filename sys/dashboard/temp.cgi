#!/usr/bin/perl

#
# chamado.cgi
#
# Lista de chamados que aparecem no modulo
#
# vars
#	$tu  = Tempo Usuario
#	$tg  = Tempo Global (tempo de todos usuarios)
#	$tub = Tempo Usuario Best (tempo de todos usuarios mostrando um a um em ordem decrescente)
#	$H = Tempo dos clientes

$nacess = "2";
require "../cfg/init.pl";

$ID = &get('ID');

print $query->header({charset=>utf8});

# gera grafico com as ultimas medicoes
# $DB = DBE("select to_char(mh.dt, 'YYYY-MM-DD') as dts, to_char(mh.dt, 'MI') as dtsm, to_char(mh.dt, 'HH24')::int as hc, tm.descrp, mh.valor, mh.valor_max, tm.unidade_simbolo from monitor_historico as mh left join monitor as m on m.codigo = mh.monitor left join tipo_monitor_valor as tm on tm.codigo = mh.tipo_valor where mh.monitor = 1 and mh.tipo_valor = 1 and to_char(mh.dt, 'YYYY-MM-DD HH24') = to_char((now() - interval '2 hour'), 'YYYY-MM-DD HH24') order by mh.codigo desc limit 3");
$DB = DBE("select DISTINCT to_char(mh.dt, 'YYYY-MM-DD HH24') as dth, max(mh.valor) as valor from monitor_historico as mh where mh.monitor = 1 and mh.tipo_valor = 1 and to_char(mh.dt, 'YYYY-MM-DD HH24') > to_char((now() - interval '10 hour'), 'YYYY-MM-DD HH24') group by dth order by dth asc");
while($h = $DB->fetchrow_hashref)
	{
	#  $porcentagem = &percentage(($tub->{tempo_total_sum} * 100) / $tg->{tempo_total_sum});

	# monta hora 
	# $h->{dts} .= " ".$h->{hc}.":".$h->{dtm};
	
	# gera array para grafico de porcentagem
	# if($h->{hc} > 12)
	# 	{ $h->{dts} .= "PM"; }
	#else
	#	{ $h->{dts} .= "AM"; }
	$porcentagem_graph .= "['$h->{dth}:00',$h->{valor}],";
	
	# $RU .= "<div><span>".(&slimit($tub->{tecnico_nome},13,'.')).":</span><span>[$tub->{total_chamados}]</span><span> ".(&dateToShow($tub->{tempo_total},"TIME"))."h </span><span>$porcentagem%</span></div>";
	}
$porcentagem_graph = substr($porcentagem_graph, 0,-1); # remove ultima virgula

$R = "<u>".&dateToShow(timestamp("timestamp"))."</u><br>";

$DB2 = DBE("select tm.descrp, mh.valor, tm.unidade_simbolo from monitor_historico as mh left join monitor as m on m.codigo = mh.monitor left join tipo_monitor_valor as tm on tm.codigo = mh.tipo_valor where mh.monitor = 1 order by mh.codigo desc limit 3");
while($t = $DB2->fetchrow_hashref)
	{
	$R .= "&nbsp;&nbsp;&nbsp;&nbsp; <b>".$t->{descrp}."</b> ".$t->{valor}." ".$t->{unidade_simbolo}."<br>";
	}
# $R = $R." - ".$t->{descrp}." - ".$t->{valor}." - ".$t->{unidade_simbolo};

# retorno do codigo 
print<<HTML;
<script>
	\$("#dashboard_temp").html("<br><br> &nbsp;&nbsp; $R <br><br>");
	
	\$("#dashboard_temp_graph").html("");
	// var aa = [['2013-08-13 05:00',25.00],['2013-08-13 06:00',25.00],['2013-08-13 07:00',24.00],['2013-08-13 08:00',25.00],['2013-08-13 09:00',24.00],['2013-08-13 10:00',25.00],['2013-08-13 11:00',25.00],['2013-08-13 12:00',25.00],['2013-08-13 13:00',25.00],['2013-08-13 14:00',25.00]];
  var plot1 = \$.jqplot('dashboard_temp_graph', [[$porcentagem_graph]], {
    title:'Histórico',
    axes:{
        xaxis:{
            renderer:\$.jqplot.DateAxisRenderer,
			tickOptions:
				{
				formatString:'%#d/%#m %#Hh'
				}
        }
		,
		yaxis: {
		        tickOptions:
					{
					// prefix: '$',
					suffix: '&deg;'
					}
				// min:0,
				// max:100
		          }
    },
    series:[{lineWidth:2, markerOptions:{style:'square'}}]
  });
  
  
	\$(".jqplot-axis, .jqplot-title").css("color","#fff");
   
</script>

HTML
