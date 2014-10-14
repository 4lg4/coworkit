#!/usr/bin/perl

#
# chamado.cgi
#
# Lista de chamados que aparecem no modulo
#

$nacess = "2";
# $nacess_more = "or menu = 74";
require "../cfg/init.pl";

$ID = &get('ID');

$tkt       = &get('feedback_tkt');
$tipo      = &get('feedback_tipo');
$avaliacao = &get('feedback_avaliacao');

# dados para finalizar feedback
$tipo1     = &get('feedback_tipo1');
$tipo2     = &get('feedback_tipo2');
$tipo3     = &get('feedback_tipo3');
$descrp    = &get('feedback_descrp');

print $query->header({charset=>utf8});

# inicia SQls execs
$dbh->begin_work;

# somente avaliacao
if($avaliacao eq "OLD NAO uSAR") {
    # deleta avaliacao
    DBE("
        delete from 
            tkt_feedback
        where 
            tkt  = $tkt and
            tipo = $tipo
    ");


    # deleta avaliacao
    DBE("
        insert into
            tkt_feedback (
                usuario,
                tipo,
                avaliacao,
                tkt
            ) values (
                $USER->{usuario},
                $tipo,
                $avaliacao,
                $tkt
            )
    ");

# finaliza feedback
} else {
    # insere avaliacao
    DBE("
        insert into
            tkt_feedback (
                usuario,
                tipo,
                avaliacao,
                tkt
            ) 
            values 
                ( $USER->{usuario}, 1, $tipo1, $tkt ),
                ( $USER->{usuario}, 2, $tipo2, $tkt ),
                ( $USER->{usuario}, 3, $tipo3, $tkt )
    ");
    
    # atualiza ticket
    DBE("
        update
            tkt
        set
           feedback = now(),
           feedback_descrp = '$descrp'
        where
            codigo = $tkt
    ");

    # atualiza tela
    print "
        <script>
            dashboard.widget.feedback.load();
        </script>
    ";
}






# finaliza SQLs
$dbh->commit;

