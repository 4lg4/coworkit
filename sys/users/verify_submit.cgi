#!/usr/bin/perl

$nacess = "2"; # nacess do dashboard para nenhum usuario ficar sem acesso
require "../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD      = &get('verify_codigo');
$solicita = &get('solicita');

print $query->header({charset=>utf8});


if($solicita) {
    $DB = DBE("
        select 
            password(usuario::text || login::text) as codigo_ativ,
            login,
            email
        from
            usuario
        where
            usuario = $USER->{usuario} and
            empresa = $USER->{empresa}
    ");

    # hash com resultados
    $r = $DB->fetchrow_hashref;

    # envia email
    $email = $r->{login};
    if($r->{email}) {
        $email .= ",".$r->{email};
    }
    @SENDER = ('NoReply');
    $result = SENDEMAIL(\@SENDER, $email, "Código de ativação", $r->{codigo_ativ});
    
    if($DB->rows() == 1 && !$result){
        $R  = '{ ';
        $R .= '     "status"  : "success", ';
        $R .= '     "message" : "Mensagem enviada para email (<b>'.$r->{login}.' / '.$r->{email}.'</b>) " ';
        $R .= '}  ';
        print $R;
    } else {
        $R  = '{ ';
        $R .= '     "status"  : "error", ';
        $R .= '     "message" : "Erro Desconhecido" ';
        $R .= '}  ';
        print $R;
    }
    exit;
}


# inicia transacao
$dbh->begin_work;


$DB = DBE("
    select 
        usuario
    from
        usuario
    where
        password(usuario::text || login::text) like '$COD' and
        usuario = $USER->{usuario} and
        empresa = $USER->{empresa}
");

if($DB->rows() == 1){
    
    # update
    DBE("
        update 
            usuario
        set
            verified = now()
        where
            usuario = $USER->{usuario} and
            empresa = $USER->{empresa}
    ");
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "success", ';
    $R .= '     "message" : "Usuário válido" ';
    $R .= '}  ';
    print $R;
    
} else {
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "error", ';
    $R .= '     "message" : "Código inválido! <br><br> solicite outro código" ';
    $R .= '}  ';
    print $R;
    exit;
}

# end bloco sql
$dbh->commit;  
