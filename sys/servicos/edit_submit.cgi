#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "51";
require "../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD    = &get('COD');
$descrp = &get('descrp');
$valor  = &get('valor');
$status = &get('status_radios');

# ajusta para salvar no banco
$valor =~ s/\.|\,//g; # remove pontos
if(length($valor) > 2) {
    substr($valor, 0, -2) .= '.';
}

print $query->header({charset=>utf8});

# inicia bloco sql
# $dbh->begin_work;

#
#   Statments
#
if($COD) { # update 
    # update
    DBE("
        update 
            prod_serv
        set
            descrp       = '$descrp', 
            valor        = '$valor',
            status       = '$status'  
        where
            codigo   = $COD and
            parceiro = $USER->{empresa}
    ");
    
} else { # NEW

    # insere
    $COD = DBE("
        insert into 
            prod_serv (
                descrp, 
                valor,
                status,
                parceiro
            ) values (
                '$descrp', 
                '$valor',
                '$status', 
                $USER->{empresa}
            ) 
    ");
        
    $CODNEW = ' , "COD" : "$COD" ';
}

# end bloco sql
# $dbh->commit;   
    
# mensagem
$R  = '{ ';
$R .= '     "status"  : "success", ';
$R .= '     "message" : "Cadastro alterado com sucesso" ';
$R .= $CODNEW;
$R .= '}  ';
print $R;



