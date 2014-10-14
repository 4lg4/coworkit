/**
 * 
 *  D-Upload
 *      Upload simples e multiplo
 *
 *  @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://adriano.gaiattos.com/)
 */

(function($){
	
$.fn.DUpload = function(settings,value){
        
    	if(isObject(settings) || !settings) { // setter
    		var s = $.extend({
    			multiple      : false,                  // upload multiplo
                refresh       : 600,                    // tempo de atualizacao para ver o status do arquivo 
                placeholder   : "Descrição do arquivo", // placeholder
                mimetype      : "",                     // lista de mime types permitidos
                disk          : true,                   // valida on the fly o espaco em disco
                link          : false,                  // tbl vinculo para arquivo link : { tbl, codigo }
                postFunction  : false,                  // executa funcao apos finalizar upload
                serializeForm : false,                  // serializa formulario se necessario
                automatic     : false                   // executa upload automatico
            }, settings || {});
            
    	} else { // getter / setter unico
        
    		switch(settings.lc()) {
    			case "upload":
                    
                    if(!$(this).val()){
                        $.DDialog({
                            type    : "alert",
                            message : "Selecionar o arquivo antes de fazer upload!"
                        });
                        
                        return false;
                    }
                    
                    upload($(this));
                    return true;
    			break;

                case "reset":  
                    /* clear file field */
                    $(this)
                        .val("");
                        
                    /* field descrp */
                    $(this).parent().find("input[type=text]")
                        .removeClass()
                        .val("");
                
                    /* nome real mostra na div do nome */
                    $(this).parent().find(".EOS_template_field_file_name")
                        .removeClass("EOS_template_field_file_name_populated")
                        .text("");
                    
                    /* mostra tamanho do arquivo na barra de progresso */
                    $(this).parent().find(".EOS_template_field_file_progress")
                        .removeClass("EOS_template_field_file_progress_populated");
                    
                    /* mostra tamanho do arquivo na barra de progresso */    
                    $(this).parent().find(".EOS_template_field_file_progress_descrp")
                        .text("");
                    
                    /* barra de progresso */
                    $(this).parent().find(".EOS_template_field_file_progress_bar")
                        .css("width","0px");
                            
                    return true;
                break;
            
                case "focus":
                    $(this).trigger("click");
                    return true;
                break;
            
                case "disable" :
                    return true;
                break;
                
                
    		}
		
    		// retorna / seta demais opcoes que nao necessitam de tratamento
    		if(!value) {
    			// return $(this).data("DUpload")[settings];
                return true;
    		} else {
    			// $(this).data("DUpload")[settings] = value;
    			return true;
    		}
    	}
		        
        /* Upload test 1 */	
        // caches estao em DPAC.js
        cacheDUploadInterval = {};
        cacheDUploadControl  = {};
        // cacheDUploadCodigo   = {};
        cacheDUploadObj      = {};
        // eos.core.cache.DUpload.control = {};
        // eos.core.cache.DUpload.file    = {};        
        
        /** 
         *  Done
         *      quando script de upload terminar dispara eos.core.upload.done()
         */
        
        /** 
         *  Progress
         *      controle progresso 
         */
        function progress(uuid,obj) {
            
            if(!cacheDUploadControl[uuid]) {
                
                cacheDUploadControl[uuid] = true; // inicia controle para n disparar diversas solicitacoes sem necessidade
                
            	var req = new XMLHttpRequest();
            	    req.open("GET", "/progress", true);
            	    req.setRequestHeader("X-Progress-ID", uuid);
            	    req.onreadystatechange = function() {
                
            		if(req.readyState == 4) {
            
                        if(req.status == 200) {                
				
                            var upload     = JSON.parse(req.responseText)
                            ,   receivedMB = eos.core.math.toMB({ value:upload.received, decimal:2 })
                            ,   percent    = (upload.received * 100) / upload.size;
                            
                            if(upload.state === 'starting') { // iniciando
                                
                                /* mostra tamanho do arquivo na barra de progresso */
                                obj.parent().find(".EOS_template_field_file_progress_descrp")
                                    .text("iniciando...");
                                
                                /* remove controle de solicitacao quando respondido */
                                delete cacheDUploadControl[uuid];
                                
                            } else if(upload.state === 'started' || upload.state === 'uploading') { // atualiza progressbar
                            
                                /* mostra tamanho do arquivo na barra de progresso */
                                obj.parent().find(".EOS_template_field_file_progress_descrp")
                                    .text(receivedMB+"MB");
                                
                                /* barra de progresso */
                                obj.parent().find(".EOS_template_field_file_progress_bar")
                                    .css("width",percent+"%");
                                    
                                /* remove controle de solicitacao quando respondido */
                                delete cacheDUploadControl[uuid];
            				
                            } else if(upload.state == 'done') { // ao finalizar
                                
                                /* limpa timer */
            					window.clearTimeout(cacheDUploadInterval[uuid]);
                                delete cacheDUploadInterval[uuid];
                                delete cacheDUploadControl[uuid];
                            
                                /* mostra tamanho do arquivo na barra de progresso */
                                obj.parent().find(".EOS_template_field_file_progress_descrp")
                                    // .text(eos.core.math.toMB({ value:upload.size, decimal:2 })+"MB");
                                    .text("concluído");
                                
                                /* barra de progresso */
                                obj.parent().find(".EOS_template_field_file_progress_bar")
                                    .css("width","100%");
                                    
                                
            				} else { // erro
                                
                                /* limpa timer e controle */
            					window.clearTimeout(cacheDUploadInterval[uuid]);
                                delete cacheDUploadInterval[uuid];
                                delete cacheDUploadControl[uuid];
                                delete cacheDUploadObj[uuid];
                            
                                /* remove controles de upload */
                                document.getElementById("uploadframe_"+uuid).remove();
                                document.getElementById("uploadform_"+uuid).remove();
                        
                                $.DDialog({
                                    type    : "alert",
                                    message : "Erro interno, entre em contato com o suporte <br> Obrigado !"
                                });
                                
            		        } 
                            
                        }  
            		} 
            	}
            	req.send(null);
                
            } 
            
        }
        
        
        /** 
         *  Upload
         *      submete arquivo e define controlador do progresso 
         */
        function upload(obj) { 
            var s = obj.data("DUploadSettings");            
            
        	uuid = eos.core.genId();  // generate random progress-id 
            
            /* codigo arquivo */
            cacheDUploadObj[uuid]    = obj; 
            
            /* timer */
        	cacheDUploadInterval[uuid] = window.setInterval(function(){  // seta interval de atualizacao para 1000 ms
                progress(uuid,obj);
            }, 500);
            
            /* Upload Frame */
            var uploadframe = document.createElement("iframe");
                uploadframe.id   = "uploadframe_"+uuid; 
                uploadframe.name = "uploadframe_"+uuid; 
                uploadframe.src  = "about:blank";
            
            document.querySelector("#CAD").appendChild(uploadframe); // adiciona frame de upload no documento
            /*
            var form = document.createElement("form");
                form.id      = "uploadform_"+uuid;
                form.name    = "uploadform_"+uuid;
                form.method  = "POST";
                form.enctype = "multipart/form-data";
                form.target  = "uploadframe_"+uuid;
                form.action  = "/sys/upload/DUpload.cgi?X-Progress-ID="+uuid;
            */
            var form = document.createElement("div");
                form.id      = "uploadform_"+uuid;
                form.name    = "uploadform_"+uuid;
        
            /* monta formulario de upload 
            if(s.serializeForm) {
                ($("#CAD").serialize().split('&')).forEach(function(v) {
                    // campos
                    var field = document.createElement("input");
                        field.type  = "hidden";
                        field.name  = v.split('=')[0];
                        field.value = v.split('=')[1];
            
                    form.appendChild(field); // adiciona campo
                });
            }
            */
            
            /* adiciona campo ID */
            var field = document.createElement("input");
                field.type  = "hidden";
                field.name  = "ID";
                field.value = document.querySelector("#AUX input[name=ID]").value;
            form.appendChild(field);
            
            /* adiciona campo do upload */
            /*
            var fieldupload = obj.clone().prop({
                    id   : "DUpload_"+uuid,
                    name : "DUpload"
                }).show();
            form.appendChild(fieldupload[0]);
            */
            var field = document.createElement("input");
                field.type  = "hidden";
                field.name  = "DUpload";
                field.value = obj.prop("name");
            form.appendChild(field);
            
            /* adiciona campo descrp do upload */
            var field = document.createElement("input");
                field.type  = "hidden";
                field.name  = "DUpload_descrp";
                field.value = obj.parent().find("input[type=text]").val();
            form.appendChild(field);
            
            
            /* adiciona campo uuid */
            var field = document.createElement("input");
                field.type  = "hidden";
                field.name  = "uuid";
                field.value = uuid;
            form.appendChild(field);
            
            
            /* link, campos para vinculo do upload */
            if(eos.core.is.object(s.link)) { // vinculo especifico
                
                var field = document.createElement("input");
                    field.type  = "hidden";
                    field.name  = "link";
                    field.value = s.link.tbl;
                form.appendChild(field);
                
                var field = document.createElement("input");
                    field.type  = "hidden";
                    field.name  = "link_codigo";
                    field.value = s.link.codigo;
                form.appendChild(field);
                
                
            } else if(s.link) { // vinculo padrao
                
                var field = document.createElement("input");
                    field.type  = "hidden";
                    field.name  = "link";
                    field.value = s.link;
                form.appendChild(field); 
            }
            
            
            // document.querySelector("body").appendChild(form);   // adiciona formulario ao documento
            var t = document.querySelector("#CAD");   // adiciona formulario ao documento
                t.appendChild(form);
                t.method  = "POST";
                t.enctype = "multipart/form-data";
                t.target  = "uploadframe_"+uuid;
                t.action  = "/sys/upload/DUpload.cgi?X-Progress-ID="+uuid;
                t.submit();
                
                // limpa form property apos submeter
                t.appendChild(form);
                t.method  = "";
                t.enctype = "";
                t.target  = "";
                t.action  = "";                
        }	
        
        
    	/**
         *   Return
         *       retorna objeto pronto
         */
    	return this.each(function() {
            
            if(s.link){
                if(!s.link.codigo){
                    console.log("DUpload - erro: settings.link com problema");
                    return false;
                }
            }
            
            
            /* prepara o campo upload */
            var name = $(this).prop("name")
            ,   id   = $(this).prop("id")
            ,   gid  = eos.core.genId();
            
            /* id and name 
            if(!name) {
                name = "DUpload_file_"+gid;
            } else if(!id) {
                id = "DUpload_file_"+gid;
            } else {
                id = "DUpload_file_"+gid;
                name = "DUpload_file_"+gid;
            }
            */
            /* id and name
            if(!id || !name) { 
                if(id) {
                    id   = id;
                    name = id;
                } else {
                    id   = name;
                    name = name;
                }
            } else {
                id = "DUpload_file_"+gid;
                name = "DUpload_file_"+gid;
            }
            */
            
            /* field upload */
            var fieldupload = $("<input />");
                fieldupload
                    .prop({
                        type     : "file",
                        name     : name,
                        id       : id,
                        multiple : s.multiple
                    })
                    .css({
                        opacity : 0
                    })

            
            /* container */
            var container = $("<div class='EOS_template_field EOS_template_field_file' id='"+ eos.core.genId() +"' style='background:#red;'></div>");
                container.append("<input type='text' placeholder='"+s.placeholder+"' />");
                container.append(fieldupload);
                container.append("<div class='EOS_template_field_file_upload'></div>");
                container.append("<div class='EOS_template_field_file_name'></div>");
                container.append("<div class='EOS_template_field_file_progress'><div class='EOS_template_field_file_progress_descrp'></div><div class='EOS_template_field_file_progress_bar'></div></div>");
                
            $(this)
                .after(container)
                .remove();
            
            /* objeto finalizado */       
            s.obj    = fieldupload;
            s.obj_id = fieldupload.prop("id");
            fieldupload.data("DUploadSettings", s); // adiciona em low level data of object
            var ftext = s.obj.parent().find("input[type=text]");
            
            /* aciona uploader no click */
            container.find(".EOS_template_field_file_upload").click(function(){
                $(this).parent().find("input[type=file]").trigger("click");
            });
            
            /* expande name ao clicar */  
            container.find(".EOS_template_field_file_name").click(function(){
                $(this).toggleClass("EOS_template_field_file_name_open");
            });
            
            /* expande progress ao clicar */  
            container.find(".EOS_template_field_file_progress").click(function(){
                $(this).toggleClass("EOS_template_field_file_progress_open");
            });
            
            /* campo descrp vazio abre o uploader quando focus in */
            ftext
                .focus(function(x){
                    if(!$(this).val()) {
                        $(this).parent().find("input[type=file]").trigger("click");
                    }
                });
            
            /* arquivo escolhido */
            s.obj.change(function(){                
                var f    = $(this)[0].files.item(0)    // file 
                ,   mime 
                ,   type;
                                
                /* mime type ajust */
                if(f.type.lc().search("pdf") > -1) {                    // PDF
                    type = "EOS_template_field_file_mimetype_pdf";
                    mime = "pdf";
                } else if(f.type.lc().search("video") > -1) {           // video
                    type = "EOS_template_field_file_mimetype_video";
                    mime = "video";
                } else if(f.type.lc().search("audio") > -1) {           // audio 
                    type = "EOS_template_field_file_mimetype_audio";
                    mime = "audio";
                } else if(f.type.lc().search("image") > -1) {           // image
                    type = "EOS_template_field_file_mimetype_image";
                    mime = "image";
                } else if(f.type.lc().search("text") > -1) {            // text
                    type = "EOS_template_field_file_mimetype_text";
                    mime = "text";
                } else if(f.type.lc().search("zip") > -1) {             // Zip
                    type = "EOS_template_field_file_mimetype_zip";
                    mime = "zip";
                } else if(f.type.lc().search("office") > -1 && f.type.lc().search("spreadsheet") > -1) { // excel
                    type = "EOS_template_field_file_mimetype_excel";
                    mime = "excel";
                } else if(f.type.lc().search("office") > -1 && f.type.lc().search("word") > -1) {        // word
                    type = "EOS_template_field_file_mimetype_word";
                    mime = "word";
                } else if(f.type.lc().search("postscript") > -1) {      // vector
                    type = "EOS_template_field_file_mimetype_vector";
                    mime = "vector";
                } else if(f.type.lc().search("photoshop") > -1) {       // photoshop
                    type = "EOS_template_field_file_mimetype_photoshop";
                    mime = "image";
                } else {
                    type = "EOS_template_field_file_mimetype_defaut";   // default
                    mime = "";
                }
                
                /* teste mime type se existir */
                if(s.mimetype && s.mimetype.indexOf(mime) !== 0) {
                    
                    var allowed = ""; 
                    s.mimetype.forEach(function(i){ 
                        allowed += i+","
                    });
                    allowed = allowed.replace(/\,$/,'');
                    
                    $.DDialog({
                        type    : "alert",
                        message : "Tipo de arquivo não permitido ("+f.name+") <br><br> tipos permitidos ("+allowed+")"
                    });
                    
                    return false;
                }
                
                
                /* testa controle de disco */
                if(s.disk && eos.disk.verify(f.size) !== true) {
                    var msg   = ""
                    ,   space = eos.disk.verify(f.size);
                    
                    if(space === false) {
                        msg = "Espaço esgotado ";
                    } else {
                        msg = "Espaço insuficiente. <br><br> Disponível <b>"+eos.core.math.toMB(space)+"MB</b>";
                    }
                    
                    $.DDialog({
                        type    : "alert",
                        message : msg
                    });
                    
                    return false;
                }
                
                /* sugestao de nome */
                var n = f.name;
                    n = n.match(/([^\/]+)(?=\.\w+$)/)[0];
                    n = n.replace(/(\/|\_|\-|\:|\,|\.|\(|\)|\ )/g,' ');
                
                /* remove mimetype icon add new and name suggestion */
                    // ftext[0].className = ftext[0].className.replace(/(EOS_template_field_file_mimetype(\w+))/g, '');
                    ftext
                        .removeClass()
                        .addClass(type)
                        .val(n);
                
                /* nome real mostra na div do nome */
                $(this).parent().find(".EOS_template_field_file_name")
                    .addClass("EOS_template_field_file_name_populated")
                    .text(f.name+" | "+f.type);
                    
                /* mostra tamanho do arquivo na barra de progresso */
                $(this).parent().find(".EOS_template_field_file_progress")
                    .addClass("EOS_template_field_file_progress_populated");
                    
                /* mostra tamanho do arquivo na barra de progresso */    
                $(this).parent().find(".EOS_template_field_file_progress_descrp")
                    .text(eos.core.math.toMB({value:f.size, decimal:2})+"MB");
                    
                    
                /* Upload automatico */
                if(s.automatic) {
                    upload(s.obj);
                }
                
            });
            
            
            
    	});
    };
    
})( jQuery );


