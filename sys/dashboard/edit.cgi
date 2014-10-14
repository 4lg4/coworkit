#!/usr/bin/perl

$nacess = "";
# $nacess_more = "or menu = 74";
# $nacess[0] = "2";
# $nacess[1] = "74";
require "../cfg/init.pl";
$ID = &get('ID');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	
<script language='JavaScript'>
/**
 *   dashboard
 *       obj dashboard
 */
function Dashboard(){
    var d = this;
    
    
    /* initialize */
    this.initialize = function() {
        
        this.widget.hide();
        
        \$.DActionAjax({
            action : "control.cgi",
            postFunction : function(x) {                
                try {
                    var w = JSON.parse(x);
                    if(w.status === "success"){
                        w.widgets.forEach(function(i) {
                            dashboard.widget[i].initialize();
                        });
                    }
                } catch(e){ 
                    console.log(e);
                }
            }
        });
    }
    
    this.widget = { 
        
        /* esconde tudo */
        hide : function() {
            \$(".widget").hide();
        },
               
        /* quotes */
        quotes : {
            
            /* initialize */
            initialize : function(){
                \$("#quote").show();
                \$("#quote").DTouchBoxes({ type:"bar" });
                
                this.load();
            },
            
            /* carrega */
            load : function(){
                
                // cache in quote se nao existir
                if(!cacheQuote) { 
                	\$.DActionAjax({
                		action : "quotes.cgi",
                		loader : \$("#quote"),
                        postFunction : function(x){
                            cacheQuote = JSON.parse(x);
                            
                            \$("#quote_descrp").text('"'+cacheQuote.descrp+'"');
                            \$("#quote_autor").text(cacheQuote.autor);
                        }
                	});   
                } else {
                    \$("#quote_descrp").text('"'+cacheQuote.descrp+'"');
                    \$("#quote_autor").text(cacheQuote.autor);
                }
            }
            
        },
        
        /* chamados */
        tkt : {
            
            /* initialize */
            initialize : function(){
                this.load(true);
            },
            
            /* carrega */
            load : function(ini){
            	\$.DActionAjax({
            		action: "chamado.cgi",
            		loader: \$("#dashboard_tkt_container"),
                    postFunction : function() {
                        
                        \$("#dashboard_tkt_container").show();
                        
                        if(ini) {
                            \$("#dashboard_tkt_container").DTouchBoxes({ title:"Service Desk" });
                        }
                    }
            	});    
            }
        
        },
        
        
        
        /* feedback */
        feedback : {
            
            /* initialize */
            initialize : function(){
                this.load(true);
            },
            
            /* carrega */
            load : function(ini){
            	\$.DActionAjax({
            		action: "feedback.cgi",
            		loader: \$("#feedback_container"),
                    postFunction : function() {
                        
                        \$("#feedback_container").show();
                        
                        if(ini) {
                            \$("#feedback_container").DTouchBoxes({ title:"Avalie nosso atendimento" });
                        }
                    }
            	});    
            }
        
        },
        
        
        
        /** 
         *  estatisticas cliente 
         */
        customer_status : {
            
            /* initialize */
            initialize : function(){
                this.load("INI");
            },
            
            /* carrega */
            load : function(x){
                var ini = false;
                
                if(!x){
                    x = '';
                } else if(x === "INI"){
                    x = '';
                    ini = true;
                }
            	\$.DActionAjax({
            	    action : "estatisticas.cgi",
            	    loader : \$("#status_container"),
                    req    : "periodo="+x,
                    postFunction : function() {
                        
                        \$("#status_container").show();
                        
                        if(ini) { 
                            \$("#status_container").DTouchBoxes({ title : "Estatísticas" });
                            \$("#customer_status_container").DTouchBoxes();
                        }
                    }
            	});   
            }
            
        },
        
        /** 
         *  estatisticas tecnicos
         */
        tec_status : {
            
            /* initialize 
            initialize : function(){
                \$("#status_container").DTouchBoxes({ title : "Estatísticas" });
                \$("#customer_status_container").DTouchBoxes();
                
                this.load();
            },
            */
            
            /* carrega */
            load : function(){
                
            	\$.DActionAjax({
            		action : "estatisticas_tecnicos.cgi",
            		loader : \$("#status_container")
            	});   
            }
            
        },
        
        /* empresas */
        empresas : {
            
            /* initialize */
            initialize : function(){
                \$("#empresas_container").show();
                \$("#empresas_container").DTouchBoxes({ title:"Empresas TOP 10" });
                
                this.load();
            },
            
            /* carrega */
            load : function(){
            	\$.DActionAjax({
            		action: "empresas.cgi",
            		loader: \$("#empresas_container")
            	});    
            }
        
        },
        
        
        /* orcamentos */
        orc : {
            
            /* initialize */
            initialize : function(){
                this.load(true);
            },
            
            /* carrega */
            load : function(ini){
            	\$.DActionAjax({
            		action: "orcamento.cgi",
            		loader: \$("#dashboard_orc_container"),
                    postFunction : function() {
                        
                        \$("#dashboard_orc_container").show();
                        
                        if(ini) {
                            \$("#dashboard_orc_container").DTouchBoxes({ title:"Orçamentos / Pedidos / O.S." });
                        }
                    }
            	});    
            }
        
        }
    }
}


/**
 *   Form
 *       obj formulario
 */
function Form(){
    /* initialize */
    this.initialize = function(){
		\$("#dashboard_page").DTouchPages({
            // pageChange: "center",
            pageCenter : \$("#dashboard_page_center"),
            pageRight  : \$("#dashboard_page_right"),
			postFunctionCenter : function() {
                // dashboard.widget.quotes.load();          // quotes
                // dashboard.widget.tkt.load();             // tickets
            },
			postFunctionRight : function() {
				// dashboard.widget.customer_status.load(); // status cliente (horas)
            },
			onCreate : function() {    
                dashboard = new Dashboard();                   // Dashboard obj
                dashboard.initialize();
                
                
                
                /*
                dashboard.widget.quotes.initialize();          // quotes
                dashboard.widget.tkt.initialize();             // tickets
                
                console.log("$USER->{tipo}");
                dashboard.widget.customer_status.initialize(); // status cliente (horas)
                dashboard.widget.empresas.initialize();        // status cliente (horas)
                */
            }
        });   
        
        this.menu(); // inicia menu
    }
    
    /* menu */
    this.menu = function(){

        eos.menu.action.new({ // novo chamado
            id       : "icon_dashboard_chamado",
            title    : "novo",
            subtitle : "ticket",
            click    : function(){
                eos.core.call.module.tkt();
            }
        });
        
        eos.menu.action.new({ // refresh
            id       : "icon_dashboard_refresh",
            title    : "atualiza",
            subtitle : "dashboard",
            click    : function(){
                dashboard.widget.tkt.load(); // tickets
                dashboard.widget.orc.load(); // orcamentos
                
                // dashboard.widget.customer_status.load(); // status cliente (horas)
            }
        });
    }
}


/*
*   Document Ready
*/
\$(document).ready(function() { 
    form = new Form();
    form.initialize();
    
    // refres dos itens do dashboard
    control_refresh = window.setInterval(function(){ 
        if(\$("#dashboard_page").is(":visible")) {
            dashboard.widget.tkt.load(); // tickets
            dashboard.widget.orc.load(); // orcamentos
            
        } else {
            window.clearTimeout(control_refresh);
        }
    }, 900000);

});

</script>
</head>
<body>

    <!-- Formulario -->
    <form >
	
        <!-- DTouchPages -->
        <div id="dashboard_page">
            
            <!-- Page Center -->
            <div id="dashboard_page_center">
                
                <div class="dashboard_container_center">
    
                    <!-- Quotes -->
                	<div id="quote" class="widget">
                	    <span id="quote_descrp"></span> <span id="quote_autor"></span>
                	</div>
    
                    <!-- Tickets -->
                	<div id="dashboard_tkt_container" class="widget"></div> 
                    
                    <!-- Orcamentos -->
                	<div id="dashboard_orc_container" class="widget"></div> 
                </div>

                <!-- container esquerda -->
                <div class="dashboard_container_left">    	
        
                </div>
                
                <!-- container direita -->
                <div class="dashboard_container_right">
    
                </div>
                
                
            </div>
        
        
        
            <!-- Page Right -->
            <div id="dashboard_page_right">
                
                <!-- container center -->
                <div class="dashboard_container_center">
                    <!-- FeedBack -->
                	<div id="feedback_container" class="widget">
                	    <div id="feedback"></div>
                	</div>
                </div>
                  
                <!-- container esquerda -->
                <div class="dashboard_container_left">
    
                    <!-- estatisticas -->
                    <div id="status_container" class="widget">
                        <div id="status_tabs">
                    		<ul>
                                <li><a href="#customer_status_container">Clientes</a></li>
                                <li><a href="#tec_status_container">Técnicos</a></li>
                            </ul>
                
                            <!-- cliente -->
                        	<div id="customer_status_container">
                        		<div id="customer_status"></div>
                        	</div>
                    
                            <!-- tecnicos -->
                            <div id="tec_status_container">
                                <div id="tec_status">estatisticas tecnicos</div>
                            </div>
                        </div>      
                    </div>
            
                </div>
                
                <!-- container direita -->
                <div class="dashboard_container_right">
                    <!-- empresas -->
            	    <div id="empresas_container" class="widget">
            		    <div id="empresas"></div>
            	    </div>
                    
                    <!-- node 
            	    <div id="node_container">
            		    <div id="node" style="width:100%; height:100px; border:1px solid red; margin-top:350px;"></div>
            	    </div>
                    -->
            </div>
        </div>
        
    </form>
    
</body>
</html>

HTML

