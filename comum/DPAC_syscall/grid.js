/* [INI]  Grid (by akgleal.com)  -------------------------------------------------------------------------
	Dependencias:
	<script type="text/javascript" src="/comum/DPAC_syscall/jquery/jquery.tablesorter.js"></script>

	CSS necessario:
	.fieldUser { }
	.fieldDisable { padrao de cores para campo desabilitado }

    Opcoes:

	Exemplo de uso:
	var campoNumber = new fieldNumber("campo_number");
	campoNumber.setSize(10);
	<input type="text" id='campo_number' name='campo_number'>

	var campoNumber = new fieldNumber("campo_number","10");
	<input type="text" id='campo_number' name='campo_number'>
*/

include("/comum/DPAC_syscall/jquery/jquery.tablesorter.js");
include("/comum/DPAC_syscall/jquery/jquery.tablesorter.pager.js");

function grid(table,tipo,sort,cor)
	{
	if(!tipo || tipo=="")
		{
		tipo ='#';
		}
	else
		{
		tipo = ".";
		}
		
	if(!cor || cor=="")
		{
		cor ="#";
		}
	else
		{
		cor = "sem_zebra";
		}

	//alert(sort);
	

	if(!sort || sort=="")
		{
		sort ="#";
		}
	else
		{
		sort ="teste";
		}

	// cria campo
	this.show = function()
		{
			//alert(table+'-'+tipo+'-'+sort);
			if(sort!="#" && cor!="#")
			{
			// seta campo
			$(tipo+''+table)
				.addClass("tablesorter")			
				.tablesorter({
						sortList: [[0,1]],
						dateFormat: 'uk',
						widgets: [],
						headers: 
						{
							1:{ 0:{sorter:'datetime'}}
						}
						
				});

			}
			else if (sort!="#" && cor=="#")
			{
			// seta campo
			$(tipo+''+table)
				.addClass("tablesorter")
				.tablesorter({
				
						sortList: [[0,1]],
						dateFormat: 'uk',
						headers: 
						{
							1:{ 0:{sorter:'datetime'}}
						}
					
				});
			}
			else if (sort=="#" && cor!="#")
			{
			// seta campo
			$(tipo+''+table)
				.addClass("tablesorter")
				.tablesorter({
				
						dateFormat: 'uk',
						widgets: [],
						headers: 
						{
							1:{ 0:{sorter:'datetime'}}
						}
					
				});
			}
			
			else
			{
			// seta campo
			$(tipo+''+table)
				.addClass("tablesorter")
				.tablesorter({
				
						dateFormat: 'uk'
					
				});
			}

		}


	// define tamanho
	// this.size = function(size){ fieldOptSize(field,size); };

	// desabilita
	// this.disable = function(){ fieldOptDisable(field); };

	// habilita
	// this.enable = function(){ fieldOptEnable(field); };

		return this.show();
	}




/*
// add new widget called repeatHeaders
$.tablesorter.addWidget({
    // give the widget a id
    id: "repeatHeaders",
    // format is called when the on init and when a sorting has finished
    format: function(table) {
        // cache and collect all TH headers
        if(!this.headers) {
            var h = this.headers = [];
            $("thead th",table).each(function() {
                h.push(
                    "" + $(this).text() + ""
                );

            });
        }

        // remove appended headers by classname.
        $("tr.repated-header",table).remove();

        // loop all tr elements and insert a copy of the "headers"
        for(var i=0; i < table.tBodies[0].rows.length; i++) {
            // insert a copy of the table head every 10th row
            if((i%5) == 4) {
                $("tbody tr:eq(" + i + ")",table).before(
                    $("").html(this.headers.join(""))

                );
            }
        }
    }
});
*/
 