#!/usr/bin/perl

#   DefaultModule.cgi
#       modulo com funcoes do modulo default do sistema

# [INI] ----------------------------------------------------------------------------------------------------------------------
sub listField {
    my ($field) = @_;
    
    if($field eq "exportar" || $field eq "parceiro" || $field eq "pai") {
        return "noshow";
    } elsif($field eq "codigo") {
        return "hidden";
    } else {
        return "show";
    }
}

sub translateTitle {
    my ($text) = @_;
    
    if($text eq "descrp") {
        return "Descrição";
    }
}
# [END] DListGet -------------------------------------------------------------------------------------------------------------

return true;
