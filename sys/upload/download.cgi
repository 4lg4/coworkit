#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;

$nacess = '';
require "../cfg/init.pl";

$COD=&get('MD5');
	
# recupera dados do arquivo ---------------------------------------------------
$DB =&DBE("select * from arquivo where md5='".$COD."'");

# Verifica se o arquivo existe.
if($anexo = $DB->rows()==0)
	{
	print $query->header({charset=>utf8});
	print "ERRO: Arquivo não encontrado.";
	exit;
	}
else
	{
	

	$anexo = $DB->fetchrow_hashref;

	$DEL_DIR = substr($anexo->{codigo},0,2);
	$fileA = $dirUpload.''.$DEL_DIR.'/'.$anexo->{codigo}; 

	# print $query->header({charset=>utf8});
	# print "Aqui -->>> ".$fileA." - ".$anexo->{nome}; # debug --
	# exit;
	$anexo->{nome} =~ s/ /_/gm;
	
	if(! -e $fileA)
		{
		print $query->header({charset=>utf8});
		print "ERRO: Arquivo não encontrado.";
		exit;
		}

	# Ajusta e faz download do arquivo --------------------------------------------		
	open(FILE, "<$fileA") or die "Erro ao ler aquivo para download !!";
	@fileholder = <FILE>;
	close (FILE) or die "Erro ao fechar o arquivo !!";

	print "Content-type: application/octet-stream\n"; 
	print "Content-Disposition:attachment;filename=".$anexo->{nome}."\n\n";
	print @fileholder;
	}
	
	