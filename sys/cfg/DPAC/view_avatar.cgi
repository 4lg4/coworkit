#!/usr/bin/perl

use Digest::MD5 qw(md5_hex);
require "../../cfg/init.pl";

# vars
$nacess  = "";
$ID      = &get('ID');
$COD     = &get('COD');
$EMP     = &get('EMP');
$USERCOD = &get('USER');
$md5     = &get('MD5');

# arquivo do banco
if($md5 eq "") {
    if($USERCOD && $ID) {
        $DB = &DBE("select a.codigo as codigo, a.nome as nome from usuario_arquivo as ua left join arquivo as a on a.codigo = ua.arquivo where ua.usuario = $USERCOD");
    } elsif($COD && $ID) {
        $DB = &DBE("select codigo, nome from arquivo where codigo = $COD and empresa = $USER->{empresa}");
    } elsif($EMP && $ID) { 
        # se parceiro e nao DONE
        if($EMP eq $USER->{empresa} && $USER->{empresa_cad} && $USER->{empresa_cad} ne "1") {
            $EMP = $USER->{empresa_cad};
        }
        $DB = &DBE("select arquivo as codigo from empresa_avatar_arquivo where empresa_avatar = $EMP order by codigo desc limit 1");
    } else {
        # $DB = &DBE("select * from arquivo where nome = 'default_man.png'");
        $file_name = "default_man.png";
        $file_path = $ldir{'img'}."usuario/";
    }	
} else {
	$DB = &DBE("select * from arquivo where md5 = '".$md5."'");
}

# print default image for avatar
if($file_path) {
    # abre o arquivo
    open(FILE, "<".$file_path.$file_name) or die 
        "Erro ao ler aquivo para download $file_path.$file_name !!";

    @fileholder = <FILE>;

    # fecha o arquivo
    close (FILE) or die 
        "Erro ao fechar o arquivo !!";

    # mostra o arquivo
    print " Cache-Control:no-cache 
            Content-type:application/octet-stream 
            Content-Disposition:attachment;filename=".$file_name."\n\n";
    
    print @fileholder;
    
    exit;
}


# print from db
$file = $DB->fetchrow_hashref;

# monta path do arquivo 
if(length($file->{codigo}) == 1) {
	$DEL_DIR = substr($file->{codigo},0,1);
	$DEL_DIR .= 0;
} else {
	$DEL_DIR = substr($file->{codigo},0,2);
}	
$file_ = $dirUpload.''.$DEL_DIR.'/'.$file->{codigo};


# Verificar se o arquivo existe
if(! -e $file_) {
	$file_ = $dirUpload.'13/13';
}
	
# abre o arquivo
open(FILE, "<$file_") or die 
    "Erro ao ler aquivo para download $file_ !!";

@fileholder = <FILE>;

# fecha o arquivo
close (FILE) or die 
    "Erro ao fechar o arquivo !!";

# mostra o arquivo
print " Cache-Control:no-cache 
        Content-type:application/octet-stream 
        Content-Disposition:attachment;filename=".$file->{nome}."\n\n";
    
print @fileholder;	

