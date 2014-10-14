#!/usr/bin/perl

#
# estatisticas.cgi
#   estatisticas dos clientes
#

$nacess = "2";
require "../cfg/init.pl";

$ID      = &get('ID');
$PERIODO    = &get('periodo');

if($PERIODO eq "") {
	$PERIODO = &timestamp('yearmonth');
}

print $query->header({charset=>utf8});


# total tickets
$DB = DBE("
            select 
                count(distinct(tkt_codigo)) as tkts
                , to_char(sum(tempo), 'HH24MI') as tempo
            from 
                tkt_acao_tkt 
            where 
                to_char(data_execucao, 'YYYY-MM') = '$PERIODO' and 
                tkt_cancelado is false
                and tempo is not null
                and tkt_empresa_logada = $USER->{empresa}
    ");
$TKT = $DB->fetchrow_hashref;

# tecnico e tempo gasto
$DB = DBE("
            select 
            	distinct executor as id, 
                executor_nome as nome, 
                to_char(sum(tempo), 'HH24MI') as total, 
                sum(tempo) as total_show, 
                count(distinct(tkt_codigo)) as tkts 
            from 
            	tkt_acao_tkt_full 
            where 
                to_char(data_execucao, 'YYYY-MM') = '$PERIODO' and 
            	tkt_cancelado is false and 
                tempo is not null 
                and tkt_empresa_logada = $USER->{empresa}
            group by 
            	executor_nome, executor
            order by total_show desc
        ");
        
if($DB->rows() > 0) {
    while($T = $DB->fetchrow_hashref) {
    	$porcentagem = &percentage(($T->{total} * 100) / $TKT->{tempo});
        $ps = $porcentagem;
        $ps =~ s/\,/\./g;
    
        $R .= "{";
    	$R .= "     val    : $T->{id},";
    	$R .= "     descrp : '";
        $R .= "         <div class=\"DTouchRadio_list_line\">";
        $R .= "             <div style=\"width:62%\">$T->{nome}:</div>";
        $R .= "             <div style=\"width:10%\">[$T->{tkts}]</div>";
        $R .= "             <div style=\"width:10%\"> ".(&dateToShow($T->{total_show},"TIME"))."h </div>";
        $R .= "             <div style=\"width:17%; position:relative; text-align:center;\">";
        $R .= "                 $porcentagem%";
        $R .= "                 <span class=\"customer_status_percent\" style=\"width:$ps%\"></span>";
        $R .= "             </div>";
        $R .= "         </div>";
        $R .= "'},";
    }
} else {
    $R = "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}


$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= " 	<div style=\"width:58%\">Técnico</div>";
$title .= " 	<div style=\"width:12%\">Tickets</div>";
$title .= " 	<div style=\"width:10%\">Tempo</div>";
$title .= " 	<div style=\"width:17%; position:relative; text-align:center;\">%";
$title .= "         <span class=\"customer_status_percent\" style=\"width:100%\"></span>";
$title .= "     </div> ";
$title .= "</div>";

    
# retorno do codigo 
print<<HTML;
<script>
	\$("#tec_status").DTouchRadio({
        orientation  : "vertical",
        title        : '$title',
        addItem      : [$R],
        postFunction : function(){
            \$("#dashboard_filter_date").fieldDateTime({
                type         : "year-month",
                postFunction : function(x){
                    dashboard.widget.customer_status.load(x);
                }
            });
        },
		click: function(res) { 
            if(res.value === "0"){
                return false;
            }  
            
            call("cad/empresa/edit.cgi",{COD:res.value}); // edicao empresa
        }
	});
 
</script>

HTML
