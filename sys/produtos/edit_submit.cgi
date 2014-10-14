#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "76";
require "../cfg/init.pl";
$ID        = &get('ID');

# Dados
$COD          = &get('COD');
$descrp       = &get('descrp');
$preco_custo  = &get('preco');
$preco_venda  = &get('preco_venda');
$status       = &get('status_radios');
$obs          = &get('obs');
$modelo       = &get('modelo');
$marca        = &get('marca');
$marca_descrp = &get('marca_descrp');
$link         = &get('link');
$partnumber   = &get('partnumber');
$unidade      = &get('unidade_radios');


# ajusta para salvar no banco
$preco_custo =~ s/\.|\,//g; # remove pontos
if(length($preco_custo) > 2) {
    substr($preco_custo, 0, -2) .= '.';
}

$preco_venda =~ s/\.|\,//g; # remove pontos
if(length($preco_venda) > 2) {
    substr($preco_venda, 0, -2) .= '.';
}

print $query->header({charset=>utf8});

# inicia bloco sql
$dbh->begin_work;

# marca
if(!$marca) {
    $DBM = DBE("
        select 
            codigo
        from 
            prod_marca
        where
            descrp <=> '$marca_descrp' and
            parceiro = $USER->{usuario}
        limit 1
    ");

    if($DBM->rows() > 0) {
        $m = $DB->fetchrow_hashref;
        $marca = $m->{codigo};
    } else {
        $marca = DBE("
            insert into 
                prod_marca (
                    descrp
                ) values (
                    '$marca_descrp'
                )
        ");
    }
}


#
#   Statments
#
if($COD) { # update 
    # update
    DBE("
        update 
            prod_mercadorias
        set
            descrp       = '$descrp', 
            marca        = '$marca',
            preco_custo  = '$preco_custo',  
            preco_venda  = '$preco_venda', 
            modelo       = '$modelo',
            partnumber   = '$partnumber',
            link         = '$link',
            obs          = '$obs',
            unidade      = '$unidade',
            status       = '$status'  
        where
            codigo   = $COD and
            parceiro = $USER->{empresa}
    ");
    
} else { # NEW

    # insere
    $COD = DBE("
        insert into 
            prod_mercadorias (
                descrp, 
                marca,
                preco_custo,
                preco_venda,
                modelo,
                partnumber,
                link,
                obs,
                unidade,
                status,
                parceiro
            ) values (
                '$descrp', 
                $marca,
                '$preco_custo',
                '$preco_venda',
                '$modelo',
                '$partnumber',
                '$link',
                '$obs',
                $unidade,
                '$status', 
                $USER->{empresa}
            ) 
    ");
        
    $CODNEW = ' , "COD" : "$COD" ';
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



