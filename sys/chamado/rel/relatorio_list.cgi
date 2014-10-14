#!/usr/bin/perl

#
#   relatorio_list.cgi
#
#       Lista de relatorios gerados
#

$nacess = "49";
require "../../cfg/init.pl";

$ID          = &get('ID');
$req         = &get('req');
$competencia = &get('competencia');

print $query->header({charset=>utf8}); # headers

# finalizados
# if($finalizado eq "true") { # ajusta query se finalizados somente
#    $finalizado_where = " and tkt_finalizado is not null ";
# }

# competencia
if(!$competencia){
    $competencia = timestamp("yearmonth");
}

# statment
$where  = " ct.empresa_logada = $USER->{empresa} ";
# $where .= " and to_char(ct.competencia, 'YYYY-MM') = '$competencia' ";
$DB = &DBE("
    select 
     	ct.*, e.nome as empresa_nome, 
     	(select sum(cti.executado) from cob_tkt_item as cti where cti.cob_tkt = ct.codigo) as executado, 
    	(select sum(cti.faturado) from cob_tkt_item as cti where cti.cob_tkt = ct.codigo) as faturado
    from 
        cob_tkt as ct
        left join empresa as e on e.codigo = ct.empresa
    where
        $where
    order by competencia, empresa_nome
");

# gera radio
if($DB->rows() > 0) {    
        
	while($item = $DB->fetchrow_hashref) {
        
		$item->{obs} = &get($item->{obs}, "NEWLINE_SHOW"); 
        
        if($item->{encerrar}) {
            $encerrado = " relatorio_encerrado ";
        } else {
            $encerrado = " ";
        }
        
        $array_radio_chamado .= "{";
		$array_radio_chamado .= "val:$item->{codigo},descrp: '";
		$array_radio_chamado .= "<div class=\"DTouchRadio_list_line $encerrado \">";
		$array_radio_chamado .= " 	<div style=\"width:5%;\">$item->{codigo}</div> ";
        $array_radio_chamado .= " 	<div style=\"width:10%;\">$item->{empresa_nome}</div> ";
		$array_radio_chamado .= " 	<div style=\"width:10%\">".(&dateToShow($item->{competencia},"YEARMONTH"))."</div>";
		$array_radio_chamado .= " 	<div style=\"width:15%\">".(&dateToShow($item->{data}))."</div>";
		$array_radio_chamado .= " 	<div style=\"width:30%\">$item->{obs}</div>";
        $array_radio_chamado .= " 	<div style=\"width:15%\">".(&dateToShow($item->{executado}))."h</div> ";
        $array_radio_chamado .= " 	<div style=\"width:15%\">".(&dateToShow($item->{faturado}))."h</div> ";
		$array_radio_chamado .= "</div>";    
        $array_radio_chamado .= "'},";
    }
    
} else {
    $array_radio_chamado .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}
		

    $radio_title  = "<div class=\"DTouchRadio_list_title\">";
    $radio_title .= "	<div style=\"width:5%\">Cod.</div>";
	$radio_title .= "	<div style=\"width:10%\">Cliente</div>";
	$radio_title .= "	<div style=\"width:10%\">Competência</div>";
	$radio_title .= "	<div style=\"width:15%\">Dt. Gerado</div>";
    $radio_title .= "	<div style=\"width:30%\">Obs</div> ";
	$radio_title .= "	<div style=\"width:15%\">Executado</div> ";
    $radio_title .= "	<div style=\"width:15%\">Faturado</div> ";
    $radio_title .= "</div>";
	
# print radio
print<<HTML;
<script>
	\$("#relatorio_list").DTouchRadio({ 
        addItem     : [$array_radio_chamado], 
		orientation : 'vertical',
		title       : '$radio_title',
		search      : true,
        postFunction : function(x) {

        },
		click : function(x) {
            if(x.value === 0){
                return true;
            }

            form.edit(x.value);
		}
	});
</script>
HTML
