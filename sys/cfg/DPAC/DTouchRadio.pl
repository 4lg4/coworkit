#!/usr/bin/perl

# [INI] DTouchRadio ----------------------------------------------------------------------------------------------------------------------
#	Usada juntamente com a funcao jquery DTouchRadio (/comum/DPAC/DTouchRadio.js)
#	Cria elementos radio com imagens e touch
#	
#	uso
#		$chamado_tipo .= DTouchRadio($t->{codigo},Nome do Campo,$t->{img},$t->{descrp});
# 	retorno
# 		"<div><input type='radio' name='chamado_tipo' value='$t->{codigo}' /><img src='$t->{img}' /><span>$t->{descrp}</span></div>"

sub DTouchRadio
	{ my ($field,$codigo,$imagem,$descrp) = @_;
		
	$retorno = "<div><input type='radio' name='".$field."' value='".$codigo."' /><img src='".$imagem."' /><span>".$descrp."</span></div>";
	
	return $retorno;
	}
# [END] DTouchRadio ----------------------------------------------------------------------------------------------------------------------



return true;
