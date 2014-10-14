/* [INI]  DATE / TIME field (by akgleal.com)  ------------------------------------------------------------------------- 
	Dependencias:
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.meiomask.js"></script> (arquivo modificado por akgleal.com)
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.ui.datepicker-pt-BR.js"></script>
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.ui.timepicker.js"></script>

	CSS necessarios
	.fieldDate { field_date.png }
	.fieldDateTime { field_datetime.png }
	.fieldTime { field_time.png }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:
	just_date_time = "date" => dd/mm/YYYY 
	just_date_time = "date-time" => dd/mm/YYYY hh:mm
	just_date_time = "time" => hh:mm
	fast = 0 / 1
	
	Exemplo de uso:
	var data = new fieldDateTime("campo_data",just_date_time,fast);
	<input type="text" id='campo_data_completa' name='campo_data_completa' alt="date-time">
*/

// dependencias
include("/comum/DPAC_syscall/jquery/jquery.ui.datepicker-pt-BR.js"); 
// include("/comum/DPAC_syscall/jquery/date-pt-BR.js");
include("/comum/DPAC_syscall/jquery/jquery.ui.timepicker.js"); 

function y2k(number) { return (number < 1000) ? number + 1900 : number; }
 
function fieldDateTime(field,just_date_time,fast) 
	{
	// seta variaveis iniciais
	var onCloseFunctionVar = ""; 
	
	// retorno automatico ativado
	if(!fast)
		{
		fast = 1;
		icon = "";
		}
	else
		{
		if(fast == "icon")
			{
			var icon = 1; // ativa icone
			fast = 0; // seta variavel para nao terminar
			}
		}
	
	this.onCloseFunction = function(x) { onCloseFunctionVar = x; }
				
	// se nao for setado opt ou for errado ajusta para padrao
	if(!just_date_time) //  != "date" || just_date_time != "date-time" || just_date_time != "time")
		just_date_time = "date";
		
	// cria campo
	this.show = function()
		{
		switch(just_date_time)
			{
			case "date":
				$('#'+field).datepicker(
					{
					// showOn: "button",
					// buttonImage: "/img/calendar.png",
					buttonImageOnly: true,
					showButtonPanel:  true
					})
				.addClass("fieldDate");
			break;
			case "date-time":
				$('#'+field).datetimepicker(
					{
					hourGrid: 4,
					minuteGrid: 15,
					// showOn: "button",
					// buttonImage: "/img/calendar.png",
					buttonImageOnly: false,
					showButtonPanel:  true
					})
				.addClass("fieldDateTime");				
			break;
			case "time":
				$('#'+field).timepicker(
					{
					hourGrid: 4,
					minuteGrid: 15,
					// showOn: "button",
					// buttonImage: "/img/calendar.png",
					buttonImageOnly: false,
					showButtonPanel:  true
					})
				.addClass("fieldTime");
			break;
			case "month-year":
				$('#'+field).datepicker(
					{ 
					changeMonth: true,
					changeYear: true,
			        showButtonPanel: true,
			        dateFormat: 'mm/yy',
			        onClose: function(dateText, inst) 
						{ 
						var month = $("#ui-datepicker-div .ui-datepicker-month :selected").val();
						var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
						$(this).datepicker('setDate', new Date(year, month, 1));
						
						// remove css que esconde calendario dos dias
						// setTimeout(function(){$('#'+field+"_style").remove();},300);
						$('#'+field+"_style").delay(500).queue(function(){ $(this).remove() });
						// $('#'+field+"_style").remove();
						
						// alert($(this).val());
						eval(onCloseFunctionVar);
						},
			        beforeShow: function(input, inst) 
						{
						var tmp = $(this).val().split('/');
						$(this).datepicker('option','defaultDate',new Date(tmp[1],tmp[0]-1,1));
						$(this).datepicker('setDate', new Date(tmp[1], tmp[0]-1, 1));
						
						// esconde calendario dos dias
						$("body").append("<style id='"+field+"_style'>.ui-datepicker-calendar{display:none;}</style>")
						}
					})
				.addClass("fieldMonthYear");
				
				// remove campo e adiciona icone com link
				if(icon)
					{
					$('#'+field).datepicker("option", "showOn", "button");
					$('#'+field).datepicker("option", "buttonImage", "/img/comum/field_date.png");
					$('#'+field).datepicker("option", "buttonImageOnly", true);
					$('#'+field).removeClass("fieldMonthYear").addClass("fieldMonthYearIcon").attr("readonly",true);
					}

			break;
			}
			
		// ajusta atributos e inicia mascaramento
		$('#'+field).attr({'alt':just_date_time, 'autocomplete':'off'}).setMask(); 
		
		// debugar problema com datas invalidas 31/08/2012   /  10-23/12/2013
		// se NAO for campo time somente data controla entrada
		if(just_date_time == "date" || just_date_time == "date-time")
			{	
			$('#'+field).change(function() 
				{
		        var f = $(this).val();
				f = f.replace(/\//g,''); // remove barras
				f = f.replace(/:/g,''); // remove dois pontos
				
				if(f.length < 8 && f.length > 0)
					{
					top.erro("<nobr>Data Errada 2 !!</nobr>",$(this).attr('id'));
					}
				else
					{
					year = f.substr(4,4);
					month = f.substr(2,2);
					day = f.substr(0,2);
				    
				    //alert(year+'-'+month+'-'+day);
				    month= month-1;
				    var test = new Date(year,month,day);
				    //alert(test);
				    if ( (y2k(test.getYear()) == year) && (month == test.getMonth()) && (day == test.getDate()) )
						a = "ok";
				    else
							top.erro("<nobr>Data Errada !!</nobr>",$(this).attr('id'));
					}
				
				});
			}
			
		// remove campo e adiciona icone com link
		if(icon)
			{
			$('#'+field).datepicker("option", "showOn", "button");
			$('#'+field).datepicker("option", "buttonImage", "/img/comum/field_date.png");
			$('#'+field).datepicker("option", "buttonImageOnly", true);
			}
		}
		
	// desabilita campo
	this.disable = function(v)
		{
		$('#'+field).datepicker("disable");
		fieldOptDisable(field);
		
		// esconde campo
		if(v)
			fieldOptHide(field);
		}
		
	// habilita campo
	this.enable = function()
		{
		$('#'+field).datepicker("enable");
		fieldOptEnable(field);
		
		// mostra campo
		fieldOptShow(field);
		}
	
	// remove campo e adiciona icone com link
	this.justicon = function()
		{
		$('#'+field).css("display", "none");
		}
	
	
	
	// quando sai do campo executa funcao
	this.blur = function(func){ fieldOptBlur(field,func); };
		
	// retorna campo pronto
	if(fast == 1)
		return this.show();
	}
/* [END]  DATE / TIME field (by akgleal.com)  ------------------------------------------------------------------------- */
