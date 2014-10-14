
//Dependências do crop
loadJS("/comum/jquery-crop/js/jquery.Jcrop.min.js");
loadCSS("/comum/jquery-crop/css/jquery.Jcrop.css");

//Css Upload
loadCSS("/css/modulos/upload.css");

(function($){
	
$.fn.fieldUpload = function(settings,value) 
	{
	
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			enable			: true,
			destino			: '/sys/upload/upload.cgi',
			modo			: 'img',
			type			: Array(),
			maxsize			: '10000000',
			unique			: false,
			addItem			: "",
			table			: '',
			field			: '',
			coluna			: '',
			dropZone		: '',
			crop			: false,
			descrp			: false,
			editable		: false,
			UploadList		: '',
			UploadDelete		: '',
			UploadReturn		: '',
			FieldUploadAdd		: '',
			FieldUploadDel		: '',
			value			: $('#CAD input[name=COD]').val()
			
			}, settings || {});
		}
	else
		{
		switch(settings)
			{
			//Reset: Limpa Lista de Upload ---------------------------
			case "reset":				

				// remover todos os itens do radio group
				if(value == "hard")
					{
					// remove itens
					$(this).removeData("fieldUploadSettings");
					
					// limpa conteudo visual
					$(this).html("");
					
					return true;
					}
				
				// altera o valor visual
				FieldUploadReset($(this));
				return true;
			
			break;
			
			// add Item, adiciona item
			case "addItem":	
				// se objeto vazio
				if($(this).data("fieldUploadSettings")["FieldUploadAdd"] != "")
					{
					$(this).data("fieldUploadSettings")["FieldUploadAdd"].push(value);
					}
				else
					{
					$(this).data("fieldUploadSettings")["FieldUploadAdd"] = value;
					}
					
				// limpa variavel de adicao de itens
				$(this).data("fieldUploadSettings")["addItem"] = "";
				// adiciona itens
				FieldUploadAdd($(this));

				// aguarda o retorno da criacao para gerar o objeto
				return true;
				
			break;
			
			// add Item, adiciona item
			case "removeItem":
				
				// retorna o valor do radio grupo se segunda opcao for vazia
				if(!value)
					{
					try 
						{ 
						return $(this).data("fieldUploadSettings")["value"];
						} 
					catch(err) 
						{ 
						return "";
						}
					}
				
				if(isFunction(settings.UploadDelete)===true)
					settings.UploadDelete(value);
				else
					// altera o valor visual
					FieldUploadRemove($(this));
				
				return true;
				
			break;
			}
		
		
		// retorna / seta demais opcoes que nao necessitam de tratamento
		if(value == "")
			{
			return $(this).data("fieldUploadSettings")[settings];
			}
		else
			{
			$(this).data("fieldUploadSettings")[settings] = value;
			return true;
			}
		}
		
		
	return this.each(function()
		{
		
//[FIM] --- ESTRUTURAÇÃO DO PLUGIN ----------------------------------------------------------------------------------------------------------
		
		// salva opcoes setadas do objeto para uso futuro
		if(isObject(settings) === true)
			$(this).data("fieldUploadSettings", settings);
		
		
		//[INI] --------------------- Monta a estrutura do formulário --------------------- //
		
		//Verifica se existe tipo estipulado caso contrário pega o padrão (imagem).
		if(settings.type == "doc")
			settings.type= new Array (".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt",".odt");
		else if(settings.type == "doc,img")
			settings.type= new Array (".doc", ".docx", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx", ".txt",".odt",".jpeg", ".png", ".jpg");
			
		//Se não tiver dropZone definido seta o bloco do upload
		if(settings.dropZone == "")
			settings.dropZone=$(this);
			
		//Bota o enctype no formulário pai para poder enviar o arquivo
		$(this).parents('#CAD').prop("enctype","multipart/form-data");
		
		//[INI] Monta o 'form' para upload ----------------------------------------------------------------------------
		var form_upload='';
		
		form_upload='<progress id="upload_progress" max="100" value="0"></progress><span id="progress">0%</span>';
		form_upload +='<span class="file-wrapper">';
		form_upload +='<input type="file" id="fieldUploadInputFile" name="file[]" multiple="multiple">';		
		form_upload +='<span class="button">Escolha o arquivo</span>';
		form_upload +='</span>';
		if(settings.descrp===true)
			{
			form_upload +='<span id="fieldUploadDescrp"> Descrição:<input placeholder="Preencha a descrição primeiramente." name="fieldUploadDescrp" type="text"></span>';
			}
		form_upload +='<span class="file-wrapper"><span class="button" id="fieldUploadSubmit">Upload</span></span>';
		form_upload +='<div id="fieldUploadList"></div>';
		if(settings.crop===true)
			{
			form_upload +='<div id="FieldUploadCrop">';
			form_upload +='</div>';
			}
			
		//Cria o elemento no form
		$(this).html("");
		$(this).html(form_upload);
		
		//[FIM] --------------------- Monta a estrutura do formulário --------------------- //
		
		// Em caso de setar o plugin já com items
		if(isArray(settings.addItem) === true && settings.addItem.length == 0)
			{ // se for um array vazio passado limpa o radio

			// remove itens
			$(this).removeData("fieldUploadSettings");
					
			return true;
			}
		else if(settings.addItem)
			{			
			// ajusta para criacao
			$(this).data("fieldUploadSettings")["FieldUploadAdd"] = settings.addItem;
			
			// limpa variavel de adicao de itens
			$(this).data("fieldUploadSettings")["addItem"] = "";
			
			//Limpa a variável
			cont=0;
			
			// adiciona itens
			FieldUploadAdd($(this));
			
			// aguarda o retorno da criacao para gerar o objeto
			return true;
			}
			
		// se Editable habilitado
		if(settings.editable !==false)
			{
			// insere botao de exclusao se nao existir
			$(this).find(".fieldUploadItems").each(function()
				{
				// pega ultima div 
				radio_del = $(this).find("div").last();
								
				// se nao achar ultima div ajusta para mostrar botao de deletar mesmo assim
				if(radio_del.length == 0)
					radio_del = $(this);
				
				if(radio_del.find(".FieldUploadDelItem").length == 0)
					radio_del.append("<p class='FieldUploadDelItem'></p>");
				});
			
			// Remove Radio Item 
			// .off("click") o uso de unbinding do click se fez necessario para velocidade de resposta
			$(this).find(".FieldUploadDelItem").off("click").click(function(event) 
				{
				// evita que o trigger click da linha seja executado
				event.stopPropagation();		
				// ajusta obj (item linha) para exclusao
				var obj = $(this);
				var remove_radio_item = function()
					{
					// funcao post delecao do objeto visual
					if(isFunction(settings.editable))
						{ // envia o valor do objeto clicado para delecao
						settings.editable.call(this, obj.parents(".DTouchRadio_items").find("input:radio[name='"+settings.radios_id+"_radios']").val());
						
							
						}		
					// remove objeto low level e html
					DTouchRadioDelItems(obj);
					}
				
				// confirmacao de exclusao
				if(settings.delNoCheck === false)
					confirma("Deseja remover o item selecionado? <br><br> essa ação é irreversível !",remove_radio_item,"");
				else
					DTouchRadioDelItems(obj);
				});
			}
		
		
			
		//url de destino
		var url = settings.destino;
		var obj = $(this);
		
//[FIM] --- ESTRUTURAÇÃO DO PLUGIN ----------------------------------------------------------------------------------------------------------
		
//[INI]--- Função principal que executa o upload --------------------------------------------------------------------------------------------
		//Envio do arquivo e recebimento da resposta
		var handleUpload = function(event)
			{
			//Evita propagação e click padrão
			event.preventDefault();
			event.stopPropagation();
			
			//Pega o input dentro elemento
			var fileInput= obj.find('input[type=file]')[0];
			
			//Inicia a data
			var data = new FormData(document.getElementById("CAD"));
			
			data.append("FieldUploadTable",settings.table);
			data.append("FieldUploadField",settings.field);
			data.append("FieldUploadColum",settings.coluna);
			
			if(isFunction(settings.UploadReturn) === true)
				data.append("action","upload_personalizado");
			
// 			data.append('ajax',true);
			
// 			for (var i=0; i<fileInput.files.length; i++)
// 				{
// 				data.append('file[]',fileInput.files[i]);
// 				}
				
			var request = new XMLHttpRequest();
			
			// Enquanto faz o upload exibe um progress bar.
			request.upload.addEventListener('progress', function(event)
				{
				if(event.lengthComputable)
					{
					var percent = event.loaded / event.total;
					obj.find('#upload_progress, #progress').fadeIn();
					obj.find("#upload_progress").prop('value',Math.round(percent * 100));
					obj.find("#progress").text(Math.round(percent * 100)+"%");
					}
				});
			//Depois que carregou/enviou o arquivos
			request.upload.addEventListener('load', function(event)
				{
				obj.find('#upload_progress, #progress').fadeOut();
				obj.find('.file-wrapper, #fieldUploadDescrp').fadeIn();
				});
			//Em caso de erro
			request.upload.addEventListener('error', function(event)
				{
				alerta('Upload Falhou.');
				obj.find('#upload_progress, #progress').hide();
				obj.find('.file-wrapper, #fieldUploadDescrp').show();
				return false;
				});
			
			//Request de finalização
			request.addEventListener('readystatechange',function(event)
				{
				//Se a transação foi feita
				if(this.readyState==4)
					{
					obj.find('#upload_progress, #progress').hide();
					obj.find('.file-wrapper, #fieldUploadDescrp').fadeIn();
					//Se a transação foi concluída
					if(this.status==200)
						{
						obj.find('input[type=file]')[0].value="";
// 						var  links = document.getElementById('uploaded');
						if(settings.unique !==false)
							{
							if(obj.find("input[type=hidden]").val()!="")
								{
								FieldUploadRemove(obj.find("input[type=hidden]").val(),obj);
								}
							obj.find('#fieldUploadList').html('');
							}
						
						$("#resultado").html(this.responseText);
						
						
						//Se tiver crop ativado chama a funcao
						if(settings.crop===true)
							{
							FieldUploadCrop(obj,FieldUpload);
							}
						//Retorno personalizado, passado o result
						if(isFunction(settings.UploadReturn) === true)
							settings.UploadReturn(FieldUpload);
						}
					else
						{
						alerta('Falha ao executar o upload.');
						return false;
						}
					}
				});
			
			console.log("Enviando");
			
			request.open('POST',settings.destino, true);
			request.setRequestHeader('Cache-Control','no-cache');
			
			obj.find('#upload_progress, #progress').show();
			
			request.send(data);
			
			}
//[FIM]--- Função principal que executa o upload -----------------------------------------------------------------------------------------------

//[INI]--- Função click do upload --------------------------------------------------------------------------------------------------------------
		obj.find('#fieldUploadSubmit').off("click").click(function(event) 
			{
			if(obj.find('input[type=file]')[0].value !="")
				{
				obj.find('.file-wrapper, #fieldUploadDescrp').hide();
				handleUpload(event);
				}
			else
				{
				alerta("Selecione um arquivo");
				return false;
				}
			});
//[FIM]--- Função click do upload -------------------------------------------------------------------------------------------------------------
		
//[INI]--- Função de selecionar os arquivos, faz as verificações e restrições -----------------------------------------------------------------
		obj.find('#fieldUploadInputFile').change(function(event) 
			{
			//Pega o input dentro elemento
			var fileInput = obj.find('input[type=file]')[0].files;
			var FilesList = ""; 
			
			//Faz o for para verificar em todos os arquivos
			for(var i=0; i<fileInput.length; ++i)
				{
				//pega a extensão do arquivo selecionado
				var Ext = fileInput[i].name.substring(fileInput[i].name.lastIndexOf('.')).toLowerCase();
				//Verifica se o tipo é permitido
				if (settings.type.indexOf(Ext) < 0 && settings.type !="all")
					{
					alerta("Tipo de arquivo ("+Ext+") não permitido!");
					obj.find('input[type=file]')[0].value="";
					return false;
					}
				// Verifica se o tamanho do arquivo não é maior que o permitido	
				else if (fileInput[i].size > settings.maxsize || fileInput[i].size==0) 
						{ // 2mb
						alerta('Tamanho do arquivo ('+fileInput[i].name+') é maior que o limite estipulado ou está vazio!');
						obj.find('input[type=file]')[0].value="";
						return false;
						}
// 					//Adiciona na lista de verificação
// 					else
// 						{
// 						if(fileInput.length==1)
// 							FilesList =fileInput[i].name+"<br>";
// 						else
// 							
// 							FilesList +=fileInput[i].name+"<br>";
// 						}
				}
// 					obj.find('#fieldUploadList').html(FilesList);
			});
//[FIM]--- Função de selecionar os arquivos, faz as verificações e restrições -----------------------------------------------------------------

		
		 // Listagem Personalizada
		if(isFunction(settings.UploadList)===true)
			{
			var table = settings.table;
			var field = settings.field;
			var coluna = settings.coluna;
			settings.UploadList(table,field,coluna);
			}
		// Listagem Padrão
		else
			{
			id_cad= settings.value;
			UploadListAuto(id_cad,obj);
			}
		});
	};

})( jQuery );





//Contador
var cont=0;
// [INI] FieldUploadAdd: Adiciona itens no list do upload----------------------------------------------------------------
function FieldUploadAdd(obj)
	{
	var showVal = ""; 
	var showImg = "";
	var delitem = "";
	var settings = obj.data("fieldUploadSettings"); // acesso as configuracoes atuais do objeto
	var items = settings.FieldUploadAdd;
	
	// monta itens e adiciona no objeto
	for(var f in items)
		{
		// ajusta se nao tiver descricao
		if(items[f]['descrp'] == "")
			items[f]['descrp'] = items[f]['val'];
		else
			
		// ajusta se tem imagem
		if(items[f]['img'])
			showImg = "<img src='"+items[f]['img']+"' />";
		else
			showImg="";
		
		// adiciona objeto no radio on the fly	
		obj.find("#fieldUploadList").last().append("<div class='fieldUploadItems'><input type='hidden' name='FileUploadFile"+cont+"' value='"+items[f]['val']+"' />"+showVal+" "+showImg+"<span class='FieldUploadDescrp'>"+items[f]['descrp']+"</span></div>");
		
		// se Editable habilitado
		if(settings.editable !==false)
			{
			// insere botao de exclusao se nao existir
			obj.find(".fieldUploadItems").last().append("<p class='FieldUploadDelItem'></p>");
			}
		cont++;
		}
		
		//Download do arquivo
		obj.find(".fieldUploadItems").off("click").click(function(event)
			{
			var md5=$(this).find("input[type=hidden]").val();

			$("body").append("<form id='FieldUploadForm' action='/sys/upload/download.cgi' target='_blank' method='POST'  > </form>")
			$("#FieldUploadForm").append("<input type=hidden name='MD5' id='MD5' value='"+md5+"'>");
			$("#FieldUploadForm").submit();
			$("#FieldUploadForm").remove();
			});
		
		// Remove Radio Item 
		// .off("click") o uso de unbinding do click se fez necessario para velocidade de resposta
		obj.find(".FieldUploadDelItem").off("click").click(function(event)
			{
			
			var val = $(this).parent().find('input[type=hidden]').val();
			$(this).parent().remove();
			
			
			if(isFunction(settings.UploadDelete)===true)
				settings.UploadDelete(val);
			else
				FieldUploadRemove(val,obj);
// 			// evita que o trigger click da linha seja executado
// 			event.stopPropagation();		
// 			// ajusta obj (item linha) para exclusao
// 			var obj = $(this);
// 			var remove_radio_item = function()
// 				{
// 				// funcao post delecao do objeto visual
// 				if(isFunction(settings.editable))
// 					{ // envia o valor do objeto clicado para delecao
// 					settings.editable.call(this, obj.parents(".DTouchRadio_items").find("input:radio[name='"+settings.radios_id+"_radios']").val());
// 					
// 						
// 					}		
// 				// remove objeto low level e html
// 				DTouchRadioDelItems(obj);
// 				}
// 			
// 			// confirmacao de exclusao
// 			if(settings.delNoCheck === false)
// 				confirma("Deseja remover o item selecionado? <br><br> essa ação é irreversível !",remove_radio_item,"");
// 			else
// 				DTouchRadioDelItems(obj);
			});
	
	$("#upload").data("fieldUploadSettings")["FieldUploadAdd"]="";
	
	}
	
// [INI] Limpa os items da list, reset o input file e limpa a descrição.
function FieldUploadReset(obj)
	{
	var settings = obj.data("fieldUploadSettings"); // acesso as configuracoes atuais do objeto
	obj.find('#fieldUploadList').html('');
	obj.find('#fieldUploadInputFile')[0].value="";
	obj.find('input[name=fieldUploadDescrp]').val('');
	}

//Função que remove o arquivo em caso de erro.
function FieldUploadRemove(val,obj)
		{
		var settings = obj.data("fieldUploadSettings");	
		req="&FieldUploadColum="+settings.coluna+"&FieldUploadTable="+settings.table+"&FieldUploadField="+settings.field+"&action=delete"+"&cod_arq="+val;

		DActionAjax('/sys/upload/upload.cgi',req,obj,true);
		}
			
//Função que lista os uploads
function UploadListAuto(val,obj)
		{
		var settings = obj.data("fieldUploadSettings");
		if(val=="" || !val){val="null";}
		
		req="&FieldUploadColum="+settings.coluna+"&FieldUploadTable="+settings.table+"&FieldUploadField="+settings.field+"&action=list"+"&COD="+val;

		DActionAjax('/sys/upload/upload.cgi',req,obj);
		
		return true;
		}
		
function FieldUploadCrop(obj,FieldUpload)
	{
	
 	var settings = obj.data("fieldUploadSettings");
	var md5=FieldUpload["MD5"];
	
	var form_crop ='<div id="FieldUploadModal">';
	form_crop +='<img src="/sys/cfg/DPAC/view_avatar.cgi?MD5='+md5+'" id="UploaImgCrop"/>';
	form_crop +='<input type="hidden" size="4" id="x" name="x" />';
	form_crop +='<input type="hidden" size="4" id="y" name="y" />';
	form_crop +='<input type="hidden" size="4" id="w" name="w" />';
	form_crop +='<input type="hidden" size="4" id="h" name="h" />';
	form_crop +='<input type="hidden" size="4" id="md5" value="'+md5+'" name="md5" />';
	form_crop +='</div>';
	
	//Popula a imagem no modal
	obj.find("#FieldUploadCrop").append(form_crop);
	
	//Monta o crop na imagem
	obj.find('#UploaImgCrop').Jcrop(
		{
		onChange:   showCoords,
		onSelect:   showCoords,
		bgFade: true,
		minSize: [ 95, 100 ],
		maxSize: [ 570, 600 ]
		});
	//Pega os valores do corte e popula os campos		
	function showCoords(c)
		{
		$('#x').val(c.x);
		$('#y').val(c.y);
		$('#h').val(c.h);
		$('#w').val(c.w);
		}
	//Cria o modal com a imagem
	obj.find("#FieldUploadModal").dialog(
		{
                position: ['center','top'],
		autoOpen: true,
		resizable: true,
		modal: true,
		show: 
			{
			effect: "fadeIn",
			duration: 500
			},
			hide: 
			{
			effect: "explode",
			duration: 500
			},
		buttons: 
			{
			//Botão cortar
			"Cortar": function() 
				{
				$(this).dialog('close');
				req="&x="+$("#x").val()+"&y="+$("#y").val()+"&w="+$("#w").val()+"&h="+$("#h").val()+"&md5="+$("#md5").val();
				
				DActionAjax('/sys/upload/resize.cgi',req,'',true);
				},
			//Botão cancel
			"Cancelar": function() 
				{
				$( this ).dialog( "close" );
				}
			}
		});
	
	//Esconde o botão fechar.
	obj.find(".ui-dialog-titlebar-close").hide();
	}