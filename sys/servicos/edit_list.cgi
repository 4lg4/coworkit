#!/usr/bin/perl

$nacess = "51";
require "../cfg/init.pl";
$ID = &get('ID');


$DB = DBE("
    select 
        *
    from 
        prod_serv
    where
        parceiro = $USER->{empresa}
    order by
        descrp 
    asc
");

if($DB->rows() > 0) {
        
    while($p = $DB->fetchrow_hashref) {
        
        if(!$p->{parceiro}) {
            $nochange = "nochange";
        } else {
            $nochange = "";
        }
         
        if($p->{status} == 0) {
            $ckd = "Não";
        } else {
            $ckd = "Sim";
        }
        
        # valor
        if($p->{valor} !~ /\./){
            $p->{valor} .= ".00";
        } elsif($p->{valor} =~ /\.\d{1}$/){ 
            $p->{valor} .= "0";
        }
        $p->{valor} =~ s/\./\,/g;
           
        $servicos .= "{";
        $servicos .= "  \"val\"    : \"$p->{codigo}\",";
        $servicos .= "  \"descrp\" : \"";
        $servicos .= "     <div class='DTouchRadio_list_line $nochange'>";
        $servicos .= "         <div style='width:50%'>$p->{descrp}</div>";
        $servicos .= "         <div style='width:20%'>$p->{valor}</div>";
        $servicos .= "         <div style='width:10%'>$ckd</div>";
        $servicos .= "     </div>";
        $servicos .= "\"},";
	}
} else {
        $servicos .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:50%\">Descrição</div> ";
$title .= "	<div style=\"width:20%\">Valor</div> ";
$title .= "	<div style=\"width:15%\">Ativo</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $servicos = substr($servicos, 0,-1);
# $servicos = "{$servicos}";

print<<HTML;
<script>
    \$("#servicos_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$servicos],
        click       : function(x){
            form.edit(x.value);
        }
    });
</script>
HTML

