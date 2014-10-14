#!/usr/bin/perl


# [INI] DTouchRadio ----------------------------------------------------------------------------------------------------------------------
#	Usada juntamente com a funcao jquery DTouchRadio
#	Cria elementos radio com imagens e touch
#
sub DTouchRadio
	{ my ($codigo,$imagem,$descrp) = @_;
		
	$retorno = "<div><input type='radio' name='chamado_tipo' value='".$codigo."' /><img src='".$imagem."' /><span>".$descrp."</span></div>";
	
	return $retorno;
	}
# [END] DTouchRadio ----------------------------------------------------------------------------------------------------------------------	