/**
 * 
 * DMaps:
 * 		atualmente usa google maps para rendernizar os mapas
 *
 * @example var G = $.DMaps();
 * @desc Uso
 *
 * @return Retorna Mapa
 *
 * @type jQuery
 *
 * @name DMaps
 * @cat Plugins / Core
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

// api google maps (carregamento dentro do DPAC de forma asyncrona unico lugar que funcionou)
//loadJS("https://maps.googleapis.com/maps/api/js?sensor=false");
loadJS("/comum/gmap3/gmap3.min.js");

(function($){
$.fn.DMaps = function(settings,value)
	{ console.log(settings);
	var settings = $.extend(
		{
		enable	: true,
		fulladdress: "",
		address	: "Avenida São Pedro, 1001",
		country	: "Brasil",
		state	: "Rio Grande do Sul",
		city	: "Porto Alegre",
		descrp	: "Defaut description for the pinned place !"
		}, settings || {});

	return this.each(function()
		{
		if(settings.fulladdress == "")
			settings.fulladdress = settings.address+", "+settings.city+" - "+settings.state+", "+settings.country
		
		// settings.map = $(this);
		// settings.map_id = $(this).prop("id");
		// $(this).gmap3('destroy').remove();
		
		$(this).gmap3(
			{
			marker:{
				values:
					[
					// endereco do cliente
					{address: settings.fulladdress,
					data: settings.descrp,
					options:{ icon: "/img/ui/map_pin.svg" }},
					
					// endereco da empresa
					{address: COMPANY["address"],
					data: COMPANY["name"],
					options:{ icon: COMPANY["icon_maps"] }}
					],
				options:{
				      draggable: false
				    },
				    events:{
				      mouseover: function(marker, event, context){
				        var map = $(this).gmap3("get"),
				          infowindow = $(this).gmap3({get:{name:"infowindow"}});
				        if (infowindow){
				          infowindow.open(map, marker);
				          infowindow.setContent(context.data);
				        } else {
				          $(this).gmap3({
				            infowindow:{
				              anchor:marker,
				              options:{content: context.data}
				            }
				          });
				        }
				      }
					  /*,
				      mouseout: function(){
				        var infowindow = $(this).gmap3({get:{name:"infowindow"}});
				        if (infowindow){
				          infowindow.close();
				        }
				      }
					  */
			    	}
				},
			    map:{
			      options:{
			        zoom: 17
			      }
			    }	
			});
		});
	};
})( jQuery );


/* usando geolocalizacao 

$('#test1').gmap3({
  getgeoloc:{
    callback : function(latLng){
      if (latLng){
        $('#test1-result').html('localised !');
        $(this).gmap3({
          marker:{ 
            latLng:latLng
          }
        });
      } else {
        $('#test1-result').html('not localised !');
      }
    }
  }
});

*/

