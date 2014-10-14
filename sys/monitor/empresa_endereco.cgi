#!/usr/bin/perl

#
# Empresa Enderecos
# 	- empresa_enderecos.cgi
#
# Chamado, lista enderecos da empresa selecionada
#

# variaveis
$nacess = "903";
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID = &get('ID');
$empresa = &get('empresa');
$endsel  = &get('end');

# Busca enderecos da empresa e atualiza lista
$DB = &DBE("select ee.*, et.descrp as tipo_descrp from empresa_endereco as ee left join tipo_endereco as et on et.codigo = ee.tipo where empresa = $empresa order by ee.tipo asc");

while($end = $DB->fetchrow_hashref) {
	$c = "$end->{tipo_descrp} - $end->{endereco}, $end->{complemento} - $end->{bairro} / $end->{cidade} - $end->{uf}";
		
	# monta array com todos os itens para adicionar no radio
	$array_radio_end .= "{val:$end->{codigo},descrp:'$c'},";
		
	# somente 1 endereco
	if($DB->rows() == 1) {
        $endsel = $end->{codigo};
	}		
}

# retorno
print<<HTML;

<script>
	\$("#cliente_endereco")
		.DTouchRadio({ 
			addItem:[$array_radio_end], 
			orientation:"vertical",
			value: "$endsel",
			click: function(x){
				sel_host();
				}
			});
HTML
if($endsel ne "")
	{
	print "sel_host();";
	}
else
	{
	print "\$('#host_container').hide();";
	}
print<<HTML;
</script>

HTML
