#!/usr/bin/perl

#
#   relatorio_reativar.cgi
#
#       reativa lancamentos unicos ou todos
#       quando reativa todos desmarca itens selecionados para cobranca e 
#       remove todas entradas na tbl cob_tkt_item e cob_tkt
#

$nacess = "49";
require "../../cfg/init.pl";

$ID      = &get('ID');             # id testes de sessao
$COD     = &get('COD');            # codigo para edicao

$reativar = &get('reativar');      # codigo ou "all" 
@item     = &get_array('item_tkt_acao');

print $query->header({charset=>utf8}); # headers

# inicia SQls execs
$dbh->begin_work;

#  Statments
if($reativar eq "all"){ # reativa todos lancamentos
    
    # gera lista de filhos
    foreach $i (@item) {    
        # atualiza item no ticket
        &DBE("
            update tkt_acao set 
                faturado = NULL
            where
                codigo = $i
        ");
    }    
    
    # delete cob itens
    &DBE("
        delete from 
            cob_tkt_item
        where
            cob_tkt = $COD
    ");
    
    # delete cob
    &DBE("
        delete from 
            cob_tkt
        where
            codigo = $COD
    ");
    
    
    # atualiza modulo
    print "<script>eos.core.call.module.tkt_rel()</script>";
    
} else { # reativa lancamento especifico
    
    # remove item da cobranca
    &DBE("
        delete from 
            cob_tkt_item 
        where
            tkt_acao = $reativar
    ");
    
    # atualiza item no ticket
    &DBE("
        update tkt_acao set 
            faturado = NULL
        where
            codigo = $reativar
    ");

}

# finaliza SQLs
$dbh->commit;

exit;

