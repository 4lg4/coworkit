/*
 * Plugin D-Tips
 * Tool Tip, para uso em links, forms, imagens etc.
 *
 * akgleal.com
 */
(function($){

    $.fn.dtips = function(options) {

        var defaults = {
            message : 'D-Tips Works !',
            useAttr : false,
            /* 
			Background: '#EEE',
            cssColor: '#000',
            cssBorder: '1px solid #DDD',
            cssPadding: '5px',
            cssWidth: '250px',
            cssTextAlign: 'left',
			*/
			X: '10',
			Y: '10'
        };
        var options = $.extend(defaults, options);
		// var X = $('body').pageX - options.X;
		// var Y = $('body').pageY - options.Y;
			
			
        /* Atribute, se estiver setado como falso  ------------------------------*/
        if(options.useAttr !== false)
            options.message = $(this).attr(options.useAttr);

        /* Adiciona Tool Tip ---------------------------------------------------- */
        $('body').append('<div id="Dtips" style="display:none"></div>');

        /* Mouse Over, Mostra Tool Tip ----------------------------------------- */
        $(this).mousemove(function(e)
			{
            // texto
            $('#Dtips').html(options.message);

            // css
            $('#Dtips').css('position','absolute');
            $('#Dtips').css('z-index','999999');
			/*
            $('#Dtips').css('padding',options.cssPadding);
            $('#Dtips').css('color',options.cssColor);
            $('#Dtips').css('background',options.cssBackground);
            $('#Dtips').css('width',options.cssWidth);
            $('#Dtips').css('background',options.cssBackground);
            $('#Dtips').css('border',options.cssBorder);
            $('#Dtips').css('text-align',options.cssTextAlign);
			*/
			
            // mostra
            if($('#Dtips').css('display') == 'none')
                $('#Dtips').show();

            // ajusta posicao
			// X = X; // - 20; // + options.posX;
			// Y = e.pageY; // - 5; //  options.posY;
			
			pos = $(this).offset();
			X = $(this).width();
			X = pos.left - X;
			Y = pos.top;
			
            $('#Dtips').css('right',X+'px');
            $('#Dtips').css('top',Y+'px');
			stop = 1;
        	})
		/* Mouse Out, Esconde Tool Tip --------------------------------------- */
		.mouseout(function()
			{
            $('#Dtips').hide();
        	});
    }
})(jQuery);