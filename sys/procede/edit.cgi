#!/usr/bin/perl

$nacess = "207";
require "../cfg/init.pl";

$COD = &get('codigo');

print $query->header({charset=>utf8});

# carrega valores do banco de dados
$n=0;

require "./edit_db.pl";

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
HTML

print "<script language='JavaScript'> 
	\$(document).ready(function(){
		\$('#titulo').val('$titulo');
		if('$endereco_descrp' != '') {
			\$('#enderecos').html('<br>Endereço(s): ".$endereco_descrp."');
		}
		\$('#procedimento').fieldTextEditor();
		\$('#procedimento').wysiwyg('setContent', '".&get($procedimento, 'HTML')."');
		\$('#detalhe_proced').DTouchBoxes({title:'Detalhes do Procedimento'});
		
		// filter TAGs
		\$('#tags_container').DTouchBoxes();
		\$('#tags_list').DTouchRadio({ 
			orientation : 'vertical',
			// editable    : true,
            itemDel     : true,
			unique      : true";
if($tags_list ne "")
	{
	print ",
			addItem     : [".$tags_list."]";
	}
print "	
		});
        
		\$('#tag').fieldAutoComplete({
			sql_tbl		: 'procedimentos_tags_tipo',
			allowEmpty	: 'true',
            clearOnExit  : true,
            itemAdd      : true,
			postFunction	: function(x){
                
				if(x.item.value !== '') {
					\$('#tags_list').DTouchRadio('additem',{
                        val : x.item.value,
                        descrp : x.item.value
                    });
				}
			}
		});";
		
if($COD eq "")
	{
print<<HTML;
		// filter cliente
		\$('#cliente_container').DTouchBoxes();
		\$('#cliente').fieldAutoComplete(
			{ 
			type		: 'empresa',
			postFunction	: function(x) {
				if(\$('#cliente').val() != '') {
					\$.DActionAjax({
						action:"empresa_endereco.cgi",
						req: "empresa="+\$("#cliente").val(),
						loader: \$("#cliente_container"),
						serializeForm: false,
						postFunction: function(){
							if(\$("#COD").val()){
								\$("#cliente_endereco").DTouchRadio("disable");
							}
						}
					});
				}
			},
			onReset		: function() {
				\$("#cliente_endereco").DTouchRadio("reset","hard");
				},
			placeholder: "Selecione o Cliente"
			});
HTML
	}
else
	{
print<<HTML;
		//Upload de arquivo
		\$('#bloco_upload').DTouchBoxes({title:'Arquivos Anexos'});

		// inicia lista 
		\$("#upload_list").DTouchRadio({
		    orientation : "vertical",
HTML
if($arq_list ne "")
	{
	print "			addItem: [".$arq_list."],";
	}
print<<HTML;    
		    itemDel     : function(x){
			eos.core.upload.delete(x);
		    },
		    click       : function(x){
			eos.core.upload.download(x.value);
		    } 
		});
		
		// inicia upload field
		\$("#upload").DUpload({
		    link : {
			tbl    	 : "procedimentos",
			codigo   : $COD
		    },
		    automatic: true,
		    postFunction : function(x){
			\$("#upload_list").DTouchRadio("addItem",{
			    val    : x.codigo,
			    descrp : x.descrp
			});
			\$("#upload").DUpload("reset"); // limpa campo apos inclusao
		    }
		});
HTML
	}
print<<HTML;	
		});
		
	</script>
</head>
<body>
<input type='hidden' name='codigo_save' value='$COD'>
<div style="margin: 20px; height: 100%;">
	<div id="detalhe_proced">
		<br>Título:<input type="text" name="titulo" id="titulo" />
		<div id="enderecos">
		</div>
		<div id="categorias">
		</div>
		<br>
		Procedimento:
		<br>
		<textarea id="procedimento" name="procedimento"></textarea>
	</div>
HTML

if($empresa_cod ne "")
	{
	print "<input type='hidden' name='cliente' value='$empresa_cod'>";
	if($COD ne "")
		{
print<<HTML;
      <div id="bloco_upload">
	      <div id="upload"></div>
	      <div id="upload_list"></div>
      </div>
HTML
		}
	}
else
	{
	if($COD eq "")
		{
print<<HTML;
	<!-- cliente / endereco -->
	<div id="cliente_container">
		<div class='DTouchBoxes_title DTouchBoxes_title_input'>
			<input type="text" name="cliente" id="cliente" placeholder="Cliente"/>
		</div>
		<div id="cliente_endereco" class="DTouchBoxes_line_list"></div>
	</div>
HTML
		}
	else
		{
print<<HTML;
	<div id="bloco_upload">
		<div id="upload"></div>
		<div id="upload_list"></div>
	</div>
HTML
		}
	}
print<<HTML;
	<!-- lista de TAGs -->
	<div id="tags_container">
		<div class='DTouchBoxes_title DTouchBoxes_title_input'>
			<input type="text" name="tag" id="tag" placeholder="Etiqueta ou categoria" />
		</div>
		<div id="tags_list" class="DTouchBoxes_line_list_input_title"></div>
	</div>

</div>

</body>
</html>
HTML



