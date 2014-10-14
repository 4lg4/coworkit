#!/usr/bin/perl

#####
# DDialog
#   usado em conjunto com DUI.js
#   $.DDialog();
#     gera popup de dialogo
#
# @type Perl Package
# @name DDialog
# @cat DPAC / Perl
# @author DONE Tecnologia - Adriano Karkow Gaiatto Leal (http=>//akgleal.gaiattos.com/)


package DDialog;

sub new {
    
    my $class = shift; 
    my $self = {
        message   => shift || 'Teste: Janela de Dialogo',
		type      => shift || 'alert',
        stop      => shift || false,
		title     => shift || 'Aviso',
		resizable => shift || true,
		draggable => shift || true
    };
    
    bless $self, $class; # popula variaveis
        
    # monta janela de dialogo
	print " <script>                
                \$.DDialog({ 
                    type      : \"$self->{type}\",
                    message   : \"$self->{message}\",
                    title     : \"$self->{title}\",
            		resizable : \"$self->{resizeable}\",
            		draggable : \"$self->{draggable}\"
                });
            </script>";
    
    # se for para interromper o script	
	if($self->{stop} eq true) { 
		exit; 
	}
}

1;
