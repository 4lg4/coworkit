#!/usr/bin/perl

# $nacess = "68' and usuario_menu.direito = 'a";
$nacess = "55";
require "../cfg/init.pl";
$ID        = &get('ID');

# Dados principais
$COD        = &get('COD');
$descrp     = &get('descrp');
$obs        = &get('obs');
$cob_day    = &get('cob_day');
$hora       = &get('hora');
$area       = &get('area_tipo_radios');
$cobranca   = &get('cobranca_radios');
$status     = &get('status_radios');
$empresa    = &get('empresa');
$vigencia_ini = &get('vigencia_ini');
$vigencia_fim = &get('vigencia_fim');

# normaliza variaveis para salvar no banco
if(!$vigencia_ini){
    $vigencia_ini = NULL;
} else {
    $vigencia_ini = "'".&dateToSave($vigencia_ini)."'";
}
if(!$vigencia_fim){
    $vigencia_fim = NULL;
} else {
    $vigencia_fim = "'".&dateToSave($vigencia_fim)."'";
}
if(!$hora){
    $hora = NULL;
} else {
    $hora = "".$hora."";
}
if(!$empresa){
    $empresa = NULL;
}
print $query->header({charset=>utf8});

# inicia bloco sql
$dbh->begin_work;

#
#   Statments
#
if($COD) { # update 
    # update
    DBE("
        update 
            prod_servicos
        set
            descrp       = '$descrp', 
            obs          = '$obs', 
            cobranca_dia = '$cob_day', 
            horas_plano  = $hora, 
            empresa_area_tipo = '$area',
            cobranca     = '$cobranca',
            status       = '$status',
            empresa      = $empresa,
            vigencia_ini = $vigencia_ini,
            vigencia_fim = $vigencia_fim
        where
            codigo   = $COD and
            parceiro = $USER->{empresa}
    ");
    
} else { # NEW

    # insere
    $COD = DBE("
        insert into 
            prod_servicos (
                descrp, 
                obs, 
                cobranca_dia, 
                horas_plano, 
                empresa_area_tipo, 
                cobranca,
                status,
                parceiro,
                empresa,
                vigencia_ini,
                vigencia_fim
            ) values (
                '$descrp', 
                '$obs', 
                '$cob_day', 
                '$hora', 
                '$area',
                '$cobranca',  
                '$status', 
                $USER->{empresa},
                $empresa,
                $vigencia_ini,
                $vigencia_fim
            ) 
    ");
    
    # mensagem
    #$R  = '{ ';
    #$R .= '     "status"  : "error", ';
    #$R .= '     "message" : "Verifique os campos" ';
    #$R .= '}  ';
    #print $R;

    #exit;
    
    $CODNEW = ' , "COD" : "'.$COD.'" ';
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



