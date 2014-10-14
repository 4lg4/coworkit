/* [INI] DLoad --- gaiattos.com/akgleal -------------------------------------------------------------------------------------------------

	Carrega todas as dependencias de Javascript e CSS
	
	
	
	Uso:
	
	1) Criar array de dependencias, conforme exemplo, 
		- Titulo (comentario)
		- Nome do modulo
		- Classes Javascript em array
		- Classes CSS em array
		
		// exemplo
			{
			"module"	: "exemplo",
			"JS" 		: ["classe1.js","classe2.js"],
			"CSS" 		: ["classe1.css", "classe2.css"]
			}
			
	2) Uso no codigo
		DLoad("modulo");
		
		
	Todo: 
		- verificar a possibilidade de automatizar isso usando a funcao call
		- adicionar o carregamento por nacess
*/

// var MODULE = [];

function DLoad(m) {
	
	// listas com dependencias dos modulos
	MODULE = {
		// exemplo
			exemplo : {
    			module	: "exemplo",
    			JS 	: ["classe1.js","classe2.js"],
    			CSS 	: ["classe1.css", "classe2.css"],
    			CSSM 	: ["/css/modulos/mobile.css"]
			},
			
		// default_avatar
			default_avatar : {
			module	: "default_avatar",
			// JS 	: ["/comum/jquery/jquery.carousel.js"],
			CSS 	: ["/css/modulos/default_avatar.css"],
			PATH	: ["/sys/upload"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
			
		// tipo_usuario
			usuario_tipo : {
			module	: "usuario_tipo",
			// JS 	: ["/comum/jquery/jquery.carousel.js"],
			CSS 	: ["/css/modulos/tipo_usuario.css"],
			PATH	: ["/sys/cad/usuario_tipo"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},

		// usuarios
			usuarios : {
			module	: "usuarios",
			JS 	: [],
			CSS 	: ["/css/modulos/usuarios.css"],
			PATH	: ["/sys/cad/usuarios"]
			},
        
		// NEW usuarios
			users : {
			module	: "users",
			JS 	: [],
			CSS 	: ["/css/modulos/users.css"],
			PATH	: ["/sys/users"]
			},
            
		// verify usuario
			verify : {
			module	: "verify",
			JS 	: [],
			CSS 	: ["/css/modulos/verify.css"],
			PATH	: ["/sys/users"]
			},
            
		// Contatos
			contatos : {
			module	: "contatos",
			JS 	: [],
			CSS 	: ["/css/modulos/contatos.css"],
			PATH	: ["/sys/contatos"]
			},
            
		// Files, arquivos
			files : {
			module	: "files",
			JS 	: [],
			CSS 	: ["/css/modulos/files.css"],
			PATH	: ["/sys/files"]
			},
            
		// Planos
			planos : {
			module	: "planos",
			JS 	: [],
			CSS 	: ["/css/modulos/planos.css"],
			PATH	: ["/sys/planos"],
            COD     : "55"
			},
            
		// Produtos
			produtos : {
			module	: "produtos",
			JS 	: [],
			CSS 	: ["/css/modulos/produtos.css"],
			PATH	: ["/sys/produtos"],
            COD     : "76"
			},
            
		// Servicos
			servicos : {
			module	: "servicos",
			JS 	: [],
			CSS 	: ["/css/modulos/servicos.css"],
			PATH	: ["/sys/servicos"],
            COD     : "51"
			},
            
		// Checklist
			checklist : {
			module	: "checklist",
			JS 	: [],
			CSS 	: ["/css/modulos/checklist.css"],
			PATH	: ["/sys/checklist"]
			},    
        
		// Dados TI
			dadosti : {
			module	: "dadosti",
			JS 	: [],
			CSS 	: ["/css/modulos/dadosti.css"],
			PATH	: ["/sys/dadosti"],
            COD     : "73"
			},
            
		// Default, modulo padrao para cadastros auxialiares
			default : {
			module	: "default",
			JS 	: [],
			CSS 	: ["/css/modulos/default.css"],
			PATH	: ["/sys/default"]
			},
            
		// procedimentos
			procedimentos : {
			module	: "procedimentos",
			JS 	: [],
			CSS 	: ["/css/modulos/default.css", "/css/modulos/procedimentos.css"],
			PATH	: ["/sys/procede"]
			},
			
		// dones
			dones : {
			module	: "dones",
			JS 	: [],
			CSS 	: ["/css/modulos/dones.css"],
			PATH	: ["/sys/cad/dones"]
			},
		
		// empresa
			empresa : {
			module	: "empresa",
			// JS 		: ["http://maps.googleapis.com/maps/api/js?sensor=false"],
			CSS 	: ["/css/modulos/empresa.css"],
			PATH	: ["/sys/empresa"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
		
		// chamado
			chamado : {
			module	: "chamado",
			JS 	: [],
			CSS 	: ["/css/modulos/chamado.css", "/comum/select2/select2.css"],//,"/css/modulos/chamado_blue.css"],
			PATH	: ["/sys/chamado/"],
            COD     : "10"
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
			
		// chamado relatorio
			chamado_relatorio : {
			module	: "chamado_relatorio",
			JS 		: [],
			CSS 	: ["/css/modulos/chamado_relatorio.css"],
			PATH	: ["/sys/chamado/rel"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},

		// chamado relatorio produtividade
			chamado_relatorio_prod : {
			module	: "chamado_relatorio_prod",
			JS 		: [],
			CSS 	: ["/css/modulos/chamado_relatorio_prod.css"],
			PATH	: ["/sys/chamado/rel"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
        
		// secretaria
			secretaria : {
			module	: "secretaria",
			JS 		: [],
			CSS 	: ["/css/modulos/secretaria.css"],
			PATH	: ["/sys/secretaria"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
		
		// dashboard
			dashboard : {
			module	: "dashboard",
			JS 		: [], //["/comum/jqplot/jquery.jqplot.min.js","/comum/jqplot/plugins/jqplot.pieRenderer.min.js","/comum/jqplot/plugins/jqplot.dateAxisRenderer.min.js"],
			// JS 		: ["/comum/jqplot/jquery.jqplot.min.js","/comum/jqplot/plugins/jqplot.dateAxisRenderer.min.js"],
			CSS 	: ["/css/modulos/dashboard.css"], /* "/comum/jqplot/jquery.jqplot.min.css"], */
			PATH	: ["/sys/dashboard"],
            COD     : "2"
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
            
		// orcamento
			orc : {
			module	: "orc",
			JS 		: ["/comum/jspdf/jspdf.min.js","/comum/jspdf/base64.js"],
			CSS 	: ["/css/modulos/orc.css"],
			PATH	: ["/sys/orc"],
            // COD     : "78"
			},

		// orcamento relatorio
			orc_rel : {
			module	: "orc_rel",
			JS 		: ["/comum/modulos/orc_rel.js"],
			CSS 	: ["/css/modulos/orc_rel.css"],
			PATH	: ["/sys/orc/rel"],
            // COD     : "78"
			},
			
		// agenda
			agenda : {
			module	: "agenda",
			JS 		: ["/comum/fullcalendar/fullcalendar/fullcalendar.js","/comum/fullcalendar/fullcalendar/gcal.js"],
			CSS 	: ["/comum/fullcalendar/fullcalendar/fullcalendar.css","/comum/fullcalendar/fullcalendar/fullcalendar.print.css","/css/modulos/agenda.css"],
			PATH	: ["/sys/dashboard"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
			
		// Faturamento
			faturamento : {
			module	: "faturamento",
			JS 		: [],
			CSS 	: ["/css/modulos/faturamento.css"],
			PATH	: ["/sys/done/faturamento"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
			
		// Games SNAKE
			snake : {
			module	: "snake",
			JS 		: ["/comum/games/jssnake/scripts/jcanvas.min.js","/comum/games/jssnake/scripts/helpers.js","/comum/games/jssnake/scripts/snakegame.js"],
			CSS 	: ["/css/modulos/games/snake.css"],
			PATH	: ["/sys/games/snake"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
		
		// Games bejeweled
			bejeweled : {
			module	: "bejeweled",
			JS 		: ["/comum/games/bejeweled/scripts/script.js"],
			CSS 	: ["/css/modulos/games/bejeweled.css"],
			PATH	: ["/sys/games/bejeweled"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
            
		// monitoramento
			monitoramento : {
			module	: "monitoramento",
			JS      : ["/comum/jqplot/jquery.jqplot.min.js","/comum/jqplot/plugins/jqplot.pieRenderer.min.js","/comum/jqplot/plugins/jqplot.donutRenderer.min.js","/comum/jqplot/plugins/jqplot.dateAxisRenderer.min.js"],
			CSS 	: ["/css/modulos/dashboard.css", "/comum/jqplot/jquery.jqplot.min.css", "/css/modulos/default.css", "/css/modulos/procedimentos.css"],
			PATH	: ["/sys/monitoramento"]
			// CSSM 	: ["/css/modulos/chamado_mobile.css"]
			},
            
		// pagamentos
			pagamento : {
    			module	: "pagamento",
    			JS      : ["/comum/modulos/pagamento.js"],
    			CSS 	: ["/css/modulos/pagamento.css"],
    			PATH	: ["/sys/done/pagamento"]
			}
		
		};
	
    
    // modulo encontrado 
    if(MODULE[m]){
        // JS
        if(MODULE[m].JS){
            MODULE[m].JS.forEach(function(i){
                include(i);
            });
        }
        
        // CSS
        if(MODULE[m].CSS){
            MODULE[m].CSS.forEach(function(i){
                loadCSS(i);
            });
        }
        
        if(MODULE[m].COD){
            eos.menu.where(MODULE[m].COD,true);
        }
        
		// seta variavel global do modulo atual
		$('#AUX [name="MODULO_PATH"]').val(MODULE[m].PATH);
    
        
    // se modulo nao cadastrado
    } else {
        $.DDialog({
            type : "error",
            message : "Módulo não cadastrado"
        });
    }

    
}