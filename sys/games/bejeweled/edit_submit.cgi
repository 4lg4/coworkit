#!/usr/bin/perl

$nacess = "0";
require "../../cfg/init.pl";

print $query->header({charset=>utf8});

# vars
$ID = &get('ID');
$SCORE = &get('SCORE');
$GAME = &get('GAME');

$DB = DBE("insert into games_score (usuario, game, score) values ($USER->{usuario}, $GAME, '$SCORE')");

print<<HTML;
<script>

	DMessages('Score adicionado com sucesso !!');
	
</script>
HTML


exit;
