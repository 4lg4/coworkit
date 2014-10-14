#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "81";
require "../../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD         = &get('COD');
$dt_ini    = &dateToSave(&get('dt_ini'));
$dt_end    = &dateToSave(&get('dt_end'));


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
        $list .= '  "valor"  : "'.$o->{total}.'"';
        $list .= '},';
    }
}
$list = '['.substr($list, 0,-1).']';
print $list;
exit;


# 
# codigo abaixo copiado do modulo de orcamento, mas ainda nao implementado nesta versao
# 

# inicia bloco sql
$dbh->begin_work;

#
#   Statments
#
if($COD) { # update 
    # update
    DBE("
        update 
            orc
        set
            descrp       = '$descrp', 
            obs          = '$obs', 
            empresa      = '$empresa',
            endereco     = '$endereco',
            responsavel  = '$responsavel',
            validade     = '$validade'
        where
            codigo   = $COD and
            parceiro = $USER->{empresa}
            $aprovals
    ");
    
} else { # NEW

    


    # insere
    $COD = DBE("
        insert into 
            orc (
                usuario,
                empresa,
                endereco,
                descrp, 
                obs,
                responsavel,
                validade,
                parceiro
            ) values (
                $USER->{empresa},
                $empresa,
                $endereco,
                '$descrp', 
                '$obs',
                '$responsavel', 
                $validade,
                $USER->{empresa}
            ) 
    ");
        
    $CODNEW = ' , "COD" : "'.$COD.'" ';
}



#
#   itens
#

#
# servicos
#
foreach $s (@servico) {
    $codigo      = &get("servico_codigo_$s");
    $codigo_item = &get("servico_codigo_item_$s");
    $quantidade  = &get("servico_qtd_$s");
    $valor       = &get("servico_valor_$s");
    $descrp      = &get("servico_descrp_$s");

    # insere novo servico direto
    if($codigo eq "new" || !$codigo) {
        $codigo = &DBE("
            insert into prod_serv (
                descrp, 
                valor,
                parceiro
            ) values (
                '$descrp',
                '$valor',
                $USER->{empresa}
            )
        ");
    }

    # update
    if($codigo_item) {
        DBE("
            update 
                orc_item
            set
                modificado_data    = now(),
                modificado_usuario = $USER->{usuario},
                orc                = $COD,
                quantidade         = '$quantidade',
                valor              = '$valor'
            where
                codigo = $codigo_item
        ");
        
    # insert new item 
    } else {
        $itens .= "($USER->{usuario}, $COD, '$quantidade', '$valor', 'prod_serv', $codigo),";
    }
}
# insere filhos
if($itens) {
    $itens = substr($itens, 0,-1); # remove ultima virgula
    DBE("
        insert into orc_item (
            usuario, 
            orc, 
            quantidade, 
            valor, 
            link_tbl, 
            link_codigo
        ) values
            $itens
    ");
}


#
# produtos
#
foreach $p (@produto) {
    $codigo      = &get("produto_codigo_$p");
    $codigo_item = &get("produto_codigo_item_$p");
    $quantidade  = &get("produto_qtd_$p");
    $valor       = &get("produto_valor_$p");

    # update
    if($codigo_item) {
        DBE("
            update 
                orc_item
            set
                modificado_data    = now(),
                modificado_usuario = $USER->{usuario},
                orc                = $COD,
                quantidade         = '$quantidade',
                valor              = '$valor'
            where
                codigo = $codigo_item
        ");
        
    # insert new item 
    } else {
        $itensp .= "($USER->{usuario}, $COD, '$quantidade', '$valor', 'prod_mercadorias', $codigo),";
    }
}
# insere filhos
if($itensp) {
    $itensp = substr($itensp, 0,-1); # remove ultima virgula
    &DBE("
        insert into orc_item (
            usuario, 
            orc, 
            quantidade, 
            valor, 
            link_tbl, 
            link_codigo
        ) values
            $itensp
    ");
}
    


#
# despesas
#
foreach $d (@despesa) {
    $codigo      = &get("despesa_codigo_$d");
    $codigo_item = &get("despesa_codigo_item_$d");
    $descrp      = &get("despesa_descrp_$d");
    $valor       = &get("despesa_valor_$d");
    
    $aaa .= $codigo." - ".$codigo_item." - ".$valor.", ";
    
    
    # insere novo servico direto
    if($codigo eq "new" || !$codigo) {
        $codigo = &DBE("
            insert into prod_despesas (
                descrp, 
                parceiro
            ) values (
                '$descrp',
                $USER->{empresa}
            )
        ");
    }
    
    # update
    if($codigo_item) {
        DBE("
            update 
                orc_item
            set
                modificado_data    = now(),
                modificado_usuario = $USER->{usuario},
                orc                = $COD,
                valor              = '$valor'
            where
                codigo = $codigo_item
        ");

    # insert new item 
    } else {
        $itensd .= "($USER->{usuario}, $COD, '$valor', 'prod_despesas', $codigo),";
    }
}
# insere filhos
if($itensd) {
    $itensd = substr($itensd, 0,-1); # remove ultima virgula
    &DBE("
        insert into orc_item (
            usuario, 
            orc, 
            valor, 
            link_tbl, 
            link_codigo
        ) values
            $itensd
    ");
}


# end bloco sql
$dbh->commit;   
    
# mensagem
$R  = '{ ';
$R .= '     "status"  : "success", ';
$R .= '     "message" : "Cadastro alterado com sucesso" ';
$R .= $CODNEW;
$R .= '}  ';
print $R;



