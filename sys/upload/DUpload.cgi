#!/usr/bin/perl

#
#   DUpload.cgi
#       upload padrao do sistema
#

# libs
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

# cfg
$nacess = '2';

# include
require "../cfg/init.pl";

# controle de sessao
$ID = &get("ID");

# header
# print "Content-type: text/html\n\n";

# vars
$uuid      = &get("uuid");
$COD       = &get("codigo");
$download  = &get("download");
$realfield = &get("DUpload"); # pega nome real do file upload
$f         = $query->upload($realfield); # arquivo

#
#   File
#       Dados do arquivo
#
my  $file;
    $file{name}        = &get($realfield);
    $file{descrp}      = &get("DUpload_descrp");
    $file{tmpdir}      = $ldir{upload}."tmp/";
    $file{tmpname}     = $uuid;
    $file{finaldir}    = $ldir{upload}."/";
    $file{link}        =  &get("link");
    $file{link_codigo} =  &get("link_codigo");



#
#   tmp directory
#      ****** ver necessidade pois era para ajuste de erro no core do syscall
# if(! -d $file{tmpdir}) { 
#     mkdir $file{tmpdir}; 
# }
# 

#
#   Update / Delete
#
if($COD && $uuid) { # update
    # update stuff
    
} elsif($download) { # download
    $DB = &DBE("select * from arquivo where codigo = $download and empresa = $USER->{empresa}");

    if($DB->rows() == 0) {
    	print $query->header({charset=>utf8});
    	print "ERRO: Arquivo não encontrado.";
    	exit;
        
    } else { # donwload

    	$file_down = $DB->fetchrow_hashref;
    	$file_path = $ldir{upload}.''.(substr($file_down->{codigo},0,2)).'/'.$file_down->{codigo}; 

    	$file_down->{nome} =~ s/ /_/gm; # corrige nome para download
	
    	if(! -e $file_path) {
    		print $query->header({charset=>utf8});
    		print "ERRO: Arquivo não encontrado.";
    		exit;
    	}

    	# executa
    	open(FILE, "<$file_path") or die "Erro ao ler aquivo para download !!";
    	@fileholder = <FILE>;
    	close (FILE) or die "Erro ao fechar o arquivo !!";

    	print "Content-type: application/octet-stream\n"; 
    	print "Content-Disposition:attachment;filename=".$file_down->{nome}."\n\n";
    	print @fileholder;
        
        exit;
    }

} elsif($COD && !$uuid) { # delete
print "Content-type: text/html\n\n";


    $DB = &DBE("select * from arquivo where codigo = $COD");
    $A  = $DB->fetchrow_hashref;
    
    if($DB->rows > 0) {
        # verifica se usuario logado pode deletar
        if($USER->{empresa} ne $A->{empresa}){
            print '
                {
                    "type"    : "error",
                    "message" : "Voce não tem direito de deletar esse arquivo"
                }
            ';
        exit;
        }
    
        # inicia SQls execs
        $dbh->begin_work;
    
        if($A->{link}) { # remove vinculo
            &DBE("delete from ".$A->{link}."_arquivo where arquivo = ".$COD);
        }
    
        # remove arquivo 
        &DBE("delete from arquivo where codigo = ".$COD);
    
    	# remove o arquivo fisico
        if(length($COD) == 1) { # Controla os 9 primeiros registros 
            $file{finaldir} .= "0".(substr($COD,0,1)); 
        } else {
            $file{finaldir} .= substr($COD,0,2); 
        }
        
        unlink($file{finaldir}."/".$COD) or # se erro ao remover
            die
                print '
                    {
                        "type"    : "error",
                        "message" : "erro ao remover o arquivo do servidor"
                    }
                ';
        
        # finaliza SQLs
        $dbh->commit;
        
        
        # se sucesso
        print '
            {
                "type"    : "success",
                "message" : "arquivo removido com sucesso"
            }
        ';
        
        exit;
        
    } else {
        print '
            {
                "type"    : "error",
                "message" : "arquivo inexistente"
            }
        ';
        exit;
    }
        
}

# header
print "Content-type: text/html\n\n";

#
#   Upload
#       executa upload
#
open(UPLOADFILE, ">".$file{tmpdir}.$file{tmpname}) or die "$!";
binmode UPLOADFILE;
while ( <$f> ){
	print UPLOADFILE;
}
close UPLOADFILE;


#
#   file data
#       pega dados do arquivo
#
$ftmp       = $file{tmpdir}.$file{tmpname};       # junta caminho com nome do arquivo temporario
$file{type} = `/usr/bin/file -i -b $ftmp`;        # pega tipo do arquivo
$file{md5}  = `md5sum -t $fileA | cut -d" " -f1`; # pega md5
$file{size} = -s $ftmp;

#
#   Add File
#       Adiciona arquivo
#
$COD = DBE("
        insert into arquivo (
            nome, tipo, descrp, md5, 
            usuario, empresa, tamanho, link
        ) values (
            '$file{name}', 
            '$file{type}', 
            '$file{descrp}', 
            '$file{md5}', 
            $USER->{usuario},
            $USER->{empresa}, 
            $file{size},
            '$file{link}'
        )
");

# insere vinculo
&DBE("
        insert into ".$file{link}."_arquivo (
            ".$file{link}.", arquivo
        ) values (
            $file{link_codigo}, $COD
        )
");

#
#   Diretorios			
#       Cria diretorio se nao existir
#
if(length($COD) == 1) { # Controla os 9 primeiros registros 
#     $file{finaldir} = substr($COD,0,1);
    $file{finaldir} .= "0".(substr($COD,0,1)); 
} else {
    $file{finaldir} .= substr($COD,0,2); 
}

if(! -d $file{finaldir}) { # se a pasta nao existir cria
    mkdir $file{finaldir}; 
}
      
#
#   Move arquivo para local final
#
rename($file{tmpdir}."".$file{tmpname},$file{finaldir}."/".$COD)
    or die ("Erro ao mover o arquivo para pasta final !");


# retorno dados arquivo inserido
print<<HTML;
<script>
    top.eos.core.upload.done($uuid,$COD);
</script>
HTML
