#!/usr/bin/perl

#
#   relatorio_submit.cgi
#
#       executa db transactions 
#

$nacess = "49";
require "../../cfg/init.pl";

$ID      = &get('ID');             # id testes de sessao
$COD     = &get('COD');            # codigo para edicao

$competencia = &dateToSave(&get('competencia'));
$finalizado  = &get('finalizado');
$empresa     = &get('empresa');
$descrp      = &get('descrp');
$obs         = &get('obs');
@cobrar      = &get_array('cobrar');   # lista de emails
@item        = &get_array('item');     # lista de itens

print $query->header({charset=>utf8}); # headers

# inicia SQls execs
$dbh->begin_work;

#  Statments
if(!$COD){ # insert

    # ajusta variaveis
    if(!$finalizado){
        $finalizado = 'false';
    }

    # insere pai, recupera codigo inserido
    $COD = &DBE("insert into cob_tkt (
                usuario, empresa_logada, empresa, competencia, descrp, obs, finalizado 
            ) values (
              $USER->{usuario}, $USER->{empresa}, $empresa, '$competencia-01', '$descrp', '$obs', $finalizado
            ) ");
                
    # gera lista de filhos
    foreach $c (@cobrar) {    
        $tempo  = &get('cobrar_tempo_'.$c);
        $descrp = &get('cobrar_descrp_'.$c);
        $itens .= "($USER->{usuario}, $c, '$descrp', '$tempo', '$tempo', $COD),";
        
        # atualiza item no ticket
        &DBE("
            update tkt_acao set 
                faturado = now()
            where
                codigo = $c
        ");
    }
    $itens = substr($itens, 0,-1); # remove ultima virgula
    
    # insere filhos
    &DBE("
        insert into cob_tkt_item (
            usuario, tkt_acao, descrp, executado, faturado, cob_tkt
        ) values
            $itens
    ");
    
    # retorna em modo de edicao
    print "<script>form.edit($COD)</script>";
} else {

    # encerrar
    $encerrar = &get('encerrar');
    if($encerrar) {
        $encerrar = ", encerrar = now()";
    }

    # atualiza pai
    &DBE("
        update cob_tkt set
            competencia = '$competencia-01',
            descrp      = '$descrp', 
            obs         = '$obs', 
            finalizado  = $finalizado
            $encerrar
        where
            codigo = $COD
    ");
    
    # atualiza filhos
    foreach $i (@item) {
        $executado = &get('item_executado_'.$i);
        $faturado  = &get('item_faturado_'.$i);
        $descrp    = &get('item_descrp_'.$i);
        $tkt_acao  = &get('item_tkt_acao_'.$i);
        
        &DBE("
            update cob_tkt_item set 
                descrp    = '$descrp', 
                executado = '$executado', 
                faturado  = '$faturado'
            where
                codigo = $i
        ");
        
        
        # atualiza descricao externa item no ticket
        &DBE("
            update tkt_acao set 
                executor_descrp = '$descrp',
                tempo           = '$executado',
                faturado        = now()
            where
                codigo = $tkt_acao
        ");
    }

}

# finaliza SQLs
$dbh->commit;

exit;

