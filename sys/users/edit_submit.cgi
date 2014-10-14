#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "68";
require "../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD        = &get('COD');
$login      = lc(&get('login'));
$nome       = &get('nome');
$phone      = &get('phone');
$email      = lc(&get('email'));
$senha_old  = &get('senha');
$senha_new  = &get('senha_new');
$senha_conf = &get('senha_conf');

$acao       = &get('acao');

print $query->header({charset=>utf8});

if($COD && $acao eq "unlock") { # reativar cadastro
    # update
    DBE("
        update 
            usuario
        set
            bloqueado = false
        where
            usuario = $COD
    ");
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "success", ';
    $R .= '     "message" : "Usuário reativado" ';
    $R .= '}  ';
    print $R;
    exit;
    
} elsif($COD && $acao eq "lock") { # reativar cadastro
    # update
    DBE("
        update 
            usuario
        set
            bloqueado = true
        where
            usuario = $COD
    ");
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "success", ';
    $R .= '     "message" : "Usuário bloqueado" ';
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

    # alterar senha
    
    # troca de senha feita pela done
    if(($USER->{tipo} eq "1") && (($senha_new && $senha_conf) && ($senha_new eq $senha_conf)) && ($USER->{empresa} eq 1)) {
        $senha_change = " , senha = password('$senha_new') ";
        
    # troca feita pela empresa (usuario / admin) 
    } else {
    
    
        if(($senha_new && $senha_conf) && ($senha_new eq $senha_conf)) {

            # troca feita pelo proprio usuario
            if(($USER->{tipo} ne "1") && $senha_old) { 
                $senha_consulta = " and senha = password('$senha_old') ";
            } 
            # erro ao trocar a senha
            } elsif(($USER->{tipo} ne "1") && !$senha_old) {  {
                $R  = '{ ';
                $R .= '     "status"  : "error", ';
                $R .= '     "message" : "Senha antiga inválida" ';
                $R .= '}  ';
                print $R;
    
                exit;
            }
            
        } else {
            $R  = '{ ';
            $R .= '     "status"  : "error", ';
            $R .= '     "message" : "Senha nova não confere" ';
            $R .= '}  ';
            print $R;

            exit;
        }
        
        
        # consulta senha
        $DB = DBE("
            select 
                usuario, empresa
            from
                usuario
            where
                usuario = $COD 
                $senha_consulta
        ");
    
        $userconsulta = $DB->fetchrow_hashref;
    
        if($DB->rows() != 1){
            # mensagem
            $R  = '{ ';
            $R .= '     "status"  : "error", ';
            $R .= '     "message" : "Senha antiga inválida" ';
            $R .= '}  ';
            print $R;
    
            exit;
        } else {
            $senha_change = " , senha = password('$senha_new') ";
        }   
         
    }
    
    # update
    DBE("
        update 
            usuario
        set
            login = '$login', 
            nome  = '$nome', 
            email = '$email',
            phone = '$phone'
            $senha_change
        where
            usuario = $COD
    ");

    $msgtype = "update";
    
    
} else { # NEW
    
    # verifica os campos
    if(!$login || !$nome || !$email || !$senha_new || !$senha_conf) {
        # mensagem
        $R  = '{ ';
        $R .= '     "status"  : "error", ';
        $R .= '     "message" : "Verifique os campos" ';
        $R .= '}  ';
        print $R;
    
        exit;
    } elsif($senha_new ne $senha_conf) {
        # mensagem
        $R  = '{ ';
        $R .= '     "status"  : "error", ';
        $R .= '     "message" : "Senha não confere" ';
        $R .= '}  ';
        print $R;
    
        exit;
    }
    
    # verifica disponibilidade do login
    $DB = DBE("
        select 
            login
        from
            usuario
        where
            login like '$login'
    ");
    
    if($DB->rows() != 0){
        # mensagem
        $R  = '{ ';
        $R .= '     "status"  : "error", ';
        $R .= '     "message" : "Login já existente", ';
        $R .= '     "focus"   : "login" ';
        $R .= '}  ';
        print $R;
    
        exit;
    }  
    
    
    # insere
    $COD = DBE("
        insert into 
            usuario (
                login, 
                nome, 
                email, 
                empresa, 
                tipo, 
                senha
            ) values (
                '$login', 
                '$nome', 
                '$email', 
                $USER->{empresa}, 
                2, 
                password('$senha_new')
            ) 
    ");
    
    
    # insere menus
    # plano = 1 (freemium)
    $DB = DBE("
        select 
            * 
        from
            menu_plano
        where
            plano = 1
    ");
    while($m = $DB->fetchrow_hashref) {
        $mlist .= "($COD,$m->{menu},'$m->{direito}'),";
    }
    $mlist = substr($mlist, 0,-1); # remove ultima virgula

    # sql exec
    DBE("
        insert into
            usuario_menu (
                usuario,
                menu,
                direito
            ) values 
                $mlist
    ");  
    
    
    
    # retrieve the cod
    $CODNEW = ' , "COD" : "$COD" ';
    $msgtype = "new";
}



$dbh->commit;   

# mensagem
$R  = '{ ';
$R .= '     "status"  : "success", ';
$R .= '     "message" : "Cadastro alterado com sucesso" ';
$R .= $CODNEW;
$R .= '}  ';
print $R;

exit;


#
#   envio de mensagem desativado MVP 1
#


#
#   Mensagem
#       envia mensagem ao usuario quando modificado
#

# template mensagem
require "../template/users.pl";

# dados remetente para conexao com servidor de envio
@SENDER = ('NoReply', 'noreply@done.com.br', 'noreply@done.com.br', '204cacti1001');

# ajusta mensagem vinda do template
if($msgtype eq "update") {
    $USERMSG = $USERMSGUPDATE;
} else {
    $USERMSG = $USERMSGNEW;
}

# 
#   Finaliza
#
if(SENDEMAIL(\@SENDER, $email, $USERMSGTITLE{$msgtype}, $USERMSG)){ # erro desfaz tudo
	$dbh->rollback; # desfaz alteracoes do banco
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "error", ';
    $R .= '     "message" : "Erro ao enviar o email" ';
    $R .= '}  ';
    print $R;
    
    exit;
    
} else { # sucesso 
    
    # end bloco sql
    $dbh->commit;   
    
    # mensagem
    $R  = '{ ';
    $R .= '     "status"  : "success", ';
    $R .= '     "message" : "Cadastro alterado com sucesso" ';
    $R .= $CODNEW;
    $R .= '}  ';
    print $R;
    
}


