/// <reference path="jquery-1.9.1.js" />
/// <reference path="jcanvas.js" />
/// <reference path="snakegrid.js" />
/// <reference path="helpers.js" />

(function (namespace) {
    var Snake = function (grid) {

        var _grid = grid;
        var _settings = {
            start: {
                x: 0,
                y: 0
            },
            length: 10,
            direction: Direction.Right,
            growSize: 3,
            growInterval: 5
        };
        var _current = {
            end: {
                x: 0,
                y: 0
            },
            joints: [],
            isOver: false,
            hasMoved: false
        };
        var _events = {
            onmove: [],
            onover: [],
            oneat: []
        };
        var _foodEaten = 0;
        var _growLength = 0;
        var _errTry = 3;

        Initialize(_settings);

        function Initialize(settings) {
            var x = 0, y = 0;

            if (typeof settings != "undefined") $.extend(_settings, settings);
            _current = $.extend({}, _current, _settings);

            var len = _current.length - 1;

            switch (_current.direction) {
                case Direction.Right:
                    x = _current.start.x - len;
                    y = _current.start.y;
                    break;
                case Direction.Left:
                    x = _current.start.x + len;
                    y = _current.start.y;
                    break;
                case Direction.Up:
                    x = _current.start.x;
                    y = _current.start.y + len;
                    break;
                case Direction.Down:
                    x = _current.start.x;
                    y = _current.start.y - len;
                    break;
            }
            _current.end.x = x;
            _current.end.y = y;
        }

        function Reset() {
            _foodEaten = 0;
            _growLength = 0;
            _errTry = 3;
            _current.hasMoved = false;
            _current.isOver = false;
            _current.joints = [];
            _current.direction = Direction.Right;
            Initialize();
        }

        function SetDirection(direction) {

            if (_current.direction != direction) {
                var isValidRoute = false;

                switch (_current.direction) {
                    case Direction.Up:
                    case Direction.Down:
                        switch (direction) {
                            case Direction.Left:
                            case Direction.Right:
                                isValidRoute = true;
                                break;
                        }
                        break;
                    case Direction.Left:
                    case Direction.Right:
                        switch (direction) {
                            case Direction.Up:
                            case Direction.Down:
                                isValidRoute = true;
                                break;
                        }
                        break;
                }

                if (isValidRoute) {
                    var coords = $.extend({}, _current.start);

                    _current.joints.unshift(coords);
                    _current.direction = direction;
                    Move();
                }
            }
        }

        function Move() {
            if (!_current.isOver && !_current.hasMoved) {
                var start = $.extend({}, _current.start);
                var end = $.extend({}, _current.end);
                var lastJoint = _current.joints[_current.joints.length - 1];

                switch (_current.direction) {
                    case Direction.Up:
                        start.y--;
                        break;
                    case Direction.Down:
                        start.y++;
                        break;
                    case Direction.Left:
                        start.x--;
                        break;
                    case Direction.Right:
                        start.x++;
                        break;
                }

                if (_growLength == 0) {
                    var tailDirection = null;

                    if (_current.joints.length > 0) {
                        tailDirection = Point.direction(end, lastJoint);
                    } else {
                        tailDirection = Point.direction(end, start);
                    }

                    switch (tailDirection) {
                        case Direction.Up:
                            end.y--;
                            break;
                        case Direction.Down:
                            end.y++;
                            break;
                        case Direction.Left:
                            end.x--;
                            break;
                        case Direction.Right:
                            end.x++;
                            break;
                    }
                } else {
                    _growLength--;
                }

                if (IsMoveValid(start)) {
                    _current.start = start;
                    _current.end = end;

                    if (_current.joints.length > 0) {
                        if (Point.equals(end, lastJoint)) {
                            _current.joints.pop();
                        }
                    }
                    _errTry = 3;

                    var param = $.extend({}, _current.start);

                    ExecEvent(_events.onmove, param);
                } else {
                    if (_errTry == 0) {
                        ExecEvent(_events.onover);
                        _current.isOver = true;
                    }
                    _errTry--;
                }
            }
            _current.hasMoved = true;
        }

        function IsMoveValid(point) {
            var isValid = true;

            if (point.x < 0) isValid = false;
            if (point.x > _grid.columnLimit()) isValid = false;
            if (point.y < 0) isValid = false;
            if (point.y > _grid.rowLimit()) isValid = false;

            if (_current.joints.length >= 3 && isValid) {
                var lastIndex = _current.joints.length - 1;

                $.each(_current.joints, function (index, value) {
                    if (index >= 2) {
                        var start = value;
                        var end = null;

                        if (index < lastIndex) {
                            end = {
                                x: _current.joints[index + 1].x,
                                y: _current.joints[index + 1].y
                            };
                        } else {
                            end = _current.end;
                        }

                        if (Point.intersect(point, start, end)) {
                            isValid = false;
                            return false;
                        }
                    }
                });
            }

            return isValid;
        }

        function Draw() {
            Move();

            _grid.drawPoint(_current.start);
            if (_current.joints.length > 0) {
                var lastIndex = _current.joints.length - 1;

                end = _current.joints[0];
                _grid.drawLine(_current.start, _current.joints[0]);

                $.each(_current.joints, function (index, value) {
                    if (index < lastIndex) _grid.drawLine(value, _current.joints[index + 1]);
                    _grid.drawPoint(value);
                });

                _grid.drawLine(_current.joints[lastIndex], _current.end);
                _grid.drawPoint(_current.end);
            } else {
                _grid.drawLine(_current.start, _current.end);
                _grid.drawPoint(_current.end);
            }
            _current.hasMoved = false;
        }

        function Start() {
            Move();
        }

        function Eat(food) {
            _foodEaten++;
            if (_foodEaten == _current.growInterval) {
                _growLength = _current.growSize;
                _foodEaten = 0;
            }
            ExecEvent(_events.oneat);
        }

        var _instance = {
            draw: Draw,
            setDirection: SetDirection,
            init: Initialize,
            start: Start,
            eat: Eat,
            reset: Reset,
            onmove: function (event) {
                if (typeof event === 'function') _events.onmove.push(event);
            },
            onover: function (event) {
                if (typeof event === 'function') _events.onover.push(event);
            },
            oneat: function (event) {
                if (typeof event === 'function') _events.oneat.push(event);
            }
        };

        return _instance;
    };

    namespace.Snake = Snake;

})(SnakeNamespace);