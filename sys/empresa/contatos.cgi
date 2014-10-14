#!/usr/bin/perl
 
# 
# end_change.cgi
# carrega tabs com enderecos
#

$nacess = '201';
require "../cfg/init.pl";

print $query->header({charset=>utf8});

# $COD = &get('COD');
$end = &get('end');
$add = &get('add');
$id_add = &get('id_add');


# ------------------------------------------------------------------------------------------------------------------------
# [INI] Novo BOX
# 	- FUTURO: melhorar o conteudo de novo box para otimizar o codigo
# ------------------------------------------------------------------------------------------------------------------------
if($add ne "") {
	$R = "<div class='contatos_container_dbox newbox' id='new_contato_$id_add'>";
	$R .= "		<div class='DTouchBoxes_title'>";
	$R .= "			<input type='hidden' name='contato_cod' value='n$id_add'>";
    $R .= "             <div class='contato_title_default' title='Definir como principal ?'>";
    $R .= "                 <input type='checkbox' class='checkbox_principal' value='n$id_add'>";
    $R .= "             </div>";
    $R .= "             <div class='contato_title_descrp'>";
    $R .= "                 <input type='text' name='contato_descrp'>";
    $R .= "             </div>";
	$R .= "		</div>";
    
    
#	$R .= "		<div id='contatos_form_$id_add' class='contatos_form'>";
#	$R .= "			<select name='field_tipo_form' class='field_tipo_form'></select>";
#   $R .= "			<input type='text' name='field_valor_form'>";
#	$R .= "			<div class='contatos_form_icons'>";
#	$R .= "				<span class='icon_add icon_add_$id_add' title='Adicionar novo dado'></span>";
#	$R .= "				<span class='icon_update icon_update_$id_add' title='Atualizar dado'></span>";
#	$R .= "			</div>";
#	$R .= "		</div>";
    
	$R .= "		<div id='contatos_form_$id_add' class='contatos_form'>";
    $R .= "			<div class='field_tipo_form_container'>";
	$R .= "			    <select name='field_tipo_form' class='field_tipo_form'></select>";
    $R .= "			</div>";
    $R .= "			<div class='field_valor_form_container'>";
    $R .= "			    <input type='text' name='field_valor_form'>";
    $R .= "			</div>";
	$R .= "			<div class='contatos_form_icons'>";
	$R .= "				<span class='icon_add icon_add_ icon_add_$id_add' title='Adicionar novo dado'></span>";
	$R .= "				<span class='icon_update icon_update_$id_add' title='Atualizar dado'></span>";
	$R .= "			</div>";
	$R .= "		</div>";
    
	$R .= "		<div id='contatos_container_$id_add' class='contatos_container'></div>";
	$R .= "</div>";

print<<HTML;
<script>
	// find container correto
	var container = "$add";
		container = container.replace("li","tabs");
		
	// adiciona box ao grupo
	\$("#"+container+" .endereco_contatos").append("$R");
	
	// cria touch boxes e remove classe para controle dos novos
	\$(".newbox").DTouchBoxes({ removeable:true }).removeClass("newbox");
</script>
HTML

print<<HTML;
	<script>
		// inicia radio
		\$("#contatos_container_$id_add").DTouchRadio(
			{
			// addItem:[$fields],
			orientation:"vertical",
			sortable:true,
            itemDel     : true,
			// editable: true,
			DTouchRadioClick: function()
				{
				// junta todos inputs da linha
				var linha = \$("input:radio[name='contatos_container_$id_add_radios']:checked").next().find('input[type=hidden]');
				
				// popula formulario do box
				linha.each(function()
					{
					\$("#contatos_form_$id_add select[name="+\$(this).prop('name')+"form]").val(\$(this).val());
					\$("#contatos_form_$id_add input[name="+\$(this).prop('name')+"form]").val(\$(this).val());
					});
				
				// mostra icone update
				\$("#contatos_form_$id_add .icon_update").show();
				},
			DTouchRadioUncheck: function()
				{
				// limpa formulario
				\$("#contatos_form_$id_add input").val("");
				
				// esconde icone update
				\$("#contatos_form_$id_add .icon_update").hide();
				}
			}); 
		
		// icone update dos formularios DTouchBoxes dos contatos
		\$(".icon_update_$id_add").click(function(){
			// box
			var box = \$(this).parents(".DTouchBoxes");

			// radio grupo
			var radio = box.find(".contatos_container");

			// formulario do box selecionado
			var form = box.find(".contatos_form");

			// junta todos inputs da linha
			var linha = box.find("input:radio:checked").next().find('input[type=hidden]');

			// navega entre os inputs da linha
			linha.each(function()
				{			
				// atualiza input hidden da lista
				\$(this).val(form.find("[name="+\$(this).prop('name')+"form]").val());

				// atualiza descricao
				var descrp = "";
				if(\$(this).prop('name')+"form" == "field_tipo_form")
					descrp = form.find("[name="+\$(this).prop('name')+"form] :selected").text();
				else
					descrp = form.find("[name="+\$(this).prop('name')+"form]").val();

				\$(this).next('span').text(descrp);			
				});	
		});

		// icone insert dos formularios DTouchBoxes dos contatos
		\$(".icon_add_$id_add").click(function(){
			// localiza box
			var box = \$(this).parents(".DTouchBoxes");

			// radio
			var radio = box.find(".contatos_container");

			// formulario do box selecionado
			var form = box.find(".contatos_form");

			var tipo = form.find("[name=field_tipo_form]").val();
			var tipo_descrp = form.find("[name=field_tipo_form] :selected").text();
			var valor = form.find("[name=field_valor_form]").val();
            
            var img = form.find("[name=field_tipo_form] :selected").css("background-image");
            if(img) {
                img = img.replace(".svg","_white.svg");
                img = img.replace(".png","_white.png");
            
                tipo_descrp = "<img style='background-image:"+img+";'  class='empresa_endereco_dados_list_img'/>";
            }
            
    		// testa campos
    		if(!form.find("[name=field_tipo_form] :selected").val() || form.find("[name=field_valor_form]").val() === "") {
    			\$.DDialog({
    			    message : "Campo Tipo e Descrição devem ser preenchidos !"
                });
    			return false;
    		}

			// gen. the line to add into a list object		
			var fields  = "<div class='a'><input type='hidden' value='"+tipo+"' name='field_tipo_'> <span>"+tipo_descrp+"</span></div>";
				fields += "<div class='b'><input type='hidden' value='"+valor+"' name='field_valor_'> <span>"+valor+"</span></div>";

			// add line
			radio.DTouchRadio("addItem",{val:'add-'+\$("input[name=field_tipo_]").length, descrp:fields});
		});
		
    	/* gera select tipo de contatos */
    	\$(".field_tipo_form").each(function(){
            \$(this)
                .prop({
                    id : "tipo_contato_"+eos.tools.idGen()
                })
                .fieldSelect({ 
                    table       : "tipo_contato",
                    placeholder : "Tipo de Contato",
                    type        : "simple"
                });
        });
        
        /* campos text */
        \$("#new_contato_$id_add input[type=text]").each(function(){
            eos.template.field.text(\$(this));
        });
        
        // ajusta contato principal da empresa
        \$("#contatos_container_$id_add").parent().find(".contato_title_default").click(function(){
            \$(this).parents(".endereco_contatos").find(".contato_title_default").removeClass("contato_title_default_selected");
            \$(this).addClass("contato_title_default_selected");
            
            \$(this).parents(".endereco_contatos").find(".checkbox_principal").prop("checked", false);
            \$(this).find(".checkbox_principal").prop("checked", true);
        });
	</script>
HTML

exit;
}
# [END] Novo BOX ------------------------------------------------------------------------------------------------------------------------





# ------------------------------------------------------------------------------------------------------------------------
# [INI] COMPATIBILIDADE (REMOVER APOS IMPORTACAO TOTAL)
# ------------------------------------------------------------------------------------------------------------------------
$DBT = DBE("select * from pg_tables where tablename='endereco_contato'");
if($DBT->rows() > 0)
	{
	$DB = DBE("select codigo from endereco_contato where endereco = $end");
	if($DB->rows > 0)
		{
		$COMPATIBILIDADE = 1;
		}
	}
#	
#	PROCURAR POR TODOS IF COM A VARIAVEL $COMPATIBILIDADE E REMOVER
# ------------------------------------------------------------------------------------------------------------------------
# [END] COMPATIBILIDADE (REMOVER APOS IMPORTACAO TOTAL)
# ------------------------------------------------------------------------------------------------------------------------

# gera boxes principais
if($COMPATIBILIDADE == 1)
	{
	$DB = DBE("select *, nome as descrp from endereco_contato where endereco = $end");
	}
else
	{
	$DB = DBE("select * from contato_endereco where empresa_endereco = $end");
	}
    
while($C = $DB->fetchrow_hashref) {
    
    $color = "";
    if($C->{default} == 1){
        $color = "contato_title_default_selected";
    }
    
	$R .= "<div class='contatos_container_dbox'>";
	$R .= "		<div class='DTouchBoxes_title'>";
	$R .= "			<input type='hidden' name='contato_cod' value='$C->{codigo}'> ";
    $R .= "             <div class='contato_title_default $color' title='Definir como principal ?'>";
    $R .= "                 <input type='checkbox' class='checkbox_principal' value='$C->{codigo}'>";
    $R .= "             </div>";
    $R .= "             <div class='contato_title_descrp'>";
    $R .= "                 <input type='text' name='contato_descrp' value='$C->{descrp}'>";
    $R .= "             </div>";
	$R .= "		</div>";
	$R .= "		<div id='contatos_form_$C->{codigo}' class='contatos_form'>";
    $R .= "			<div class='field_tipo_form_container'>";
	$R .= "			    <select name='field_tipo_form' class='field_tipo_form'></select>";
    $R .= "			</div>";
    $R .= "			<div class='field_valor_form_container'>";
    $R .= "			    <input type='text' name='field_valor_form'>";
    $R .= "			</div>";
	$R .= "			<div class='contatos_form_icons'>";
	$R .= "				<span class='icon_add icon_add_' title='Adicionar novo dado'></span>";
	$R .= "				<span class='icon_update' title='Atualizar dado'></span>";
	$R .= "			</div>";
	$R .= "		</div>";
	$R .= "		<div id='contatos_container_$C->{codigo}' class='contatos_container'></div>";
	$R .= "</div>";	
}

print<<HTML;
<script>
	\$("#end_tabs_$end .endereco_contatos").html("$R");
</script>
HTML

# popula conteudo
if($COMPATIBILIDADE == 1)
	{
	$DB = DBE("select *, nome as descrp from endereco_contato where endereco = $end");
	}
else
	{
	$DB = DBE("select * from contato_endereco where empresa_endereco = $end order by descrp");
	}
	
while($C = $DB->fetchrow_hashref)
	{
	if($COMPATIBILIDADE == 1)
		{
		$DB2 = DBE("select ec.*, ec.nome as descrp, tc.descrp as tipo_descrp from endereco_contato as ec left join tipo_contato as tc on tc.codigo = ec.tipo where ec.codigo = $C->{codigo}");
		}
	else
		{
		$DB2 = DBE("select cd.*, tc.descrp as tipo_descrp, tc.img as tipo_img from contato_dados as cd left join tipo_contato as tc on tc.codigo = cd.tipo where cd.contato_endereco = $C->{codigo} order by cd.codigo asc");
		}
	
	
	$fields = "";
	while($CI = $DB2->fetchrow_hashref) {		
		$fields .= "{";
		$fields .= "val:$CI->{codigo},";
		$fields .= "descrp:\"";
		$fields .= "    <div class='a'>";
        
        if($CI->{tipo_img}) {
            $CI->{tipo_img} =~ s/\.svg/_white\.svg/gm;
            $CI->{tipo_img} =~ s/\.png/_white\.png/gm;
            
            $fields .= "        <img src='$CI->{tipo_img}' tile='$CI->{tipo_descrp}' class='empresa_endereco_dados_list_img' />";
        } else {
            $fields .= "        $CI->{tipo_descrp}";
        }
        
        $fields .= "        <input type='hidden' value='$CI->{tipo}' name='field_tipo_'>";
        $fields .= "    </div>";
		$fields .= "    <div class='b'>";
        $fields .= "        $CI->{valor}";
        $fields .= "        <input type='hidden' value='$CI->{valor}' name='field_valor_'>";
        $fields .= "    </div>";
		$fields .= "\"},";
	}
	$fields = substr($fields, 0,-1); # remove ultima virgula

print<<HTML;
	<script>
		// inicia radio
		\$("#contatos_container_$C->{codigo}").DTouchRadio(
			{
			addItem:[$fields],
			orientation:"vertical",
			sortable:true,
			visibleItems:3,
			// editable: true,
            itemDel     : true,
			DTouchRadioClick: function()
				{
				// junta todos inputs da linha
				var linha = \$("input:radio[name='contatos_container_$C->{codigo}_radios']:checked").next().find('input[type=hidden]');
				
				// popula formulario do box
				linha.each(function()
					{
					\$("#contatos_form_$C->{codigo} select[name="+\$(this).prop('name')+"form]").val(\$(this).val());
					\$("#contatos_form_$C->{codigo} input[name="+\$(this).prop('name')+"form]").val(\$(this).val());
					});
				
				// mostra icone update
				\$("#contatos_form_$C->{codigo} .icon_update").show();
				},
			DTouchRadioUncheck: function()
				{
				// limpa formulario
				\$("#contatos_form_$C->{codigo} input").val("");
				
				// esconde icone update
				\$("#contatos_form_$C->{codigo} .icon_update").hide();
				},
            postFunction : function() {
                
            }
		}); 
        
        // ajusta contato principal da empresa
        \$("#contatos_container_$C->{codigo}").parent().find(".contato_title_default").click(function(){
            \$(this).parents(".endereco_contatos").find(".contato_title_default").removeClass("contato_title_default_selected");
            \$(this).addClass("contato_title_default_selected");
            
            \$(this).parents(".endereco_contatos").find(".checkbox_principal").prop("checked", false);
            \$(this).find(".checkbox_principal").prop("checked", true);
        });
	</script>
HTML
	}



print<<HTML;
<script>
	/** 
     *  DTouchBoxes
     */
	\$(".contatos_container_dbox").each(function(){
        \$(this).DTouchBoxes({ 
            removeable : true
        });
    });
	
	/** 
     *  Update Icon
     *      icone do formulario de update de itens
     */
	\$(".icon_update").click(function() {
		// box
		var box = \$(this).parents(".DTouchBoxes");
		
		// radio grupo
		var radio = box.find(".contatos_container");

		// formulario do box selecionado
		var form = box.find(".contatos_form");
		
		// junta todos inputs da linha
		var linha = box.find("input:radio:checked").next().find('input[type=hidden]');
				
		// navega entre os inputs da linha
		linha.each(function() {			
			// atualiza input hidden da lista
			\$(this).val(form.find("[name="+\$(this).prop('name')+"form]").val());

			// atualiza descricao
			var descrp = "";
			if(\$(this).prop('name')+"form" == "field_tipo_form")
				descrp = form.find("[name="+\$(this).prop('name')+"form] :selected").text();
			else
				descrp = form.find("[name="+\$(this).prop('name')+"form]").val();
			
			\$(this).next('span').text(descrp);			
		});
	});
		
	/** 
     *  Insert Icon
     *      icone do formulario de insert de itens
     */
	\$(".icon_add_").off("click").click(function() {
		// localiza box
		var box = \$(this).parents(".DTouchBoxes");

		// radio
		var radio = box.find(".contatos_container");

		// formulario do box selecionado
		var form = box.find(".contatos_form");
		
		var tipo = form.find("[name=field_tipo_form]").val();
		var tipo_descrp = form.find("[name=field_tipo_form] :selected").text();
		var valor = form.find("[name=field_valor_form]").val();
		
        var img = form.find("[name=field_tipo_form] :selected").css("background-image");
        if(img) {
            img = img.replace(".svg","_white.svg");
            img = img.replace(".png","_white.png");
            
            tipo_descrp = "<img style='background-image:"+img+";' class='empresa_endereco_dados_list_img'/>";
        }
                
		// testa campos
		if(!form.find("[name=field_tipo_form] :selected").val() || form.find("[name=field_valor_form]").val() === "") {
			\$.DDialog({
			    message : "Campo Tipo e Descrição devem ser preenchidos !"
            });
			return false;
		}
		
        // limpa campos apos incluir
        form.find("[name=field_tipo_form]").val("");
        form.find("[name=field_valor_form]").val("");
        
		// gen. the line to add into a list object		
		var fields  = "<div class='a'><input type='hidden' value='"+tipo+"' name='field_tipo_'> "+tipo_descrp+"</div>";
			fields += "<div class='b'><input type='hidden' value='"+valor+"' name='field_valor_'> "+valor+" </div>";

        

		// add line
		radio.DTouchRadio("addItem",{val:'add-'+\$("input[name=field_tipo_]").length, descrp:fields});
	});
	
    
    
	/* gera select tipo de contatos */
	\$(".field_tipo_form").each(function(){
        \$(this)
            .prop({
                id : "tipo_contato_"+eos.tools.idGen()
            })
            .fieldSelect({ 
                table       : "tipo_contato",
                placeholder : "Tipo de Contato",
                type        : "simple"
            });
    });
    
    /* campos text */
    \$(".endereco_contatos input[type=text]").each(function(){
        eos.template.field.text(\$(this));
    });
    
</script>

HTML
