#!/usr/bin/perl
require "../init.pl";

#
#   DIssue
#       DIssue.cgi
#
#       controle de issues
#

# pega variaveis
$ID      = &get("ID");    # ID do usuario logado
# $title   = &get("title");
$type    = &get("type");
$source  = &get("source");
$message = &get("message");

# header 
print $query->header('application/json; charset="utf-8"');
# print $query->header({charset=>utf8});

# lista todos os campos para o debug
@campo = $query->param();
for($f=0;$f<@campo;$f++) {
	$campos .= "#".$campo[$f]." => ".&get($campo[$f])." <br>";
}

# adiciona variaveis de ambiente 
$message .= "<br><br><br><hr>".$campos;

$message =~ s/(\n|\r)/<br>/gm;
$message =~ s/\'/\\\'/gm;

# debug("insert into         issue (            usuario,            tipo,            source,            parceiro,            descrp        ) values (            $USER->{usuario},            $type,            $source,            $USER->{empresa},            '$message')");


DBE("
    insert into 
        issue (
            usuario,
            tipo,
            source,
            parceiro,
            descrp
        ) values (
            $USER->{usuario},
            $type,
            $source,
            $USER->{empresa},
            '$message'
        )
");

# $message =~ s/(\n|\r)/<br>/gm;

# mensagem
$R  = '{ ';
$R .= '     "status"  : "success", ';
$R .= '     "message" : "Email enviado" ';
$R .= '}  ';
print $R;

exit;

