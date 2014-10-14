#!/usr/bin/perl

$nacess = "81";
require "../../cfg/init.pl";

# vars
$ID  = &get('ID');
$COD = &get('COD');

# statment
$DB = DBE("
    select 
        o.*,
        e.nome as empresa_nome,
        ee.endereco as endereco_descrp,
        ee.complemento,
        ee.bairro,
        ee.cidade,
        ee.uf,
        te.descrp as tipo_descrp,
        (select sum(quantidade * valor) from orc_item where orc = o.codigo) as total
    from 
        orc as o
    join 
        empresa as e on 
            e.codigo = o.empresa
    join 
        empresa_endereco as ee on 
            ee.empresa = o.endereco
    left join 
        tipo_endereco as te on 
            te.codigo = ee.tipo
    where
        o.codigo = $COD and
        o.parceiro = $USER->{empresa}
");

# plano
$orc = $DB->fetchrow_hashref;

if($orc->{valor} !~ /\./){
    $orc->{valor} .= ".00";
} elsif($orc->{valor} =~ /\.\d{1}$/){ 
    $orc->{valor} .= "0";
}

$endereco = "($orc->{tipo_descrp} - $orc->{endereco_descrp}, $orc->{complemento} - $orc->{bairro} / $orc->{cidade} - $orc->{uf})";

$endereco_pdf = "$orc->{endereco_descrp}, $orc->{complemento} - $orc->{bairro} / $orc->{cidade} - $orc->{uf}";
$pdf_bg = "bgcolor='#FFFFFF'";

# itens
$DB = DBE("
    select
		codigo,
        link_tbl,
        link_codigo,
        quantidade,
		valor,
        sum(quantidade * valor) as total 
    from 
        orc_item 
    where
        orc = $orc->{codigo}
	group by 
		codigo,
        link_tbl,
        link_codigo,
		quantidade,
		valor
");

while($i = $DB->fetchrow_hashref) {
    # pega descritivo do item
    if($i->{link_tbl} eq "prod_mercadorias"){ # ajusta descritivo das mercadorias
        $link_tbl = "prod_mercadorias_full";
    } else {
        $link_tbl = $i->{link_tbl};
    }
    $DBD = DBE("select * from $link_tbl where codigo = $i->{link_codigo}");
    $id  = $DBD->fetchrow_hashref;
    
    $itens .= '{';
    $itens .= '     "codigo"      :  "'.$i->{codigo}.'",  ';
    $itens .= '     "quantidade"  :  "'.$i->{quantidade}.'",  ';
    $itens .= '     "valor"       :  "'.$i->{valor}.'",  ';
    $itens .= '     "total"       :  "'.$i->{total}.'",  ';
    $itens .= '     "descrp"      :  "'.$id->{descrp}.'",  ';
    $itens .= '     "link_codigo" :  "'.$i->{link_codigo}.'",  ';
    $itens .= '     "link_tbl"    :  "'.$i->{link_tbl}.'",  ';
    
    $itens .= '     "modelo"      :  "'.$id->{modelo}.'",  ';
    $itens .= '     "marca"       :  "'.$id->{marca_descrp}.'",  ';
    $itens .= '     "partnumber"  :  "'.$id->{partnumber}.'",  ';
    $itens .= '     "unidade"     :  "'.$id->{unidade_descrp}.'"  ';
    
    $itens .= '},';
    
    # impressao dos itens pdf
    if($pdf) {
        
        if($id->{modelo} || $id->{marca_descrp} || $id->{partnumber} || $id->{unidade_descrp}) {
            $descrp = " (".$id->{modelo}." ".$id->{marca_descrp}." ".$id->{partnumber}." ".$id->{unidade_descrp}.") ";
        } else {
            $descrp = "";
        }
        
        $i->{valor} =~ s/R\$//gm;
        $i->{total} =~ s/R\$//gm;
        

        $pdf_itens .= "<tr $pdf_bg>";
        $pdf_itens .= "   <td width='50%' valign='top'>".decode("utf8",$id->{descrp}.$descrp)."</td>";
        $pdf_itens .= "   <td align='right' valign='top' width='10%'>$i->{quantidade}</td>";
        $pdf_itens .= "   <td align='right' valign='top' width='20%'>$i->{valor}</td>";
        $pdf_itens .= "   <td align='right' valign='top' width='20%'>$i->{total}</td>";
        $pdf_itens .= "</tr>";
        
        if(!$pdf_bg){
            $pdf_bg = "bgcolor='#FFFFFF'";
        } else {
            $pdf_bg = "";
        }
    }
    
}
$itens = ',"itens" : ['.substr($itens, 0,-1).']';


    $R  = '{ ';
    $R .= '     "descrp"      : "'.$orc->{descrp}.'",  ';
    $R .= '     "status"      : "'.$orc->{status}.'",  ';
    $R .= '     "responsavel" : "'.$orc->{responsavel}.'",  ';
    $R .= '     "obs"         : "'.$orc->{obs}.'",  ';
    $R .= '     "total"       : "'.$orc->{total}.'",  ';
    $R .= '     "aprovado"    : "'.dateToShow($orc->{aprovado},"date").'",  ';
    $R .= '     "aprovado_descrp" : "'.$orc->{aprovado_descrp}.'",  ';
    $R .= '     "aprovado_status" : "'.$orc->{aprovado_status}.'",  ';
    $R .= '     "validade"    : "'.dateToShow($orc->{validade},"date").'",  ';
    $R .= '     "cliente"     :  { ';
    $R .= '         "codigo"     :  "'.$orc->{empresa}.'",  ';
    $R .= '         "descrp"     :  "'.$orc->{empresa_nome}.'"  ';
    $R .= '     }, ';
    $R .= '     "endereco"     :  { ';
    $R .= '         "codigo"     :  "'.$orc->{endereco}.'",  ';
    $R .= '         "descrp"     :  "'.$endereco.'"  ';
    $R .= '     } ';
    $R .= $itens;
    $R .= '}  ';

    # impressao dos itens pdf
    if($pdf) {
        $pdf_orc = $orc;
        $pdf_orc->{total} =~ s/R\$//gm;
        $pdf_orc->{empresa_nome} = decode("utf8",$pdf_orc->{empresa_nome});
        $pdf_orc->{endereco_descrp} = decode("utf8",$endereco_pdf);
        
        
        
        $pdf_itens .= "<tr $pdf_bg>";
        $pdf_itens .= "   <td colspan='3' align='right'><b>Total R\$</b></td>";
        $pdf_itens .= "   <td align='right'>$pdf_orc->{total}</td>";
        $pdf_itens .= "</tr>";        
    }

# print
# se NAO for pdf retorna JSON
if(!$pdf) {
    print $query->header({charset=>utf8});
    print $R;
} else {
    return true;
}