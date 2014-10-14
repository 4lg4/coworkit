#!/usr/bin/perl

#
#   relatorio_list.cgi
#
#       Lista de relatorios gerados
#

$nacess = "49";
require "../../cfg/init.pl";

$ID          = &get('ID');
$competencia = timestamp("yearmonth");
$competencia_show = timestamp("yearmonth-br");

print $query->header({charset=>utf8}); # headers

# statment
$DB = &DBE("
    select 
       empresa_nome
	   , empresa
	   , count(empresa) as tkt_total
       , sum(executado) as executado

    from 
        cob_clientes_list 
    where
        empresa_logada = $USER->{empresa}
    group by
		empresa
        , empresa_nome
    order by 
        empresa_nome asc
        
        
        
");

# gera radio
if($DB->rows() > 0) {    
        
	while($item = $DB->fetchrow_hashref) {        
        $array_radio_chamado .= "{";
		$array_radio_chamado .= "val:$item->{empresa},descrp: '";
		$array_radio_chamado .= "<div class=\"DTouchRadio_list_line\">";
        $array_radio_chamado .= " 	<div style=\"width:70%;\" class=\"clientes_list_empresa_nome\">$item->{empresa_nome}</div> ";
        $array_radio_chamado .= " 	<div style=\"width:15%;\">$item->{tkt_total}</div> ";
        $array_radio_chamado .= " 	<div style=\"width:15%\">".(&dateToShow($item->{executado}))."h</div> ";
		$array_radio_chamado .= "</div>";    
        $array_radio_chamado .= "'},";
    }
    
} else {
    $array_radio_chamado .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}
		

    $radio_title  = "<div class=\"DTouchRadio_list_title\">";
	$radio_title .= "	<div style=\"width:65%\">Cliente</div>";
    $radio_title .= "	<div style=\"width:15%\">Tickets</div> ";
	$radio_title .= "	<div style=\"width:15%\">Executado</div> ";
    $radio_title .= "</div>";
	

# print radio
print<<HTML;
<script>
	\$("#clientes_list").DTouchRadio({ 
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
            
            \$("#empresa").fieldAutoComplete("value",{ id: x.value, val: \$(this).find(".clientes_list_empresa_nome").text()});
            \$("#competencia").val("$competencia_show");
            
            form.reset();
            form.page.DTouchPages("page","center");
            relatorio.genList();
		}
	});
</script>
HTML
