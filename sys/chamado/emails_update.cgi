#!/usr/bin/perl

#
# Emails
# 	- emails.cgi
#
#   Chamado, lista emails relacionados ao chamado
#

# variaveis
$nacess = "10";
require "../cfg/init.pl";

print $query->header({charset=>utf8});

$ID      = &get('ID');
$email   = &get('email');
$empresa = &get('empresa');
$area    = &get('area');

# novo ticket lista emails existentes
if(!$email) {
    
    # Busca enderecos da empresa e atualiza lista
    $DB = &DBE("
        select 
            * 
        from 
            empresa_area_email 
        where 
            empresa = $empresa and 
            area = $area
    ");
    
    while($email = $DB->fetchrow_hashref) {
    	$array .= "{val:'$email->{email}',descrp:'$email->{email}'},";
    }

if($array) {
    $list = " addItem     : [$array], ";
}
# retorno
print<<HTML;
<script> 
		// email
		\$("#emails_list").DTouchRadio({ 
            orientation : "vertical",
            $list
            /*
			itemDel     : function(x){
			    console.log(x);
			},
            */
            itemDel     : true,
            unique      : true
		});
</script>
HTML

# se for edicao do chamado
# adiciona item em segundo plano
} else {

    $DB = &DBE("
        select 
            * 
        from 
            empresa_area_email 
        where 
            email <=> '$email'
    ");
    
    if($DB->rows() == 0) {
        $DB = &DBE("
            insert into
                empresa_area_email
                    (empresa, area, email)
                values
                    ($empresa, $area, '$email')
        ");
    }
    
    
}

