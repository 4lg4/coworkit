#!/usr/bin/perl

# 
# empresa_comp.cgi
# carrega hosts da empresa
#


$nacess = '903';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID = &get('ID');
$empresa = &get('empresa');
$endereco = &get('endereco');
$hostm = &get('host');

$host = "";
if($endereco ne "")
	{
	$DB = DBE("select empresa_comp.codigo, empresa_comp.nome, empresa_comp.descrp from empresa_comp where empresa_comp.endereco = '$endereco' order by empresa_comp.nome");


	if($DB->rows() > 0) { 
		# gera array
		while($a = $DB->fetchrow_hashref) {
			$host .= "{val:$a->{codigo},descrp:'<div align=left>$a->{nome}</div>'},";
			}
		}
	}
elsif($empresa ne "")
	{
	$DB = DBE("select empresa_comp.codigo, empresa_comp.nome, empresa_comp.descrp from empresa_comp where empresa_comp.empresa = '$empresa' order by empresa_comp.nome");


	if($DB->rows() > 0) { 
		# gera array
		while($a = $DB->fetchrow_hashref) {
			
			$host .= "{val:$a->{codigo},descrp:'<div align=left>$a->{nome}</div>'},";
			}
		}
	}
    
# se ja for selecionado
if($hostm ne "") {
	$marca = $hostm;
}

if($host ne "")
	{
print<<HTML;
<script>
	// \$('#host').DTouchRadio('reset','hard');
	\$('#host_container').fadeIn('fast');

	\$("#host").DTouchRadio({ 
		addItem:[$host],
		orientation:"vertical",
		uncheck : false
	});
</script>
HTML
	}
else
	{
	print "<script>\$('#host_container').hide();</script>";
	}
exit;
