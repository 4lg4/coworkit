#!/usr/bin/perl
 
# 
# end_change.cgi
# carrega tabs com enderecos
#

$nacess = '201';
require "../cfg/init.pl";

$COD = &get('COD');
$add = &get('add');

print $query->header({charset=>utf8});

## lista todas opcoes do primeiro select
## $("#end_tabs .tipo_end:first option")

# [INI] -------------------------------------------------------------------------------------------------------------------
# 	modelo de formulario de endereco
# -------------------------------------------------------------------------------------------------------------------------
sub geraModelo
	{ my ($id) = @_;	
	
my $modelo=<<HTML;
<div id='end_tabs_$id' class='empresa_endereco_container_master'> 
	
		<div id='SEPARA_CONTEUDO_DAS_ABAS'>

			<div class='btns'>
				<div class='btn_dados aba_vertical_active'>
				  d <br> a  <br> d <br> o <br> s
				</div>
				<div class='btn_mapa aba_vertical_inactive'>
				  m <br> a <br> p <br> a
				</div>
			</div>


			<div class='empresa_endereco_container'>
		  		<div id='aba_dados_$id' class='aba_dados'>
			
					<!-- Endereco, campos -->
					<div class='empresa_endereco_dados'>
					<table>
						<tr>
							<td class='form'>Endereço</td>
							<td colspan=5 class='empresa_endereco_dados_endereco'>
								<input type='hidden' name='endereco_codigo' value='n$id'>
								<input type='text' name='endereco'>
							</td>
						</tr>
						<tr>
							<td width='7%' class='form'>Complemento</td>
							<td width='26%'><input type='text' name='complemento' maxlength=250></td>
							<td width='7%' class='form'>Bairro</td>
							<td width='26%'><input type='text' name='bairro' maxlength=200></td>
							<td width='7%' class='form'>Cidade</td>
							<td width='26%'><input type='text' name='cidade' maxlength=250></td>
						</tr>
						<tr>
							<td class='form'>CEP</td>
							<td><input type='text' name='cep' maxlength=50></td>							
							<td class='form'>Estado</td>
							<td><select name='uf'></select></td>
							<td class='form'>País</td>
							<td><select name='pais'></select></td>
						</tr>
					</table>
				</div>
			
				<!-- Observacoes, campo -->
				<div class='empresa_endereco_obs'>
					<textarea name='problemas'></textarea>
				</div>

				<!-- Contatos clientes -->
				<div class='endereco_contatos'></div>	


				<!-- Mapa  -->  
		    	<div id='aba_mapa$id' class='aba_mapa'>
					<div id='mapa_google$id' class='mapa_google' style='position: absolute; left: 2px; right: 2px; top: 2px; bottom: 2px;'></div>	   
				</div> 
			</div>
HTML

	# remove quebras de linha para uso com javascript
	$modelo =~ s/\r|\n/ /gm; 


	return $modelo;
	}
	

sub geraHeader
	{ my ($id,$inicial) = @_;	
		
	if($inicial ne "")
		{
		$H = "<ul><li id='end_li_$id'><span><select name='endereco_tipo' class='tipo_end'></select></span><span><a href='#end_tabs_$id'></a></span></li></ul>";
		}
	else
		{
		$H = "\$(\"<li id='end_li_$id'><span><select name='endereco_tipo' class='tipo_end'></select></span><span><a href='#end_tabs_$id'></a></span></li>\").appendTo(\$(\"#end_tabs\").find(\"ul\"));";
		# $H .= "\$(\"#end_tabs\").tabs(\"refresh\");";
		}
		
	$H =~ s/\r|\n/ /gm; 
		
	return $H;
	}
# [END] modelo de formulario de endereco ----------------------------------------------------------------------------------


# se for para adicionar nova aba
if($add ne "")
	{
	# retorno
	print "	<script>
				\$(\"#end_tabs\").append(\"".(geraModelo($add))."\");
				\$(\"<li id='end_li_$add'><span><select name='endereco_tipo' class='tipo_end'></select></span><span><a href='#end_tabs_$add'></a></span></li>\").appendTo(\$(\"#end_tabs\").find(\"ul\"));
				\$(\"#end_tabs\").tabs(\"refresh\");
				
				// gera e marca select estados
				\$(\"#end_tabs_$add select[name=uf]\").DList(
					{
					type: 'select', 
					table:'uf'
					});
					
				// gera e marca select paises
				\$(\"#end_tabs_$add select[name=pais]\").DList(
					{
					type: 'select',
					table:'pais'
					});
					
				// tipos de endereco de todas as tabelas
				\$('#end_li_$add select[name=endereco_tipo]').DList({
					type: 'select',
					table:'tipo_endereco',
					sql_order:'codigo' // ,
					// sql_limit:3
				});
					
				// atualiza nome do endereco
				\$('#end_tabs_$add input[name=endereco]')
					.keyup(function()
						{
						\$('#end_li_$add a').text(\$(this).val());
						});
                        
                        
                // campos text        
                \$('#aba_dados_$add input[type=text]').each(function(){
                    eos.template.field.text(\$(this));
                });
			</script>";
			
	exit;
	}
else
	{
	$add = 0;
	}
	
# se for inclusao 
if($COD eq "")
	{
	# $SQL = "select td.codigo as cod_doc, td.minidescrp as tipo_doc, td.descrp as empresa_doc from tipo_doc as td";
	
	# Tipos de endereco
	# $DB = DBE("select * from tipo_endereco order by descrp");
	# while($r = $DB->fetchrow_hashref)
	#	{
	#	$tipo_end .= "<input type='radio' name='tipo_end' value='$r->{'codigo'}'>";
	#	$tipo_end .= "$r->{'descrp'}";
	#	}
			
	# antigo botao para adicionar endereco
	# $R .= "<img src='/img/ui/add_aba.png' id='end_add_btn'>";
	
	$R .= geraHeader(0,0);
	$R .= geraModelo(0);
		
	print "	<script>				
				// gera e marca select estados
				\$(\"#end_tabs_0 select[name=uf]\").DList(
					{
					type: 'select', 
					table:'uf'
					});
					
				// gera e marca select paises
				\$(\"#end_tabs_0 select[name=pais]\").DList(
					{
					type: 'select',
					table:'pais'
					});
					
				// tipos de endereco de todas as tabelas
				\$('#end_li_0 select[name=endereco_tipo]').DList(
					{
					type: 'select',
					table:'tipo_endereco',
					sql_order:'codigo' //,
					// sql_limit:3
					});
					
					
				// atualiza nome do endereco
				\$('#end_tabs_0 input[name=endereco]')
					.keyup(function()
						{
						\$('#end_li_0 a').text(\$(this).val());
						});
			</script>";
	}
# edicao pega todos enderecos da empresa
else
	{
	$DB = DBE("
            select 
                ee.*, 
                te.descrp as tipo_end, 
                ep.descrp as problemas 
            from 
                empresa_endereco as ee 
            join 
                tipo_endereco as te on ee.tipo = te.codigo 
            left join 
                endereco_particularidades as ep on ee.codigo = ep.endereco 
            where 
                ee.empresa = $COD 
            order by 
                te.codigo, ee.codigo
    ");
	
	
	if($DB->rows() > 0) {
    	$header = 0;
    	while($E = $DB->fetchrow_hashref) {
    		print "	<script>
    					if('$header' == 0)
    						\$(\"#end_tabs\").html(\"<ul><li id='end_li_$E->{codigo}'><span><select name='endereco_tipo' class='tipo_end'></select></span><span><a href='#end_tabs_$E->{codigo}'></a></span></li></ul>\");
    					else
    						\$(\"<li><li id='end_li_$E->{codigo}'><span><select name='endereco_tipo' class='tipo_end'></select></span><span><a href='#end_tabs_$E->{codigo}'></a></span></li>\").appendTo(\$(\"#end_tabs\").find(\"ul\"));
					
    					\$(\"#end_tabs\").append(\"".(geraModelo($E->{codigo}))."\");
					
    					\$(\"#end_tabs_$E->{codigo} input[name=endereco_codigo]\").val(\"$E->{codigo}\");
    					\$(\"#end_tabs_$E->{codigo} input[name=endereco]\").val(\"$E->{endereco}\");
    					\$(\"#end_li_$E->{codigo}\").find(\"a\").text(\"$E->{endereco}\");
    					\$(\"#end_tabs_$E->{codigo} input[name=complemento]\").val(\"$E->{complemento}\");
    					\$(\"#end_tabs_$E->{codigo} input[name=bairro]\").val(\"$E->{bairro}\");
    					\$(\"#end_tabs_$E->{codigo} input[name=cidade]\").val(\"$E->{cidade}\");
    					\$(\"#end_tabs_$E->{codigo} input[name=cep]\").val(\"$E->{cep}\");
    					\$(\"#end_tabs_$E->{codigo} textarea[name=problemas]\").val(\"$E->{problemas}\");
					
					
    					// gera e marca select estados
    					\$(\"#end_tabs_$E->{codigo} select[name=uf]\").DList(
    						{ 
    						table:'uf',
    						value	: '$E->{uf}'
    						});
						
    					// gera e marca select paises
    					\$(\"#end_tabs_$E->{codigo} select[name=pais]\").DList(
    						{ 
    						table:'pais',
    						value	: '$E->{pais}'
    						});
					
    					// tipos de endereco de todas as tabelas
    					\$(\"#end_li_$E->{codigo} select[name=endereco_tipo]\").DList(
    						{ 
    						table:\"tipo_endereco\",
    						sql_order:\"codigo\",
    						// sql_limit:3,
    						value:$E->{tipo}
    						});
					
					
    					// atualiza nome do endereco
    					\$('#end_tabs_$E->{codigo} input[name=endereco]')
    						.keyup(function()
    							{
    							\$('#end_li_$E->{codigo} a').text(\$(this).val());
    							});
						
						
    					// popula contatos
    					contato.list($E->{codigo});
    				</script>";
			
    		$header++;
    	}
        
		
print<<HTML;
<script>
	\$("#end_tabs").tabs();
	
	// funcao simular botao e abas laterais ---------------
	\$(".btn_dados").click(function() 
		{
		// remove classe inativa e coloca ativa
		\$(this).removeClass("aba_vertical_inactive").addClass("aba_vertical_active");

		// ajusta css do botao mapa
		\$(this).next("div").removeClass("aba_vertical_active").addClass("aba_vertical_inactive");

		// esconde aba mapas
		\$(this).closest("div.empresa_endereco_container_master").find("div.aba_mapa").fadeOut('fast');
		});


	\$(".btn_mapa").click(function() 
		{
		// remove classe inativa e coloca ativa
		\$(this).removeClass("aba_vertical_inactive").addClass("aba_vertical_active");

		// ajusta css do botao dados
		\$(this).prev("div").removeClass("aba_vertical_active").addClass("aba_vertical_inactive");

		// mostra div que contem o mapa da aba especifica
		\$(this).closest("div.empresa_endereco_container_master").find("div.aba_mapa").fadeIn('slow'); 

		// acha objeto formulario do endereco especifico
		var address = \$(this).parents(".empresa_endereco_container_master");
		
		// acha div container do mapa do endereco especico
		var aba_mapa = address.find(".aba_mapa"); 
		
		// gera variaveis para montar o mapa
		var address_vars = {};
		if(address.find("input[name=endereco]").val() != "")
			address_vars.address = address.find("input[name=endereco]").val();
		if(address.find("input[name=cidade]").val() != "")
			address_vars.city = address.find("input[name=cidade]").val();
		if(address.find("select[name=uf] :selected").text() != "")
			address_vars.state = address.find("select[name=uf] :selected").text();
		if(address.find("select[name=pais] :selected").text() != "")
			address_vars.country = address.find("select[name=pais] :selected").text();
		
		address_vars.descrp = \$("#nome").val()+"<hr>"+address.find("input[name=endereco]").val()+"<br>"+address.find("input[name=cidade]").val();
			
		// gera mapa
		aba_mapa.DMaps(address_vars).fadeIn('slow');
		});
		
        
        /* campos text */
        \$(".empresa_endereco_dados input[type=text]").each(function(){
            eos.template.field.text(\$(this));
        });
</script>
HTML

	    exit;
        
    } else {
    	$R .= geraHeader(0,0);
    	$R .= geraModelo(0);
    }
}


# retorno

print<<HTML;

	<script>
		\$("#end_tabs").html("$R");
		\$("#end_tabs").tabs();
	
		// tipos de endereco de todas as tabelas
		//\$("#end_tabs_tipo_$add").DList(
		//	{ 
		//	table:"tipo_endereco",
		//	sql_order:"codigo",
		//	sql_limit:3
		//	});
		
		// if($COD)
		// gera e marca select estados
		\$("#end_tabs_0 select[name=uf]").DList(
			{
			type: 'select', 
			table:'uf'
			});

		// gera e marca select paises
		\$("#end_tabs_0 select[name=pais]").DList(
			{
			type: 'select',
			table:'pais'
			});

		// tipos de endereco de todas as tabelas
		\$('#end_li_0 select[name=endereco_tipo]').DList(
			{
			type: 'select',
			table:'tipo_endereco',
			sql_order:'codigo'// ,
			// sql_limit:3
			});
	
		// atualiza nome do endereco
		\$('#end_tabs_0 input[name=endereco]')
			.keyup(function()
				{
				\$('#end_li_0 a').text(\$(this).val());
				});
	
		// adiciona nova aba
		// \$("#end_add_btn").click(function(){ alert("Adicionar ABA"); });
		
		// \$("<li><a href='#end_tabs_0'>$tipo_end</a></li>").appendTo(\$("#end_tabs").find( "ul" ));
		// \$("$R").insertAfter(\$("#end_tabs").find( "ul" ));
		// \$("#end_tabs").tabs( "refresh" );
            
        
        /* campos text */
        // console.log("final");
        \$("#aba_dados_$id input[type=text]").each(function(){
            eos.template.field.text(\$(this));
        });
        
        /* campos text */
        \$('#aba_dados_0 input[type=text]').each(function(){
                eos.template.field.text(\$(this));
        });
        
	</script>

HTML

exit;
