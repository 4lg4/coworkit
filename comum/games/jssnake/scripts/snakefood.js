/// <reference path="jquery-1.9.1.js" />
/// <reference path="helpers.js" />
/// <reference path="snake.js" />
/// <reference path="snakegrid.js" />

(function (namespace) {
    var SnakeFood = function (grid) {

        var _grid = grid;
        var _snake = null;
        var _current = {
            point: {
                x: 0,
                y: 0
            }
        };
        var _isEaten = false;

        function SetSnake(snake) {
            _snake = snake;
            _snake.onmove(OnSnakeMove);
        }

        function Initialize() {
            GenerateFood();
        }

        function OnSnakeMove(data) {
            if (Point.equals(data, _current.point)) {
                _snake.eat();
                _isEaten = true;
            }
        }

        function GenerateFood() {
            var point = {};
            
            do {
                point = {
                    x: Math.floor((Math.random() * _grid.columnLimit()) + 1),
                    y: Math.floor((Math.random() * _grid.rowLimit()) + 1)
                };
            } while (!_grid.isEmpty(point));

            _current.point = point;
            _isEaten = false;
        }

        function Draw() {
            if (_isEaten) GenerateFood();
            _grid.drawSymbol(Symbols.circle, _current.point);
        }

        var _instance = {
            setSnake: SetSnake,
            draw: Draw,
            init: Initialize
        };

        return _instance;
    };

    namespace.SnakeFood = SnakeFood;

})(SnakeNamespace);