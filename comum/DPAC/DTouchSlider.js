/* [INI]  DTouchSlider (by http://gaiattos.com/akgleal)  ------------------------------------------------------------------------- 

*/

(function($){
	
$.fn.DTouchSlider = function(settings,value) 
	{
		/*
	if(isObject(settings) === true)
		{
		*/
		var settings = $.extend(
			{
			enable		: true,
			type		: 'boxes', 	// boxes / pages
			handler		: 'left',	// left / right
			orientation	: 'vertical', // vertical / horizontal
			rolltotal	: 0,
			width		: '',
			height		: ''
			}, settings);
			/*
		}
	else
		{
		switch(settings)
			{
			case "value":
				if(value == "")
					{
					console.log("DTouchSlider: valor nao pode ser vazio !!");
					return false;
					}
				
				// ajusta valor slider
				$(this).data("DTouchSliderSettings")["value"] = value;
				
				// seta valor slider
				DTouchSliderSetValue($(this));
				
				return true;
			break;
			}
		}
	*/
	// cria id unico para slider
	settings.slider_id = "DTouchSlider_"+$(this).attr("id");
	
	return this.each(function()
		{ 
		// objeto
		settings.container = $(this);
		
		// remove slider se existir
		$("#"+settings.slider_id).remove();
		
		// inicia obejto
		settings.container
			
			// esconde overflow
			.css("overflow","hidden")
			
			// adiciona elemento slider
			.prepend('<div id="'+settings.slider_id+'" class="DTouchSlider"></div>');
		
	
		// ajusta CSS para boxes se for o caso
		if(lc(settings.type) == "boxes")
			{
			$("#"+settings.slider_id).addClass('DTouchSliderBoxes');
			
			// ajusta css da orientacao vertical / horizontal
			if(lc(settings.orientation) == "horizontal")
				{
				$("#"+settings.slider_id).addClass('DTouchSliderBoxesHorizontal');
				settings.container_scroll = settings.container[0].scrollWidth;
				settings.container_view = settings.container.width();
				}
			else
				{
				$("#"+settings.slider_id).addClass('DTouchSliderBoxesVertical');
				settings.container_scroll = settings.container[0].scrollHeight;
				settings.container_view = settings.container.height();
				}
			}
		
		
		// adiciona slider somente se o tamanho exceder
		if(settings.container_scroll > settings.container_view)
			{
			// calculo do tamanho do slider
			settings.rolltotal = settings.container_scroll - settings.container_view;

			// cria slider
			$("#"+settings.slider_id).slider(
				{
				orientation: settings.orientation,
				range: "min",
				min: 0,
				max: settings.rolltotal,
				value: settings.rolltotal,
				change: function( event, ui ) 
					{
					// executa scroll 
					if(settings.orientation == "horizontal")
						settings.container.scrollLeft(settings.rolltotal - ui.value);
					else
						settings.container.scrollTop(settings.rolltotal - ui.value);
					},
				slide: function( event, ui ) 
					{
					// executa scroll 
					if(settings.orientation == "horizontal")
						settings.container.scrollLeft(settings.rolltotal - ui.value);
					else
						settings.container.scrollTop(settings.rolltotal - ui.value);
					},
				});
			}
		});
	};

})( jQuery );





