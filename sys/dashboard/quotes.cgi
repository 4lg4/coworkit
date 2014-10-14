#!/usr/bin/perl

#
# quotes.cgi
#
# carrega aleatoriamente uma quote diaria
#

$nacess = "2";
# $nacess_more = "or menu = 74";
require "../cfg/init.pl";

$ID = &get('ID');

# print $query->header({charset=>utf8});


# gera grafico com as ultimas medicoes
$DB = DBE("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1");
$q = $DB->fetchrow_hashref;

# $R = "<span style='font-size: 1.2em; letter-spacing: 1px;'>&quot;$q->{descrp}&quot;</span> <span style='font-style: italic; margin-left: 0.5%; color: #ccc;'>$q->{autor}</span>";

print $query->header('application/json; charset="utf-8"');

# retorno do codigo 
print<<HTML;

    {
        "descrp" : "$q->{descrp}",
        "autor"  : "$q->{autor}"
    }
    
HTML
