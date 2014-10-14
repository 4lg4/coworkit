#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "2";
require "../cfg/init.pl";
$ID        = &get('ID');

# variaveis
$COD    = &get('COD');
$TBL    = &get('TBL');
$descrp = &get('descrp');

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
            $TBL
        set
            descrp  = '$descrp' 
        where
            codigo   = $COD and
            parceiro = $USER->{empresa}
    ");
    
} else { # NEW

    # insere
    $COD = DBE("
        insert into 
            $TBL (
                descrp,
                parceiro
            ) values (
                '$descrp', 
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


