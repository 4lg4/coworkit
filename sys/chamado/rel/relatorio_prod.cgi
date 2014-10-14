#!/usr/bin/perl

$nacess = "40";
require "../../cfg/init.pl";

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script type="text/javascript">

/*
*   Relatorio
*       objeto com todas as funcionalidades
*/    
function Relatorio() {
        
	// gerar relatorio do chamado
	this.rel = function(){
		// testa antes de gerar
		if(\$("#filter_period").DTouchRadio("DTouchRadioGetValue") == "") {
			alerta("Período deve ser definido");
			return false;
		}

		// executa download
        eos.DAction.ajax({
			action : "relatorio_prod.xls"
		});
	}
};


/*
*   Form
*       Objeto formulario 
*/
function Form() {
    // inicializa formulario
    this.initialize = function() {
		// boxes
		\$("#chamado_rel_periodo").DTouchBoxes({title:"Período"});
		\$("#chamado_rel_cliente").DTouchBoxes({title:"Cliente"});
		\$("#chamado_rel_tecnico").DTouchBoxes({title:"Técnicos"});
		
		
		/* periodo radio */
		var period_inputs  = '<div id="filter_period_dates_container" style="display:none;">';
			period_inputs += '	<div class="filter_period_dates"><input type="text" name="filter_period_ini" id="filter_period_ini"></div>';
			period_inputs += '	<div><input type="text" name="filter_period_end" id="filter_period_end"></div>';
			period_inputs += '</div>';
			
		\$("#filter_period").DTouchRadio({
			// type: "accordion",
			orientation: "vertical",
            visibleItems : 4,
            uncheck : false,
			addItem:[
				{
                    val:"week",
                    descrp:'Semana atual'
                },
				{
                    val:"past_month",
                    descrp:'Mês anterior'},
				{
                    val:"this_month",
                    descrp:'Mês atual'
                },
				{
                    val:"period",
                    descrp:'Período '+period_inputs }
			],
            postFunction : function(x){ 

                // cria campos date
   			    \$("#filter_period_ini").fieldDateTime({ 
                    type:"date" 
                });
   			    \$("#filter_period_end").fieldDateTime({ 
                    type:"date" 
                });
                
            },
			click : function(x){ 
        		// esconde campos de filtro por periodo
        		\$("#filter_period_dates_container").hide();
		
        		// busca por periodo
        		if(x.value === "period") {
        			\$("#filter_period_dates_container").show();
        		}
			}
            /* ,
            uncheck : function(){

        		// esconde campos de filtro por periodo
        		\$("#filter_period_dates_container").hide();
                
            } */
		});

        /* cliente radio */
		var cliente_inputs  = '<div id="filter_cliente_container">';
			cliente_inputs += '		<input type="text" name="cliente" id="cliente"> ';
			cliente_inputs += '</div>';
		
		\$("#filter_cliente").DTouchRadio({
			orientation: "vertical",
            uncheck : true,
			addItem:[
				{ val : "mensalista", descrp : 'Todos Mensalistas'},
				{ val : "avulso",     descrp : 'Todos Avulsos'},
				{ val : "especifico", descrp : 'Específico '+cliente_inputs }
			],
            postFunction : function(x){ 

                // cria campos date
    			\$("#cliente").fieldAutoComplete({ 
    				type           : "empresa",
    				createFunction : function(x) { // console.log(x);
    					\$("#cliente_descrp").focus();
    				}
    			});
                // \$("#cliente").fieldAutoComplete("hide");
                \$("#filter_cliente_container").hide();
            
            },
			click : function(x){ 
        		// esconde campos de filtro por periodo
                \$("#filter_cliente_container").hide();
                
        		// busca por periodo
        		if(x.value === "especifico") {
                    \$("#filter_cliente_container").show();
                    \$("#cliente_descrp").focus();
        		}
                
			}
            /* ,
            uncheck : function(){

        		// esconde campos de filtro por periodo
        		\$("#filter_cliente_container").hide();
            
            } */
		});


		// tecnicos
        /*
		\$("#filter_tecnico").DTouchRadio({
			table : "usuario_tecnico",
            visibleItems : 3
		});
        */
        
        // inicializa menu
        this.menu.initialize();
    },
    
    // reset
	/* zera formulario */
	this.reset = function() {
		\$("#filter_period_dates_container, #filter_cliente_container").hide();
		\$("#cliente, #cliente_descrp, .filter_period_dates").val("");
		\$("#filter_tipo").DTouchRadio("DTouchRadioReset");
		\$("#filter_cliente").DTouchRadio("DTouchRadioReset");
		\$("#filter_period").DTouchRadio("DTouchRadioReset");
	},
        
    /* menu */
    this.menu = {
        initialize : function(){
    		menu_chamado_rel = new menu();
    		// menu_chamado_rel.btnNew("icon_chamado_rel_gerar_pdf","gerar","chamadoRelGerar()","pdf");
    		menu_chamado_rel.btnNew("icon_chamado_rel_gerar_excel","gerar","chamadoRelGerar(1)","excel");
    		menu_chamado_rel.btnNew("icon_chamado_rel_limpar","limpar","formularioReset()","form.");
            
            
            /*
            *   icones edicao
            */
            eos.menu.action.new({ // encaminhar
                id       : "icon_chamado_rel_gerar_excel",
                title    : "gerar",
                subtitle : "excel",
                click    : function(){
                    tktrel.rel();
                }
            });
            eos.menu.action.new({ // encaminhar
                id       : "icon_chamado_rel_gerar_excel",
                title    : "gerar",
                subtitle : "excel",
                click    : function(){
                    tktrel.rel();
                }
            });
        }
    }
};


/*
*   Document Ready
*/
\$(document).ready(function() { 
    form = new Form();
    form.initialize();
    
    tktrel = new Relatorio();
});


</script>
</head>
<body>

<!-- main form -->
<form>

    <!-- full container -->
    <div id="CAD_full_container">
        
        <!-- left container -->
        <div id="left_container">
            <!-- periodos pre determinados -->
    		<div id="chamado_rel_periodo">
    			<div id="filter_period"></div>
    		</div>
        
            <!-- tipos de cliente -->
    		<div id="chamado_rel_cliente">
    			<div id="filter_cliente"></div>
    		</div>
        </div>
    
        <!-- right container -->
        <div  id="right_container">
            <!-- tecnicos -->
    		<div id="chamado_rel_tecnico" style="display:none;">
    			<div id="filter_tecnico"></div>
    		</div>
    	</div>
        
    </div>
    	
</form>

<!-- Templates -->
<div class="eos_template_chamado_relatorio_prod" style="display:none;">
    <input />
</div>


</body>
</html>
HTML












