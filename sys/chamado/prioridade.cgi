#!/usr/bin/perl
 
# 
# area.cgi
# carrega areas da empresa baseado nos planos do cliente
#

$nacess = '10';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID = &get('ID');
$empresa = &get('empresa');
$planom = &get('plano');




# Areas Empresa  ----------------------------------------------------------------------------------
# $DB = DBE("select ea.area as codigo, eat.descrp, eat.img from empresa_area as ea left join empresa_area_tipo as eat on eat.codigo = ea.area where ea.empresa = 1 order by eat.descrp");
$DB = DBE("select DISTINCT(eat.codigo), eat.descrp, eat.img from empresa_prod_servicos as ep left join prod_servicos as ps on ps.codigo = ep.prod_servicos  left join empresa_area_tipo as eat on eat.codigo = ps.empresa_area_tipo where ep.empresa = $empresa and eat.codigo is not null");
while($a = $DB->fetchrow_hashref)
	{
	# $a->{img}="/sys/cfg/DPAC/view_avatar.cgi?MD5=".$a->{img};
	# monta array com todos os itens para adicionar no radio
	# $area .= "{val:$a->{codigo},descrp:'$a->{descrp}',img:'$a->{img}'},";
	$area .= "{val:$a->{codigo},descrp:'$a->{descrp}',img:'/img/chamado/$a->{img}'},";
	}

print<<HTML;
<script>
	// \$('#area').DTouchRadio('reset','hard');
	\$('#area_container').fadeIn('fast');

	\$("#area").DTouchRadio(
		{ 
		addItem:[$area],
		value: '$area_unico',
		// click: function(x){ empresaFilterPlans2($empresa,x.value); }
		});
</script>
HTML
exit;
# debug($planom);

# Planos de Atendimento --------------------------------------------------------------------------------------
$DB = DBE("select ps.codigo, ps.descrp from empresa_prod_servicos as eps left join prod_servicos as ps on ps.codigo = eps.prod_servicos where eps.empresa = $empresa order by ps.descrp");
while($p = $DB->fetchrow_hashref)
	{
	$plano .= "{val:$p->{codigo},descrp:'$p->{descrp}'},";
	
	# se existir somente um plano
	if($DB->rows() == 1)
		{
		$marca = $p->{codigo};
		}
	}
	
# se nao existir registros
if($DB->rows() == 0)
	{
	print "<script>	
				\$('#plano').DTouchRadio('reset','hard');
				\$('#plano_container').fadeOut('fast');
			</script>";
	exit;
	}
	
# se plano vier preenchido
if($planom ne "")
	{
	$marca = $planom;
	}

# debug($planom);
# debug($marca);

print<<HTML;
<script>
	\$('#plano_container').DTouchBoxes("show");
	
	\$("#plano").DTouchRadio({ 
		orientation:"vertical", 
		addItem:[$plano],
		value: '$marca'
	});
        
    \$("#plano").DTouchRadio("disable");
</script>
HTML

exit;
