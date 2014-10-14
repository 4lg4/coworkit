/// <reference path="jquery-1.9.1.js" />
/// <reference path="jcanvas.js" />
/// <reference path="snakegame.js" />
/// <reference path="snake.js" />
/// <reference path="snakegrid.js" />

var canvas = null;
var game = null;

function Start() {
    $("#btnStartGame").blur();
    $("#btnPauseGame").removeAttr("disabled");
    $("#btnStartGame").attr({
        disabled: "disabled"
    });

    game.start();
}

function Pause() {
    $("#btnStartGame").removeAttr("disabled");
    $("#btnPauseGame").attr({
        disabled: "disabled"
    });
    game.stop();
}

function Reset() {
    $("#btnResetGame").attr({
        disabled: "disabled"
    });
    $("#btnStartGame").removeAttr("disabled");
    game.reset();
}

function OnGameOver() {
    var score = game.score();

    $("#btnPauseGame").attr({
        disabled: "disabled"
    });
    $("#btnResetGame").removeAttr("disabled");
    alert("Game Over!\nFinal Score:" + score.toString());

	// salva score do usuario
	$("#CAD input[name=SCORE]").val(score.toString());
	DActionSave();
	}


$(function () {
    canvas = $("#gamewindow");
    game = new SnakeGame(canvas);

    game.init({

    });
    game.ongameover(OnGameOver);
})

