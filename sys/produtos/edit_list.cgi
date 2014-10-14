#!/usr/bin/perl

$nacess = "76";
require "../cfg/init.pl";
$ID = &get('ID');


$DB = DBE("
    select 
        *
    from 
        prod_mercadorias_full
    where
        parceiro = $USER->{empresa}
    order by
        descrp 
    asc
");

if($DB->rows() > 0) {
        
    while($p = $DB->fetchrow_hashref) {
         
        if($p->{status} == 0) {
            $ckd = "Não";
        } else {
            $ckd = "Sim";
        }
        
        # preco custo
        if($p->{preco_custo} !~ /\./){
            $p->{preco_custo} .= ".00";
        } elsif($p->{preco_custo} =~ /\.\d{1}$/){ 
            $p->{preco_custo} .= "0";
        }
        $p->{preco_custo} =~ s/\./\,/g;
        
        # preco porcentagem
        if($p->{preco_venda} !~ /\./){
            $p->{preco_venda} .= ".00";
        } elsif($p->{preco_venda} =~ /\.\d{1}$/){ 
            $p->{preco_venda} .= "0";
        }
        $p->{preco_venda} =~ s/\./\,/g;
           
        $produtos .= "{";
        $produtos .= "  \"val\"    : \"$p->{codigo}\",";
        $produtos .= "  \"descrp\" : \"";
        $produtos .= "     <div class='DTouchRadio_list_line $nochange'>";
        $produtos .= "         <div style='width:50%'>$p->{descrp}</div>";
        $produtos .= "         <div style='width:10%'>$p->{unidade_descrp}</div>";
        $produtos .= "         <div style='width:10%'>$p->{marca_descrp}</div>";
        $produtos .= "         <div style='width:10%'>$p->{preco_custo}</div>";
        $produtos .= "         <div style='width:10%'>$p->{preco_venda}</div>";
        $produtos .= "         <div style='width:10%'>$ckd</div>";
        $produtos .= "     </div>";
        $produtos .= "\"},";
	}
} else {
        $produtos .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:47%\">Descrição</div> ";
$title .= "	<div style=\"width:10%\">Unidade</div> ";
$title .= "	<div style=\"width:10%\">Marca</div> ";
$title .= "	<div style=\"width:10%\">Preço Custo</div> ";
$title .= "	<div style=\"width:10%\">Preço Venda</div> ";
$title .= "	<div style=\"width:8%\">Ativo</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $produtos = substr($produtos, 0,-1);
# $produtos = "{$produtos}";

print<<HTML;
<script>
    \$("#produtos_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$produtos],
        click       : function(x){
            form.edit(x.value);
        }
    });
</script>
HTML

