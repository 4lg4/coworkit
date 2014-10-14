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

$ID = &get('ID');
$COD = &get('COD');

# Busca enderecos da empresa e atualiza lista
$DB = &DBE("select * from tkt_email where tkt = $COD");

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
			itemDel     : true,
            unique      : true
		});
</script>

HTML
