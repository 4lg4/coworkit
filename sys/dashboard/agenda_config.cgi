#!/usr/bin/perl

$nacess = "4";
require "../cfg/init.pl";

# Usuarios do sistema ---------------------------------------------------------------------------------------------------------
$DB = &select("select * from usuario where empresa = $USER->{empresa} order by nome asc");
while($t = $DB->fetchrow_hashref)
	{
	# monta array com todos os itens para adicionar no radio
	$usuarios .= "{val:$t->{usuario},descrp:'$t->{nome}',img:'$t->{img}'},";
	}
$usuarios = substr($usuarios, 0,-1); # remove ultima virgula

print $query->header({charset=>utf8});
print<<HTML;

<script>
	\$("#dashboard_agenda_users").DTouchRadio(
			{ 
			addItem:[$usuarios],
			visibleItems	: 10,
			DTouchRadioClick: function()
				{	
				calendarRefresh(\$("#dashboard_agenda_users").DTouchRadio("DTouchRadioGetValue"));
				
				DTouchPagesChange(\$("#DTouchPages_agenda"),"center");
				}
			});
</script>

HTML
