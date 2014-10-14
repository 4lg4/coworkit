#!/usr/bin/perl

$nacess = "55";
require "../cfg/init.pl";
$ID = &get('ID');


$DB = DBE("
    select 
        ps.*,
        at.img as area_img,
        e.nome as empresa_nome
    from 
        prod_servicos as ps
    left join
        empresa_area_tipo as at on at.codigo = ps.empresa_area_tipo
    left join
        empresa as e on e.codigo = ps.empresa
    where
        ps.parceiro = $USER->{empresa}
    order by
        ps.descrp 
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
        
        if(!$p->{vigencia_ini}){
            $p->{vigencia_ini} = "";
        } else {
            $p->{vigencia_ini} = &dateToShow($p->{vigencia_ini},"date");
        }
        if(!$p->{vigencia_fim}){
            $p->{vigencia_fim} = "";
        } else {
            $p->{vigencia_fim} = &dateToShow($p->{vigencia_fim},"date");
        }
        
        # generico
        if(!$p->{empresa_nome}) {
            $p->{empresa_nome} = "Genérico";
        }
           
        $planos .= "{";
        $planos .= "  \"val\"    : \"$p->{codigo}\",";
        $planos .= "  \"descrp\" : \"";
        $planos .= "     <div class='DTouchRadio_list_line $nochange'>";
        $planos .= "         <div style='width:25%'>$p->{empresa_nome}</div>";
        $planos .= "         <div style='width:5%'><img src='$p->{area_img}' class='img_list'></div>";
        $planos .= "         <div style='width:20%'>$p->{descrp}</div>";
        $planos .= "         <div style='width:12%'>$p->{horas_plano}</div>";
        $planos .= "         <div style='width:10%'>$p->{obs}</div>";
        $planos .= "         <div style='width:20%'>$p->{vigencia_ini} - $p->{vigencia_fim}</div>";
        $planos .= "         <div style='width:5%'>$ckd</div>";
        $planos .= "     </div>";
        $planos .= "\"},";
	}
} else {
        $planos .= "{ val:0, descrp:'<div style=\"width:100%\">Nenhum registro encontrado !</div>' }";
}

$title  = "<div class=\"DTouchRadio_list_title\">";
$title .= "	<div style=\"width:24%\">Empresa</div> ";
$title .= "	<div style=\"width:5%\">Área</div> ";
$title .= "	<div style=\"width:17%\">Descrição</div> ";
$title .= "	<div style=\"width:12%\">Tempo</div> ";
$title .= "	<div style=\"width:15%\">Obs</div> ";
$title .= "	<div style=\"width:10%\">Vigência</div> ";
$title .= "	<div style=\"width:18%\">Ativo</div> ";
$title .= "</div>";

# print $query->header('application/json; charset="utf-8"');
print $query->header({charset=>utf8});

# $planos = substr($planos, 0,-1);
# $planos = "{$planos}";

print<<HTML;
<script>
    \$("#planos_list").DTouchRadio({
        orientation : "vertical",
    	title       : '$title',
    	search      : true,
        itemAdd     : [$planos],
        click       : function(x){
            form.edit(x.value);
        }
    });
</script>
HTML

