#!/usr/bin/perl

$nacess = "nocheck";
require "../../cfg/init.pl";

# Resolve problema de carregamento de dados de TI no iframe
# Limpa as os campos COD e MODO

print $query->header({charset=>utf8});
print "<body onLoad='top.unLoading();'><form action='edit.cgi' method='post'>\n";
@campo = $query->param();
for($f=0;$f< scalar(@campo);$f++)
	{
	if($campo[$f] ne "COD" && $campo[$f] ne "MODO" && $campo[$f] ne "THIS")
		{
		print "<input type='hidden' name='".$campo[$f]."' value='".&get($campo[$f])."'>\n";
		}
	}
print "<input type='submit'>";
print "</form></body>\n";


