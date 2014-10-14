#!/usr/bin/perl

$nacess = "0";
require "../../cfg/init.pl";
$ID = &get('ID');

print $query->header({charset=>utf8});

print<<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.01 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html id="html">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	
<script language='JavaScript'>
	// carrega dependencias especificas
	DLoad("snake");
	
// salva score
function DActionSave()
	{
	DActionAjax("edit_submit.cgi",\$("#CAD").serialize());
	}

var canvas = null;
var game = null;

// inicia partida
function Start() 
	{
    game.start();
	}

function Pause() 
	{
    game.stop();
	}

// reiniciar o game
function Reset() 
	{
	var sim = function()
		{
		var score = game.score();
		
		// salva score do usuario
		\$("#CAD input[name=SCORE]").val(score.toString());
		DActionSave();
		
		// reinicia o jogo
		game.reset();
		};
	
	Pause();
	confirma("Deseja finalizar a partida atual ? ",sim,"Start()");
	}

// quando finaliza o game
function OnGameOver() 
	{
    var score = game.score();

	// salva score do usuario
	\$("#CAD input[name=SCORE]").val(score.toString());
	DActionSave();
	
	game.reset();
	}

// quando o documento esta pronto 
\$(document).ready(function() 
	{ 
	unLoading();
	
	menu_snake = new menu();
	menu_snake.btnNew("icon_snake_start","iniciar","Start()");
	menu_snake.btnNew("icon_snake_pause","pausar","Pause()");
	menu_snake.btnNew("icon_snake_reset","finalizar","Reset()");

	
	// ajustes iniciais do game
	canvas = \$("#gamewindow");
    game = new SnakeGame(canvas);

    game.init({});
    game.ongameover(OnGameOver);

	// unLoading();
	});
</script>
<style>
.jqplot-table-legend
	{
	top: 15px !important;
	}
</style>
</head>
<body>

<form name='CAD' id='CAD'>

	<div id="snake_container">
        <canvas id="gamewindow"></canvas>
    </div>
    <div style="display:none;">
        <input id="btnStartGame" type="button" value="Start Game" onclick="javascript: Start();" />
        <input id="btnPauseGame" type="button" value="Pause" onclick="javascript: Pause();" disabled="disabled" />
        <input id="btnResetGame" type="button" value="Reset" onclick="javascript: Reset();" disabled="disabled" />
    </div>

<div id="resultado" class="DDebug"></div>

	<!-- variaveis de ambiente -->
	<input type='hidden' name='SCORE'>
	<input type='hidden' name='GAME' value='1'>
</form>
</body></html>

HTML


