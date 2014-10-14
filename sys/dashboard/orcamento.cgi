#!/usr/bin/perl

#
# chamado.cgi
#
# Lista de chamados que aparecem no modulo
#

$nacess = "2";
# $nacess_more = "or menu = 74";
require "../cfg/init.pl";

$ID = &get('ID');

$DB = DBE("
    select 
        o.*,
        e.nome as empresa_nome,
		(select sum(quantidade * valor) from orc_item where orc = o.codigo) as total
    from 
        orc as o
    left join
        empresa as e on e.codigo = o.empresa
    where
        o.parceiro = $USER->{empresa} and
        aprovado is null and
        cancelado is null
");

if($DB->rows() > 0) {
        
    while($o = $DB->fetchrow_hashref) {
        
        if(!$o->{parceiro}) {
            $nochange = "nochange";
        } else {
            $nochange = "";
        }
         
        if($o->{status} == 0) {
            $ckd = "Não";
        } else {
            $ckd = "Sim";
        }
        
        # valor
        if($o->{valor} !~ /\./){
            $o->{valor} .= ".00";
        } elsif($o->{valor} =~ /\.\d{1}$/){ 
            $o->{valor} .= "0";
        }
        $o->{valor} =~ s/\./\,/g;
           
        $orcamento .= "{";
        $orcamento .= "  \"val\"    : \"$o->{codigo}\",";
        $orcamento .= "  \"descrp\" : \"";
        $orcamento .= "     <div class='DTouchRadio_list_line $nochange'>";
        $orcamento .= "         <div style='width:6%'>#$o->{codigo}</div>";
        $orcamento .= "         <div style='width:10%'>".(&dateToShow($o->{data}))."</div>";
        $orcamento .= "         <div style='width:30%'>$o->{empresa_nome}</div>";
        $orcamento .= "         <div style='width:40%'>$o->{descrp}</div>";
        $orcamento .= "         <div style='width:10%'>$o->{total}</div>";
        $orcamento .= "     </div>";
        $orcamento .= "\"},";
	}
} else {
        $orcamento .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:7%\">Código</div> ";
$title .= "	<div style=\"width:10%\">Data</div> ";
$title .= "	<div style=\"width:20%\">Empresa</div> ";
$title .= "	<div style=\"width:47%\">Descrição</div> ";
$title .= "	<div style=\"width:10%\">Valor</div> ";
$title .= "</div>";





$os .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
$ostitle  = "<div class=\"DTouchRadio_list_title\">";
$ostitle .= "	<div style=\"width:7%\">Código</div> ";
$ostitle .= "	<div style=\"width:20%\">Orçamento / Pedido</div> ";
$ostitle .= "	<div style=\"width:10%\">Data</div> ";
$ostitle .= "	<div style=\"width:40%\">Empresa</div> ";
$ostitle .= "</div>";


# retorno do codigo 
print $query->header({charset=>utf8});

print<<HTML;
<script>
var content  = '<div id="orcs">';
    content += '    <ul>';
    content += '        <li><a href="#orc_pedentes_tab">Orçamentos Pendentes</a></li>';
    content += '        <li><a href="#orc_exec_tab">O.S. em Execução</a></li>';
    content += '    </ul>';
    content += '    <div id="orc_exec_tab"><div id="orc_exec"></div></div>';
    content += '    <div id="orc_pedentes_tab"><div id="orc_pendentes"></div></div>';
    content += '</div>';
    
\$("#dashboard_orc_container").html(content);

\$("#orc_pendentes").DTouchRadio({ 
    title: '$title',
	addItem:[ $orcamento ], 
	orientation:'vertical',
	click: function(res) {
        if(res.value === "0"){
            return false;
        }
        
		eos.core.call.module.orc(res.value); // edita tkt
	}
});

\$("#orc_exec").DTouchRadio({ 
    title: '$ostitle',
	addItem:[ $os ], 
	orientation:'vertical',
	click: function(res) {
        if(res.value === "0"){
            return false;
        }
        
		// eos.core.call.module.orc(res.value); // edita tkt
	}
});

\$("#orcs").tabs();
</script>
HTML
