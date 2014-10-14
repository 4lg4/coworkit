#!/usr/bin/perl

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use File::Basename;
use GD;
use Image::Magick;

$nacess ='';
require "../cfg/init.pl"; #ou ../cfg/init.pl
$MD5 = &get('md5');
$MD5 =~ s/\n//gm;
$MD5 =~ s/\r//gm;
$MD5 =~ s/^\s+//; # ltrim
$MD5 =~ s/\s+$//; # rtrim

$x_img = &get('x');
$y_img = &get('y');
$w_img = &get('w');
$h_img = &get('h');

print $query->header({charset=>utf8});

#[INI]/////////////////////////////////////////////////////////  Lembretes  ///////////////////////////////////////////////////////////////////#

# SELECT --> $DB1 = &DBE("select * from tabela where tabela is null order by campo");
# DELETE --> $DB2 = &DBE("delete from tabela where coluna='identificao'");
# INSERT --> $DB3 = &DBE("insert into tabela (campo1,campo2...) values ('".$variavel."') ");

#-------------------------------------------------------------------- While -------------------------------------------------------------------#

# while($row_title = $DB->fetchrow_hashref)
# 	{
# 	$modulos .="<li><a href='#t-$i'>$row_title->{'descrp'}</a></li>";
# 	$i++;
# 	}

#-------------------------------------------------------------------  FOR  --------------------------------------------------------------------#

#for($g=0; $g<$ncol; $g++)
# {
# $menu[$g] .= "<div class='menu menu_".$row->{'codigo'}."'>";
# }

#-----------------------------------------------  Pega o primeiro o id após inserção ou atualização -------------------------------------------#

# $codigo=$tipo_usuario->fetch;
# $DB4 = &DBE("update tabela set descrp='".ucfirstall($tipo_descrp)."' where codigo='@$codigo[0]'  ");

#--------------------------------------------  Recupera o ultida id cadastrado, somente após inserção  ----------------------------------------#

#[FIM]/////////////////////////////////////////////////////////  Lembretes  ///////////////////////////////////////////////////////////////////#

#Pega o arquivo do banco
$DB = &DBE("select * from arquivo where md5 = '".$MD5."'");
$file = $DB->fetchrow_hashref;

# monta path do arquivo ----------------------------------
if(length($file->{codigo}) == 1) # Controla os 9 primeiros registros
	{
	$DEL_DIR = substr($file->{codigo},0,1);
	$DEL_DIR .= 0;
	}
else
	{ $DEL_DIR = substr($file->{codigo},0,2); }
$fileA = $dirUpload.''.$DEL_DIR.'/'.$file->{codigo};


# $myImage = $fileA;
# $srcImage = new GD::Image($myImage);
# ($srcW,$srcH) = $srcImage->getBounds();
# $destImage = new GD::Image(95,100);
# $destImage->copyResized($srcImage,0,0,95,100,$x1,$y1,$x2,$y2);
# 
# $ImageLocation = $fileA;
# open IMG,">$ImageLocation" or die "$ImageLocation $!";
# binmode(IMG);
# print IMG $destImage->jpeg;
# close IMG;
$image = Image::Magick->new();
$x = $image->Read($fileA);
warn "$x" if "$x";

$x = $image->Crop(geometry=>"$w_img x $h_img+$x_img+$y_img");
warn "$x" if "$x";

$x = $image->Resize(width=> "95", height=>"100");
warn "$x" if "$x";

$x = $image->Write($fileA);
warn "$x" if "$x";


# print "<script> location.reload(true); </script>";

#[FIM]//////////////////////////////////////////////////////  Exemplo de lista  ///////////////////////////////////////////////////////////////#