#!/usr/bin/perl

$nacess = "207";
require "../cfg/init.pl";

$COD = &get('codigo');

print $query->header({charset=>utf8});


# carrega valores do banco de dados
$n=0;
require "./edit_db.pl";


print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	</head>
<body>
<div style="border: solid 1px black; background-color: white; margin: 20px; padding: 20px;">
	<table width="100%" border=0>
		<tr>
			<td>
			<img src="../../img/logos/1.png" width=170 height=60>
			</td>
			<td>
HTML
if($empresa ne "")
	{
print<<HTML;	
			<b>Empresa: </b>$empresa<br>
			<b>Endere&ccedilo: </b>$endereco
HTML
	}
print<<HTML;
			</td>
		</tr>
	</table>
	<br>
	<table style="width:95% !important; margin:20px;" border=0>
		<tr>
			<td>
			<center><font size="20">Procedimento</font></center>
			</td>
		</tr>
		<tr>
			<td>
			<br>
			<b>Título: </b>$titulo
			</td>
		</tr>
HTML
if($tags_wlist ne "")
	{
print<<HTML;
		<tr>
			<td>
			<b>TAGs: </b>$tags_wlist
			</td>
		</tr>
HTML
	}
print<<HTML;
		<tr>
			<td>
			<hr size=1></hr>
			</td>
		</tr>
		<tr>
			<td>
			<div id='txt'>$procedimento</div>
			</td>
		</tr>
HTML
if($n>0)
	{
print<<HTML;
		<tr>
			<td>
			<br><br><hr size=1></hr><br>$n Arquivos anexados:
			</td>
		</tr>
HTML
	for($f=0; $f<$n; $f++)
		{
print<<HTML;
		<tr>
			<td>
				$arq_nome[$f] 
			</td>
		</tr>
HTML
		}
	}
print<<HTML;
	</table>
</div><br><br>
</body>
</html>
HTML

exit;

