/// <reference path="jquery-1.9.1.js" />
/// <reference path="jcanvas.js" />
/// <reference path="snakegrid.js" />
/// <reference path="snake.js" />
/// <reference path="helpers.js" />

var SnakeNamespace = {};

var SnakeGame = function (canvas) {

    var _canvas = canvas || $("canvas");
    var _score = 0;
    var _settings = {
        gridSize: 13,
        maxRow: 40,
        maxColumn: 40,
        refreshRate: 1000 / 15,
        scorePerFood: 30
    };
    var Keys = {
        Left: 37,
        Right: 39,
        Up: 38,
        Down: 40
    };
    var _events = {
        ongameover: []
    };
    var _borderSize = {
        top: 30,
        left: 30,
        right: 30,
        bottom: 30
    };
    var _colors = {
        text: "#993366",
        border: "#660033"
    };
    var _grid = null;
    var _ongoing = false;
    var _timer = null;
    var _snake = null;
    var _food = null;
    var _isGameOver = false;

    SetupScript();

    function Draw() {
        _canvas.clearCanvas();
        _snake.draw();
        _food.draw();
        _grid.draw();
        DrawScore();
        DrawBorder();

        if (_isGameOver) {
            Stop();
            ExecEvent(_events.ongameover);
        }
    }

    function DrawBackground() {
        _canvas.clearCanvas();
        _grid.draw();
        DrawScore();
        DrawBorder();
    }

    function DrawScore() {
        _canvas.drawText({
            text: "Score:",
            font: "10pt Verdana, sans-serif",
            fillStyle: _colors.text,
            align: "left",
            x: _borderSize.left,
            y: _borderSize.top + _grid.height() + 5,
            fromCenter: false
        });
        _canvas.drawText({
            text: _score.toString(),
            font: "10pt Verdana, sans-serif",
            fillStyle: _colors.text,
            strokeWidth: 2,
            align: "right",
            x: _borderSize.left + 50,
            y: _borderSize.top + _grid.height() + 5,
            fromCenter: false
        });
    }

    function DrawBorder() {
        _canvas.drawRect({
            x: _borderSize.left - 2,
            y: _borderSize.top - 2,
            width: _grid.width() + 4,
            height: _grid.height() + 4,
            fromCenter: false,
            strokeStyle: _colors.border,
            strokeWidth: 1
        });
    }

    function OnKeyDown(event) {
        if (_ongoing) {
            var newDirection = null;

            switch (event.keyCode) {
                case Keys.Left:
                    newDirection = Direction.Left;
                    break;
                case Keys.Right:
                    newDirection = Direction.Right;
                    break;
                case Keys.Up:
                    newDirection = Direction.Up;
                    break;
                case Keys.Down:
                    newDirection = Direction.Down;
                    break;
            }

            _snake.setDirection(newDirection);
        }
    }

    function Score() {
        return _score;
    }

    function Start() {
        if (_timer != null) Stop();
        _timer = setInterval(Draw, _settings.refreshRate);

        _snake.start();
        _ongoing = true;
    }

    function Stop() {
        clearInterval(_timer);
        _timer = null;

        _ongoing = false;
    }

    function Reset() {
        Stop();
        _score = 0;
        _snake.reset();
        _isGameOver = false;
        _food.init();
        DrawBackground();
    }

    function OnSnakeEat() {
        _score += _settings.scorePerFood;
    }

    function OnGameOver() {
        _isGameOver = true;
    }

    function Initialize(settings) {
        _grid = new SnakeNamespace.SnakeGrid(_canvas);
        _grid.init({
            size: _settings.gridSize,
            x: _borderSize.left,
            y: _borderSize.top,
            maxRow: _settings.maxRow,
            maxColumn: _settings.maxColumn
        });

        _snake = new SnakeNamespace.Snake(_grid);
        _snake.oneat(OnSnakeEat);
        _snake.onover(OnGameOver);

        _food = new SnakeNamespace.SnakeFood(_grid);
        _food.setSnake(_snake);
        _food.init();

        $(document).keydown(OnKeyDown);
        $.extend(_settings, settings);

        _canvas.attr({
            width: _borderSize.left + _grid.width() + _borderSize.right,
            height: _borderSize.top + _grid.height() + _borderSize.bottom
        });
        DrawBackground();
    }

    function SetupScript() {
       	//  var src = $('script[src$="snakegame.js"]').attr("src");
		var src = "/comum/games/jssnake/scripts/snakegame.js";
        var idx = src.lastIndexOf("/") + 1;
        // var path = src.substring(0, idx);
		var path = "/comum/games/jssnake/scripts/";

        if (typeof (SnakeNamespace.Snake) === 'undefined') AddScript(path + "snake.js");
        if (typeof (SnakeNamespace.SnakeGrid) === 'undefined') AddScript(path + "snakegrid.js");
        if (typeof (SnakeNamespace.SnakeFood) === 'undefined') AddScript(path + "snakefood.js");
    }

    function AddScript(src) {
        var script = $("<script>");

        script.attr("src", src);
        $("head").append(script);
    }

    var _instance = {
        score: Score,
        init: Initialize,
        start: Start,
        stop: Stop,
        reset: Reset,
        ongameover: function (event) {
            if (typeof event === 'function') _events.ongameover.push(event);
        }
    };

    return _instance;
};