#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "81";
require "../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD         = &get('COD');
$descrp      = &get('descrp');
$obs         = &get('obs');
$empresa     = &get('cliente');
$endereco    = &get('cliente_endereco');
$responsavel = &get('responsavel');
$validade    = &get('validade');

if(!$validade){
    $validade = NULL;
} else {
    $validade = "'".&dateToSave($validade)."'";
}

# itens
@servico    = &get_array('servico_id');
@produto    = &get_array('produto_id');
@despesa    = &get_array('despesa_id');



#print $query->header({charset=>utf8});
#debug($aaa);
#exit;


# ajusta para salvar no banco
#$valor =~ s/\.|\,//g; # remove pontos
#if(length($valor) > 2) {
#    substr($valor, 0, -2) .= '.';
#}

print $query->header({charset=>utf8});

#
# aprovals
#

# aprovado / recusado / cancelado
$aproval        = &get('aproval');
$aproval_descrp = &get('aproval_descrp');

# aprovado
if($aproval eq "true"){
    $aprovals  = " aprovado = now()";
    $aprovals  = ", aprovado_status = TRUE";
    $aprovals .= ", aprovado_descrp = '$aproval_descrp'";
# recusado
} elsif($aproval eq "false"){
    $aprovals  = " aprovado = now()";
    $aprovals  = ", aprovado_status = FALSE";
    $aprovals .= ", aprovado_descrp = '$aproval_descrp'";
# cancelado 
} else {
    $aprovals  = " cancelado = now()";
    $aprovals .= ", cancelado_descrp = '$aproval_descrp'";
}

# aprovals update
if($aprovals && $COD) { 
    # update
    DBE("
        update 
            orc
        set
            $aprovals
        where
            codigo   = $COD and
            parceiro = $USER->{empresa}
            
    ");
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "success", ';
    $R .= '     "message" : "Cadastro alterado com sucesso" ';
    $R .= '}  ';
    print $R;
    
    exit;
}



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



