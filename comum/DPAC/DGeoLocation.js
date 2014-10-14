/**
 * 
 * Pega Geo Localização atual
 *
 * @example var G = $.DGeoLocation();
 * @desc Uso
 *
 * @return Retorna objeto com as coordenadas
 *
 * @type jQuery
 *
 * @name DGeoLocation
 * @cat Plugins / Core
 * @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http://gaiattos.com/akgleal.com)
 */

(function($, window){
	
$.extend(
	{
	DGeoLocation: function(settings)
		{
		// testa se navegador possui suporte a geo localizacao
		if(!navigator.geolocation)
			{
			console.log("O Navegador não possui capacidade de geolocalizacao");
			return false;
			}
		
		// seta GPS var
		navigator.geolocation.getCurrentPosition(function (position) 
			{
			GPS["lat"] = position.coords.latitude;
			GPS["lon"] = position.coords.longitude;
			});
				
		// retorna conforme o caso
		switch(settings)
			{
			case "":
				return GPS;
			break;
			
			case "lat":
			case "latitude":
				return GPS["lat"];
			break;
			
			case "lon":
			case "long":
			case "longitude":
				return GPS["lon"];
			break;
			}
		}
	});
	
})(jQuery, this);
