#!/usr/bin/perl

$nacess = "2";
require "../cfg/init.pl";

# ajusta data para filtro dos totais de horas
$filter_date = timestamp("month").'/'.timestamp("year"); # gera dia inicial;

# Usuarios do sistema ---------------------------------------------------------------------------------------------------------
$DB = &select("select * from usuario where empresa = $USER->{empresa} order by nome asc");
while($t = $DB->fetchrow_hashref)
	{
	$t->{img}="/sys/cfg/DPAC/view_avatar.cgi?MD5=".$t->{img};
	# monta array com todos os itens para adicionar no radio
	$usuarios .= "{val:$t->{usuario},descrp:'$t->{nome}',img:'$t->{img}'},";
	
	}
$usuarios = substr($usuarios, 0,-1); # remove ultima virgula

print $query->header({charset=>utf8});
print<<HTML;

<script>
	\$("#dashboard_users").DTouchRadio(
			{ 
			addItem:[$usuarios],
			visibleItems	: 3,
			DTouchRadioClick: function()
				{	
				// seta variavel para abertura de chamado com usuario predefinido		
				var variaveis =
					{
					TECNICO : \$("#dashboard_users").DTouchRadio("DTouchRadioGetValue"),
					MODO:	"incluir"
					};
			
				call('chamado/edit.cgi',variaveis);
				}
			});
			
	\$("#dashboard_filter_date").val("$filter_date");
</script>

HTML
