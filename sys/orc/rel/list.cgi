#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "81";
require "../../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD         = &get('COD');
$dt_ini    = &dateToSave(&get('dt_ini'));
$dt_end    = &dateToSave(&get('dt_end'));
$categoria = &dateToSave(&get('filter_cat_radio'));


print $query->header({charset=>utf8});


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
            to_char(aprovado, 'YYYY-MM-DD') >= '$dt_ini' and 
            to_char(aprovado, 'YYYY-MM-DD') <= '$dt_end' and 
            o.parceiro = $USER->{empresa}
");

if($DB->rows() > 0) {    
    while($o = $DB->fetchrow_hashref) {
        if($o->{total} !~ /\./){
            $o->{total} .= ".00";
        } elsif($o->{total} =~ /\.\d{1}$/){ 
            $o->{total} .= "0";
        }
        
        $list .= '{';
        $list .= '  "codigo" : "'.$o->{codigo}.'",';
        $list .= '  "empresa" : "'.$o->{empresa_nome}.'",';
        $list .= '  "descrp" : "'.$o->{descrp}.'",';
        $list .= '  "valor"  : "'.$o->{total}.'",';
        $list .= '  "valor"  : "'.$categoria.'"';
        $list .= '},';
    }
}


$list = '['.substr($list, 0,-1).']';
print $list;

