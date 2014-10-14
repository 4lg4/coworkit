#!/usr/bin/perl

$nacess = '204';
require "../cfg/init.pl";

$ID       = &get('ID');
$empresa  = &get('empresa');
$endereco = &get('endereco');
$grupo    = &get('grupo');
$agrupo   = &get('agrupo');
$linha    = &get('linha');

$itemDel  = &get('itemDel');
$acao = "update";

@GRUPO_ITEM       = &get_array('GRUPO_ITEM_');
@GRUPO_ITEM_VALOR = &get_array('GRUPO_ITEM_VALOR_');


print $query->header({charset=>utf8});


#
#   Remove item
#           
if($linha ne "" && $itemDel) {
    $dbh->begin_work;
    
    $debug .= "delete from grupo_empresa where empresa = $empresa and endereco = $endereco and linha = $linha and grupo = $grupo; | ";
    $rv = DBE("
            delete from 
                grupo_empresa 
            where 
                empresa  = '$empresa' and 
                endereco = '$endereco' and 
                linha    = '$linha' and 
                grupo    = '$grupo' 
    ");
    
    # historico
    DBE("
        insert into 
            dados_ti_historico (
                usuario,
                parceiro,
                acao,
                sql
            ) values (
                $USER->{usuario},
                $USER->{empresa},
                'delete',
                '$debug'
            )
    ");
    
    $dbh->commit;
    
    
    $R  = '{';
    $R .= '    "status"  : "success", ';
    $R .= '    "message" : "Item removido com Sucesso !"';
    $R .= '}';

    print $R;
    exit;
}



#
#   New / Update item
#       

$dbh->begin_work;

#
#   Insert item
# 
if($linha eq "") {
	$sth4 = DBE("
        select 
            max(linha) 
        from 
            grupo_empresa 
        where 
            empresa  = '$empresa' and 
            endereco = '$endereco' and 
            grupo    = '$grupo'
        limit 1 
    ");

	if($sth4->rows() == 0) {
        $R  = '{';
        $R .= '    "status"  : "error", ';
        $R .= '    "message" : "Item não encontrado !"';
        $R .= '}';
        print $R;
        exit;
        
	} else {
        
		$row4 = $sth4->fetch;
		$LINHA = @$row4[0];
		$linha = $LINHA + 1;
            
	}
    
    $acao = "insert";
}




#
#   remove item
#
# $debug .= "delete from grupo_empresa where empresa  = $empresa and endereco = $endereco and linha = $linha and grupo = $grupo; | ";
$rv = DBE("
        delete from 
            grupo_empresa 
        where 
            empresa  = '$empresa' and 
            endereco = '$endereco' and 
            linha    = '$linha' and 
            grupo    = '$grupo' 
");

# 
#   grava item
# 
$c = 0;
foreach $gi (@GRUPO_ITEM) {
    
    # $debug .= "insert into grupo_empresa (empresa, endereco, linha, grupo, grupo_item, valor) values ($empresa, $endereco, $linha, $grupo, $GRUPO_ITEM[$c], \"$GRUPO_ITEM_VALOR[$c]\"); | ";
    
	$rv = DBE("
        insert into 
            grupo_empresa (
                empresa, 
                endereco, 
                linha, 
                grupo, 
                grupo_item, 
                valor
            ) values (
                '$empresa', 
                '$endereco', 
                '$linha', 
                '$grupo', 
                '$GRUPO_ITEM[$c]', 
                '$GRUPO_ITEM_VALOR[$c]'
            ) 
    ");
    
    $c += 1;
}


# historico
DBE("
    insert into 
        dados_ti_historico (
            usuario,
            parceiro,
            acao,
            sql
        ) values (
            $USER->{usuario},
            $USER->{empresa},
            '$acao',
            '$debug'
        )
");

$dbh->commit;

    
$R  = '{';
$R .= '    "status"  : "success", ';
$R .= '    "message" : "Item atualizado com Sucesso !"';
# $R .= '    , "debug" : "'.$debug.'"';
$R .= '}';

print $R;

