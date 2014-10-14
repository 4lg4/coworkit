/* [INI]  DATE / TIME field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
		Javascript
			/comum/jquery/jquery.meiomask.js (loaded on DPAC)
			/comum/jquery/jquery.ui.datepicker-pt-BR.js
			/comum/jquery/jquery.ui.timepicker.js

		CSS
			/css/ui.css
				.fieldDate { field_date.png }
				.fieldDateTime { field_datetime.png }
				.fieldTime { field_time.png }
				.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
		Enable / Disable
		Auto Complete
		Type
		Icon
		Just Icon
			
	Exemplo de uso:
		Javascript
			$("#campo_DateTime").fieldNumber();
			$(".campo_DateTime").fieldNumber();
			
			$("#campo_DateTime").fieldNumber(
				{
				options:values
				});
	
		HTML
			<input type="text" id='campo_data_completa' name='campo_data_completa'>
*/

// dependencias
include("/comum/jquery/jquery.ui.datepicker-pt-BR.js"); 
include("/comum/jquery-ui-timepicker/jquery-ui-timepicker-addon.min.js"); 
// include("/comum/jquery/jquery.ui.timepicker.js"); 

// support for multiple picker
// http://multidatespickr.sourceforge.net/
// include("/comum/multiple-dates/jquery-ui.multidatespicker.js"); 


(function($){

$.fn.fieldDateTime = function(settings,value)
	{
	// se for um array ou estiver vazio ajusta variaveis
	if(isObject(settings) === true)
		{
		var settings = $.extend(
			{
			autocomplete	: 'on',
			enable			: 'on',
			icon			: 'off', // aparece o icone
			justicon		: 'off', // mostra somente o icone
			type			: 'date',
			postFunction	: '', // funcao para executar apos escolha da data
			value			: '',
			allowEmpty		: true, // aceita campo vazio
			// opcoes
			fieldDateTimeValueMonthYear	: '',
			fieldDateTimeValueDate	: '',
			fieldDateTimeValueTime	: '',
			fieldDateTimeGetValue	: '',
			}, settings);
			
		// salva opcoes setadas do objeto para uso futuro
		$(this).data("fieldDateTimeSettings", settings);
		}
	else
		{
		switch(settings)
			{			
			// fieldDateTimeGetValue: pega valor do campo para uso ex. (YYYY-MM-DD HH:MM:SS) ------------------
			case "GetValue":
			case "getvalue":
			case "value":
			case "val":
			case "fieldDateTimeGetValue":
			
                // se nao for objeto retorna valor vazio
                if(!$(this).data("fieldDateTimeSettings")){
                    return "";
                }
            
				// retorna valor conforme tipo do campo
				switch($(this).data("fieldDateTimeSettings")["type"])
					{
					// Data, somente
					case "date":
                        if(value){
                            $(this).datepicker('setDate', new Date(value+"T13:00"));
                            fieldDateTimeTest($(this));
                            return true;
                        } else {
						    return $(this).data("fieldDateTimeSettings")["fieldDateTimeValueDate"];
                        }
					break;
					
					// Tempo, somente
					case "time":
                        if(value){ 
                            $(this).datetimepicker('setDate', new Date("2013-01-01T"+value));
                            return true;
                        } else {
						    // return $(this).data("fieldDateTimeSettings")["fieldDateTimeValueTime"];
                            return $(this).val();
                        }
					break;
					
					// Data e Tempo
					case "date-time":
						// return $(this).data("fieldDateTimeSettings")["fieldDateTimeValueDate"]+" "+$(this).data("fieldDateTimeSettings")["fieldDateTimeValueTime"];
                        // return $(this).data("fieldDateTimeSettings")["fieldDateTimeValueDate"]+" "+$(this).data("fieldDateTimeSettings")["fieldDateTimeValueTime"];
                        if(value){
                            $(this).datetimepicker('setDate', new Date(value));
                        } else {
						    // return $(this).data("fieldDateTimeSettings")["fieldDateTimeValueTime"];
                            return $(this).val();
                        }
					break;
					
					// Data e Tempo
					case "month-year":
                    case "year-month":
                        if(value){  // console.log(value+"T00:00:00"); erro de preenchimento de campo ???
                            $(this).datepicker('setDate', new Date(value+"T13:00:00"));
                        } else {
                            return $(this).val();
                        }
					break;
					}
			break;
            
            // habilita campo para uso 
            case "enable" :
                eos.template.field.unlock($(this));
                $(this)
                    .datepicker("enable")
                    .prop("readonly",false);
                return true;
            break;
            
            // desabilita
            case "disable" :
                eos.template.field.lock($(this));
                $(this)
                    .datepicker("disable")
                    .prop({
                        readonly:true,
                        disabled:false
                    });
                return true;
            break;
            
            // somente leitura
            case "readonly" :
                eos.template.field.readonly($(this));
                $(this)
                    .datepicker("disable")
                    .prop({
                        readonly:true,
                        disabled:false
                    });
                return true;
            break;
            
            // reset
            case "reset" :
                $(this).val("");
                return true;
            break;
			}
		}
	
	
	// retorno do campo
	return this.each(function() { 
        $(this).addClass('DFields'); // adiciona identificador para campos EOS DFields
        
		switch(settings.type.lc()) {
            
			/* Date  */
			case "date":				
				// se for dispositivos moveis
				if(isTablet() === true || isMobile() === true) {
					fieldDateTimeMobilize($(this));	
				} else {
					$(this)
						.datepicker(
							{
							buttonImageOnly: true,
							showButtonPanel:  true,
							onSelect: function(date)
								{
								fieldDateTimeTest($(this));
								}
							});
                            
                        eos.template.field.date($(this)); // mostra na tela
						// .addClass("fieldDate");
				}
			break;
			
			// Date and Time   ---------------------------------------------------------------------------------
			case "date-time":
				// se for dispositivos moveis
				if(isTablet() === true || isMobile() === true) {
					fieldDateTimeMobilize($(this));
				} else {
					$(this)
						.datetimepicker(
							{
							hourGrid: 4,
							minuteGrid: 15,
							buttonImageOnly: false,
							showButtonPanel:  true,
							onSelect: function(date)
								{
								fieldDateTimeTest($(this));
								}
							});
                            
                    eos.template.field.datetime($(this)); // mostra na tela
                }		
			break;
			
			// Time
            case "time-hour":
			case "time":
				// se for dispositivos moveis
				if(isTablet() === true || isMobile() === true) {
					fieldDateTimeMobilize($(this));
				} else {
                    
                    
                    if(settings.type.lc() === "time-hour") {
                        var minute = false;
                    } else {
                        var minute = true;
                    }
                        
					$(this)
                        .timepicker({
                            hourMax    : 99,
                            minuteGrid : 15,
                            stepMinute : 15,
    						minuteGrid : 15,
    						buttonImageOnly : false,
    						showButtonPanel :  true,
                            showMinute      : minute,
                            hourText        : "Horas",
                            minuteText      : "Minutos",
                            timeOnlyTitle   : "Escolha o Tempo",
                            timeText        : "Tempo",
                            currentText     : "agora",
                            closeText       : "fechar",
    						onClose: function(date) { 
    							// executa postFunction se for funcao
    							if(isFunction(settings.postFunction)) {
    								settings.postFunction.call(this,date);
                                }
    						}
    					})
                        .prop({
                            placeholder : settings.placeholder
                        });
                    
                    // remove botao NOW
                    // $(".ui-datepicker-current").remove();
                    
					// .addClass("fieldTime");
                    eos.template.field.time($(this)); // mostra na tela
				}
			break;
			
			// Month and Year   -------------------------------------------------------------------------------
			case "month-year":
            case "year-month":
				$(this).datepicker({ 
					changeMonth: true,
					changeYear: true,
			        showButtonPanel: true,
					/*
					showOn: "both",
					buttonImageOnly: true,
					buttonImage: "/img/field/field_date.png",
					*/
			        dateFormat: 'mm/yy',
			        onClose: function(dateText, inst) 
						{ 
						var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
						var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
						$(this).datepicker('setDate', new Date(year, month, 1));
						
						// remove css que esconde calendario dos dias
						// setTimeout(function(){$('#'+field+"_style").remove();},300);
						$("#"+$(this).attr("id")+"_style").delay(500).queue(function(){ $(this).remove() });
						// $('#'+field+"_style").remove();
						
						fieldDateTimeTest($(this));
						},
			        beforeShow: function(input, inst) 
						{
						var tmp = $(this).val().split('/');
						$(this).datepicker('option','defaultDate',new Date(tmp[1],tmp[0]-1,1));
						$(this).datepicker('setDate', new Date(tmp[1], tmp[0]-1, 1));
						
						// esconde calendario dos dias
						$("body").append("<style id='"+$(this).prop("id")+"_style'>.ui-datepicker-calendar{display:none;}</style>")
						}
				});
				// .addClass("fieldMonthYear");
                eos.template.field.datetime($(this)); // mostra na tela

			break;
			
			// Calendar / Calendario completo   -------------------------------------------------------------
			case "calendar":

				$(this).datepicker();

			break;	
		}
			
		// remove campo e adiciona icone com link
		if(settings.icon == "on")
			{
			$(this).datepicker("option", "showOn", "button");
			$(this).datepicker("option", "buttonImage", "/img/comum/field_date.png");
			$(this).datepicker("option", "buttonImageOnly", true);
			$(this).removeClass("fieldMonthYear").addClass("fieldMonthYearIcon").attr("readonly",true);
			}
			
			
		// remove campo e adiciona icone com link
		if(settings.justicon == "on")
			{
			$(this).css("display", "none");
			}

		// ajusta o opcoes do campo 
		$(this)
			.prop(
				{
				'maxlength'		: settings.maxlength,
				'autocomplete'	: settings.autocomplete,
				'enable'		: settings.enable,
				'alt':settings.type 
				})
			.setMask()
			.keydown(function(e)
				{
				// ajusta comportamento do tab como enter 
				if(e.which == 9)
					{
					e.preventDefault();
					e.which = 13;
					$(this).trigger(e);
					}
				else if(e.which == 13)
					{
					// se for data testa conteudo
					// if(settings.type == "date" || settings.type == "date-time")
						if(($(this).val() != "" && settings.allowEmpty !== true) && (settings.type == "date" || settings.type == "date-time"))
							fieldDateTimeTest($(this));
						
					// esconde date picker	
					$(this).datepicker("hide");

					// pula campo
					$(this).next().focus();
					}
				}); 
				
		// seta valor inicial se existir
		if(settings.value != "")
			$(this).data("fieldDateTimeSettings")["fieldDateTimeValueDate"] = settings.value;
		});

	};

})( jQuery );



// funcoes para teste de data
function fieldDateTimeTest(obj)
	{
	var settings = obj.data("fieldDateTimeSettings"); // acesso as configuracoes atuais do objeto
	
	// console.log(obj);
	// alert(obj.val());
	
	// var f = obj.val();
	var f = obj.val().replace(/(\/|\-|\:|\ )/g,'');
	
	/*
	f = f.replace(/\//g,''); // remove barras
	f = f.replace(/:/g,''); // remove dois pontos
	f = f.replace(/ /g,''); // remove espacos
	*/
	
	if(f.length == 6) // year-month (ano/mes)
		{
		var year = f.substr(2,4);
		var month = f.substr(0,2);
		
		// seta valor data
		obj.data("fieldDateTimeSettings")["fieldDateTimeValueMonthYear"] = year+"-"+month;
        obj.data("fieldDateTimeSettings")["value"] = year+"-"+month;
		
		// executa postFunction se for funcao
		if(isFunction(settings.postFunction) === true)
			settings.postFunction.call(this,obj.data("fieldDateTimeSettings")["value"]);
		}
	else if(f.length < 8 && f.length > 0)
		{
		top.alerta("<nobr>Data Errada !!</nobr>","top.fieldFocus('"+obj.attr('id')+"')");
		}
	else
		{
		var year = f.substr(4,4);
		var month = f.substr(2,2);
		var month2 = month-1; // comparacao
		var day = f.substr(0,2);
		var hour = f.substr(5,2);
		var minute = f.substr(7,2);

	    var test = new Date(year,month2,day);
		var y2k = (test.getYear() < 1000) ? test.getYear() + 1900 : test.getYear(); // ajusta o ano
	   
	    if((y2k == year) && (month2 == test.getMonth()) && (day == test.getDate()) )
			{
			// seta valor data
			obj.data("fieldDateTimeSettings")["fieldDateTimeValueDate"] = year+"-"+month+"-"+day;
			
			// seta valor hora
			obj.data("fieldDateTimeSettings")["fieldDateTimeValueTime"] = hour+":"+minute+":00";
			
            
            obj.data("fieldDateTimeSettings")["value"] = year+"-"+month+"-"+day+" "+hour+":"+minute+":00";
            
			// executa postFunction se for funcao
			if(isFunction(settings.postFunction) === true)
				settings.postFunction.call(this,obj.data("fieldDateTimeSettings")["value"]);
			}
	    else
			top.alerta("<nobr>Data Errada !!</nobr>","top.fieldFocus('"+obj.attr('id')+"')");
		}
	}

// ajusta para dispositivos mobile
function fieldDateTimeMobilize(obj) {
    
	var settings = obj.data("fieldDateTimeSettings"); // acesso as configuracoes atuais do objeto
    var f, change, type;
    
    if(settings.type === "date-time") {
        type = "datetime-local";
        change = "datetime";
    } else {
        type = settings.type;
        change = "time";
    }        
    
	obj.replaceWith(function() {
        return $("<input type='"+type+"' id='"+obj.attr("id")+"' name='"+obj.attr("id")+"' value='"+obj.val()+"' />").append(obj.contents());
    });
    

    eos.template.field[change]($("#"+obj.attr("id")));    
}
	
	
