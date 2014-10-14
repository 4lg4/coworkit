#!/usr/bin/perl

#
# Grupos.cgi
#
# na tela de cadastro de empresas adiciona a feature para
# cadastrar novos grupos no banco de dados
#

$nacess = "201";
require "../cfg/init.pl";

$grupo = &get('grupo');

# insere no banco
$DB = &DBE("insert into tipo_relacionamento(descrp) values ('$grupo')");

# recupera codigo do novo registro incluido
$DB = &DBE("select currval('tipo_relacionamento_codigo_seq')");
$R = $DB->fetch;

# retorno do codigo 
print $query->header({charset=>utf8});
print @$R[0];