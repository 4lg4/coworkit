#!/usr/bin/perl

$nacess = "201";
require "../cfg/init.pl";

$COD    = &get('COD');

# [INI] -------------------------------------------------------------------------------------------------------------------
#	 top empresas, grid
# -------------------------------------------------------------------------------------------------------------------------
if($COD ne "") {
	$DB = DBE("select * from last_view where tabela = 'empresa' and usuario = $USER->{usuario} and codigo = $COD ");
	if($DB->rows > 0) {
		DBE("update last_view set dt=now() where tabela = 'empresa' and usuario = $USER->{usuario} and codigo = $COD ");
	} else {
		DBE("insert into last_view (tabela, usuario, codigo) values ('empresa', $USER->{usuario}, $COD) ");
	}
}
# [END] top empresas, grid ------------------------------------------------------------------------------------------------

# [INI] -------------------------------------------------------------------------------------------------------------------
#	 tipo de empresa
# -------------------------------------------------------------------------------------------------------------------------
$DB = DBE("select * from empresa_tipo order by descrp");

if($DB->rows() < 1)
	{
	$tipo_emp_list .= "Nenhum tipo de cadastrado";
	}
else
	{
	while($r = $DB->fetchrow_hashref)
		{
		$tipo_emp_list .= "<input type='radio' name='tipo_emp' value='$r->{'codigo'}'>";
		$tipo_emp_list .= "$r->{'descrp'}";
		}
	}
# [END] tipo de empresa ---------------------------------------------------------------------------------------------------

# [INI] -------------------------------------------------------------------------------------------------------------------
#	 grupos disponiveis e da empresa
# -------------------------------------------------------------------------------------------------------------------------
if($COD ne "") {
    
	# monta grupos participantes
	$DB = &DBE("
        select 
            tr.*
        from 
            empresa_relacionamento as er 
        left join 
            tipo_relacionamento as tr on tr.codigo = er.relacionamento 
        where 
            er.empresa = $COD
    ");
    
	while($gp = $DB->fetchrow_hashref) {
		$grupos_participantes .= "<li><input type='hidden' name='grupos_participantes' value='$gp->{codigo}'>".ucfirstall($gp->{descrp})."</li>";
	}
		
	$SQL_existentes = "
        select 
            tr.* 
        from 
            tipo_relacionamento as tr 
        where 
            not exists (
                select
                    * 
                from 
                    empresa_relacionamento as er 
                where 
                    er.empresa = $COD and tr.codigo = er.relacionamento
            ) and 
            tr.parceiro = $USER->{empresa}
    ";
    
} else {
    
	$SQL_existentes ="select tr.* from tipo_relacionamento as tr where tr.parceiro = $USER->{empresa}";
}
	
# monta grupos existentes
$DB = &DBE($SQL_existentes);
while($gp = $DB->fetchrow_hashref) {
	$grupos_existentes .= "<li><input type='hidden' name='grupos_existentes' value='$gp->{codigo}'>".ucfirstall($gp->{descrp})."</li>";
}

# gera listas
$grupos_participantes = "<ul id='grupos_participantes_ul' class='grupos_connect'>".$grupos_participantes."</ul>";
$grupos_existentes    = "<ul id='grupos_existentes_ul' class='grupos_connect'>".$grupos_existentes."</ul>";
# [END] grupos disponiveis e da empresa -----------------------------------------------------------------------------------

# [INI] -------------------------------------------------------------------------------------------------------------------
#	 tecnicos disponiveis e da empresa
# -------------------------------------------------------------------------------------------------------------------------
if($COD ne "") {
	# monta tecnicos participantes
	$DB = &DBE("
        select 
            et.*, 
            u.nome as descrp, 
            u.usuario as usuario 
        from 
            empresa_tecnico as et 
        left join 
            usuario as u on et.usuario = u.usuario 
        where 
            et.empresa = $COD
    ");
    
	while($gp = $DB->fetchrow_hashref) {
		$tecnicos_participantes .= "<li><input type='hidden' name='tecnicos_participantes' value='$gp->{usuario}'>".ucfirstall($gp->{descrp})."</li>";
	}
		
	$SQL_existentes ="select u.usuario, u.usuario as usuario, u.nome as descrp from usuario as u where not exists (select * from empresa_tecnico as et where et.empresa = $COD and u.usuario = et.usuario) and empresa = $USER->{empresa}";
    
} else {
    
	$SQL_existentes ="select usuario, nome as descrp from usuario where empresa = $USER->{empresa}";
}
	
# monta tecnicos existentes
$DB = &DBE($SQL_existentes);
while($gp = $DB->fetchrow_hashref) {
	$tecnicos_existentes .= "<li><input type='hidden' name='tecnicos_existentes' value='$gp->{usuario}'>".ucfirstall($gp->{descrp})."</li>";
}

# gera listas
$tecnicos_participantes = "<ul id='tecnicos_participantes_ul' class='tecnicos_connect'>".$tecnicos_participantes."</ul>";
$tecnicos_existentes    = "<ul id='tecnicos_existentes_ul' class='tecnicos_connect'>".$tecnicos_existentes."</ul>";
# [END] tecnicos disponiveis e da empresa -----------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 planos disponiveis e da empresa
# -------------------------------------------------------------------------------------------------------------------------
    
if($COD ne "") {    
	# monta planos participantes
	$DB = &DBE("
        select
            ps.descrp as descrp,
            ps.vigencia_ini,
            ps.vigencia_fim,
            at.img as area_img,
            at.descrp as area 
        from 
            prod_servicos as ps
        left join
            empresa_area_tipo as at on at.codigo = ps.empresa_area_tipo
        where 
            ps.empresa = $COD
    ");
    
	while($gp = $DB->fetchrow_hashref) {
        $vigencia = "(Indeterminado)";
        if($gp->{vigencia_ini}) {
            $vigencia = " (".dateToShow($gp->{vigencia_ini},"date")." - ".dateToShow($gp->{vigencia_fim},"date").")";
        }
		$planos_participantes .= "<li><input type='hidden' name='planos_participantes' value='$gp->{prod_servicos}'>$gp->{area} - ".ucfirstall($gp->{descrp})." $vigencia</li>";
	}
} else {
    $planos_participantes .= "<li>Nenhum</li>";
} 
# gera listas
$planos_participantes = "<ul id='planos_participantes_ul' class='planos_connect'>".$planos_participantes."</ul>";
# $planos_existentes    = "<ul id='planos_existentes_ul' class='planos_connect'>".$planos_existentes."</ul>";
# [END] planos disponiveis e da empresa -----------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Dados da empresa
# -------------------------------------------------------------------------------------------------------------------------
if($COD ne "")
	{
	$DB = DBE("select * from empresa where codigo = $COD");

	if($DB->rows() < 1)
		{
		$empresa .= "Erro Empresa Não existente";
		}
	else
		{
		$empresa = $DB->fetchrow_hashref;
	
		# ajusta variaveis
		$empresa->{obs} = &get($empresa->{obs},"NEWLINE_SHOW");
		}
	}
else
	{
	$empresa->{ativo} = "true"; # seta empresa ativo para verdadeiro se for novo cadastro
	# $empresa->{tipo} = "J"; # seta tipo empresa para juridica se for novo cadastro
	}
# [END] Dados de empresa --------------------------------------------------------------------------------------------------


# [INI] -------------------------------------------------------------------------------------------------------------------
#	 Bancos, dados bancarios
# -------------------------------------------------------------------------------------------------------------------------
if($COD) {
    
    $DB = &DBE("
        select 
            eb.*, b.descrp as banco_descrp, b.codigo as banco_codigo  
        from 
            empresa_banco as eb join bancos as b on eb.banco = b.codigo 
        where 
            eb.empresa = '$COD'
    ");
    
    if($DB->rows() > 0) {
    	while($banco= $DB->fetchrow_hashref) {
    		$lista_bancos .= "{";
    		$lista_bancos .= "val:$banco->{codigo},";
    		$lista_bancos .= "descrp:\"";
    		#$lista_bancos .= "$banco->{obs}\"},";
	
    		$lista_bancos .= "<div><input type='hidden' value='$banco->{banco_codigo}' name='banco_codigo_'> <span>$banco->{banco_descrp}</span></div>";
    		$lista_bancos .= "<div><input type='hidden' value='$banco->{agencia}' name='banco_agencia_'> ag. <span>$banco->{agencia}</span></div>";
    		$lista_bancos .= "<div><input type='hidden' value='$banco->{conta}' name='banco_conta_'> c/c. <span>$banco->{conta}</span></div>";
    		$lista_bancos .= "<div><input type='hidden' value='$banco->{obs}' name='banco_obs_'> <span>$banco->{obs}</span></div>";
    		$lista_bancos .= "\"},";
    	}
		
    	$lista_bancos = substr($lista_bancos, 0,-1); # remove ultima virgula
        $lista_bancos = "addItem:[".$lista_bancos."],";
    } 
} 
# [END] Bancos, dados bancarios -------------------------------------------------------------------------------------------


#
#   Arquivos anexos
#
if($COD) {    
    $DB = &DBE("select ea.*, a.* from empresa_arquivo as ea join arquivo as a on a.codigo = ea.arquivo where ea.empresa = $COD");
	while($arquivo = $DB->fetchrow_hashref) {
		$lista_arquivo .= "{";
		$lista_arquivo .= "codigo : $arquivo->{codigo},";
		$lista_arquivo .= "descrp : '$arquivo->{descrp}',";
        $lista_arquivo .= "type   : '".(&get($arquivo->{tipo},"NEWLINE_SHOW"))."',";
        $lista_arquivo .= "size   : '$arquivo->{tamanho}'";
		$lista_arquivo .= "},";
	}



#
#   Avatar
#
# if($avatar) { 
    $DB = &DBE("select * from empresa_avatar_arquivo where empresa_avatar = $COD order by arquivo desc limit 1");
    $a = $DB->fetchrow_hashref;
	$codigo_avatar = $a->{arquivo};
    # }
    
    
    
    #
    #   Service Desk
    #    
    $DB = DBE("
        select 
            * 
        from
            usuario
        where
            empresa = $COD
        order by
            usuario asc
        limit 1
    ");
    if($DB->rows() > 0) {
        $tkt = $DB->fetchrow_hashref;
        if($tkt->{bloqueado} == 1) {
            $tkt->{bloqueado} = "true";
        } else {
            $tkt->{bloqueado} = "false";
        }
    }
}

print $query->header({charset=>utf8});

print<<HTML;

<script>
	//	grupos inicia listas
	\$("#DVgrupo_showlist_exis").html("$grupos_existentes");
	\$("#DVgrupo_showlist").html("$grupos_participantes");
	\$("#grupos_participantes_ul, #grupos_existentes_ul").sortable(
		{
		connectWith: ".grupos_connect",
		// forcePlaceholderSize: true,
		dropOnEmpty: true,
		receive: function(event, ui) 
			{			
			// se vier de grupos existentes para grupos participantes
			if(ui.sender.prop("id") == "grupos_existentes_ul")
				{
				ui.item.find("input[type=hidden]").prop("name", "grupos_participantes");
				}
			// se vier de grupos participantes para grupos existentes
			else
				{
				ui.item.find("input[type=hidden]").prop("name", "grupos_existentes");
				}
			}
		})
		.disableSelection();
		
	//	tecnicos inicia listas
	\$("#tecnicos_list_exis").html("$tecnicos_existentes");
	\$("#tecnicos_list").html("$tecnicos_participantes");
	\$("#tecnicos_participantes_ul, #tecnicos_existentes_ul").sortable(
		{
		connectWith: ".tecnicos_connect",
		dropOnEmpty: true,
		receive: function(event, ui) 
			{			
			// se vier de tecnicos existentes para tecnicos participantes
			if(ui.sender.prop("id") == "tecnicos_existentes_ul")
				{
				ui.item.find("input[type=hidden]").prop("name", "tecnicos_participantes");
				}
			// se vier de tecnicos participantes para tecnicos existentes
			else
				{
				ui.item.find("input[type=hidden]").prop("name", "tecnicos_existentes");
				}
			}
		})
		.disableSelection();
		
	//	planos inicia listas
    \$("#planos_list").html("$planos_participantes");
	\$("#planos_list_exis").hide();
    /*
	\$("#planos_list_exis").html("$planos_existentes");
	\$("#planos_participantes_ul, #planos_existentes_ul").sortable(
		{
		connectWith: ".planos_connect",
		dropOnEmpty: true,
		receive: function(event, ui) 
			{			
			// se vier de planos existentes para planos participantes
			if(ui.sender.prop("id") == "planos_existentes_ul")
				{
				ui.item.find("input[type=hidden]").prop("name", "planos_participantes");
				}
			// se vier de planos participantes para planos existentes
			else
				{
				ui.item.find("input[type=hidden]").prop("name", "planos_existentes");
				}
			}
		})
		.disableSelection();
    */
	
	// bancos
	\$("#bancos_list").DTouchRadio({ 
            $lista_bancos
			orientation: 'vertical',
			DTouchRadioClick: function() {
				// junta todos inputs da linha
				var linha = \$("input:radio[name='bancos_list_radios']:checked").next().find('input[type=hidden]');
				
				// navega entre os inputs da linha
				linha.each(function()
					{
					if(\$(this).prop('name') == 'banco_codigo_')
						\$("#"+\$(this).prop('name')+"form_descrp").val(\$(this).parent().text());
						
					\$("#"+\$(this).prop('name')+"form").val(\$(this).val());
					});
				
				// mostra icone update
				\$("#banco_icon_update").show();
			},
			DTouchRadioUncheck: function(){
				// limpa formulario
				\$("#bancos_title input").val("");
				
				// esconde icone update
				\$("#banco_icon_update").hide();
			}
		});
		
	// tipo empresa radio J / F
	\$("#tipo_emp_container").html("$tipo_emp_list");
	\$("input[name=tipo_emp]").change(function()
		{ 
		DActionAjax("tipo_emp_change.cgi","tipo_emp="+\$(this).val(),"top_tabs");
		});
		
	// ajustes se o codigo ja estiver preenchido
	if("$COD" != "") {
		// tipo da empresa
		DActionAjax("tipo_emp_change.cgi","tipo_emp=$empresa->{tipo}","top_tabs");		
	}
		
		
		
	// popula formulario se for edicao
	\$("#nome").val("$empresa->{nome}");
	\$("#apelido").val("$empresa->{apelido}");
	\$("#obs").val("$empresa->{obs}");		
	\$("#ativo").prop("checked", $empresa->{ativo});
	
	\$("input[name=tipo_emp]:radio[value=$empresa->{tipo}]").prop("checked", true);
    
    
    // service desk
    \$("#tkt_usuario").val("$tkt->{usuario}");
    \$("#tkt_login_confirm").val("$tkt->{login}");
    \$("#tkt_login").val("$tkt->{login}");
    \$("#tkt_password").val("true");
    \$("input[name=tkt_open]:radio[value=$tkt->{bloqueado}]").prop("checked", true);
    
    
    // popula uploads
    empresa.upload.addDb([$lista_arquivo]);
    empresa.avatar.show($codigo_avatar);
    
</script>

HTML

exit;
