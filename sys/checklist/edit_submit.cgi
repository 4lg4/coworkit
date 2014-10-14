#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "70";
require "../cfg/init.pl";
$ID        = &get('ID');

# variaveis
$COD        = &get('COD');
$TKT        = &get('TKT');
$descrp     = &get('descrp');
$dtag       = &get('dtag');

@servico     = &get_array('servico');
@usuario_ini = &get_array('usuario_ini');
@usuario_end = &get_array('usuario_end');
@hora_ini    = &get_array('hora_ini');
@hora_end    = &get_array('hora_end');
@inventario  = &get_array('inventario');


print $query->header({charset=>utf8});


# inicia SQls execs
$dbh->begin_work;


# servicos
if(@servico) {
    $c = 0;
    foreach $s (@servico) {
    
        # usuario ini
        if(!@usuario_ini[$c] || @usuario_ini[$c] eq 'undefined') {
            @usuario_ini[$c] = $USER->{usuario};
        }
        
        # usuario end
        if(!@usuario_end[$c] || @usuario_end[$c] eq 'undefined') {
            @usuario_end[$c] = NULL;
        }
        
        # hora ini
        if(!@hora_ini[$c]) {
            @hora_ini[$c] = "'".timestamp()."'";
        } else {
             @hora_ini[$c] = "'".(dateToSave(@hora_ini[$c]))."'"
        }
        
        # hora end
        if(!@hora_end[$c]) {
            @hora_end[$c] = NULL;
        } else {
             @hora_end[$c] = "'".(dateToSave(@hora_end[$c]))."'"
        }
        
        $servicos .= "(";
        $servicos .=    @usuario_ini[$c].",";
        $servicos .=    @usuario_end[$c].",";
        $servicos .=    @hora_ini[$c].",";
        $servicos .=    @hora_end[$c].",";
        $servicos .=    $s.",";
        $servicos .=    $COD;
        $servicos .= "),";
        $c += 1;
    }
    $servicos = substr($servicos, 0,-1);
        
    # remove todas as entradas antes de inserir
    &DBE("delete from checklist_acao_servico where checklist = $COD"); 

    # save	
    $email_list = substr($email_list, 0,-1); # remove ultima virgula
    &DBE("
        insert into 
            checklist_acao_servico (
                usuario_ini, 
                usuario_end,
                hora_ini,  
                hora_end,  
                servico,
                checklist
            ) values 
                $servicos
    ");
}


# inventario
if(@inventario) {
    foreach $i (@inventario) {    
        $inventarios .= "(";
        $inventarios .=    $i.",";
        $inventarios .=    $COD.",";
        $inventarios .=    $USER->{usuario};
        $inventarios .= "),";
    }
    $inventarios = substr($inventarios, 0,-1);
        
    # remove todas as entradas antes de inserir
    &DBE("delete from checklist_acao_inventario where checklist = $COD"); 

    # save	
    $email_list = substr($email_list, 0,-1); # remove ultima virgula
    &DBE("
        insert into 
            checklist_acao_inventario (
                inventario,
                checklist,
                usuario
            ) values 
                $inventarios
    ");
}

# update
DBE("
    update 
        checklist
    set
        descrp = '$descrp', 
        dtag   = '$dtag' 
    where
        codigo = $COD
");


# finaliza SQLs
$dbh->commit;


# mensagem
$R  = '{ ';
$R .= '     "status"  : "success", ';
$R .= '     "message" : "Cadastro alterado com sucesso" ';
$R .= $COD;
$R .= '}  ';
print $R;


