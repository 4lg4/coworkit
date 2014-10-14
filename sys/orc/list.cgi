#!/usr/bin/perl

$nacess = "81";
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
        o.parceiro = $USER->{empresa}
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
        $orcamento .= "         <div style='width:5%'>$o->{codigo}</div>";
        $orcamento .= "         <div style='width:10%'>".(&dateToShow($o->{data}))."</div>";
        $orcamento .= "         <div style='width:20%'>$o->{empresa_nome}</div>";
        $orcamento .= "         <div style='width:30%'>$o->{descrp}</div>";
        $orcamento .= "         <div style='width:20%'>$o->{total}</div>";
        $orcamento .= "         <div style='width:15%'>".(&dateToShow($o->{aprovado}))."</div>";
        $orcamento .= "     </div>";
        $orcamento .= "\"},";
	}
} else {
        $orcamento .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:5%\">Cod.</div> ";
$title .= "	<div style=\"width:10%\">Data</div> ";
$title .= "	<div style=\"width:15%\">Empresa</div> ";
$title .= "	<div style=\"width:28%\">Descrição</div> ";
$title .= "	<div style=\"width:20%\">Valor</div> ";
$title .= "	<div style=\"width:15%\">Aprovado</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $orcamento = substr($orcamento, 0,-1);
# $orcamento = "{$orcamento}";

print<<HTML;
<script>
    \$("#orcamento_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$orcamento],
        uncheck     : false,
        click       : function(x){
            orc.edit();
        }
    });
</script>
HTML

