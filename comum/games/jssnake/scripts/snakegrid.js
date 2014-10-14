/// <reference path="jquery-1.9.1.js" />
/// <reference path="jcanvas.js" />
/// <reference path="helpers.js" />

(function (namespace) {
    var SnakeGrid = function (canvas) {

        var _colors = {
            marker: "#656767",
            border: "#3D3E3E",
            gridlines: "#DADDDD"
        };
        var _settings = {
            size: 10,
            maxRow: 50,
            maxColumn: 50,
            x: 0,
            y: 0
        };
        var _width = 0;
        var _height = 0;
        var _canvas = canvas || $("canvas");
        var _marks = [];
        var _symbols = [];

        function Initialize(settings) {
            if (typeof settings != "undefined") $.extend(_settings, settings);

            _width = _settings.maxColumn * _settings.size;
            _height = _settings.maxRow * _settings.size;
        }

        function Width() {
            return _width;
        }

        function Height() {
            return _height;
        }

        function RowLimit() {
            return _settings.maxRow - 1;
        }

        function ColumnLimit() {
            return _settings.maxColumn - 1;
        }

        function DrawGrid() {
            var yCoord = 0, xCoord = 0;

            for (var i = 0; i <= _settings.maxColumn; i++) {
                if (i == 0) {
                    xCoord = _settings.x;
                    yCoord = _settings.y;
                } else {
                    xCoord += _settings.size;
                }
                _canvas.drawLine({
                    strokeStyle: _colors.gridlines,
                    strokeWidth: 1,
                    x1: xCoord,
                    y1: yCoord,
                    x2: xCoord,
                    y2: yCoord + _height
                });
            }

            for (var i = 0; i <= _settings.maxRow; i++) {
                if (i == 0) {
                    xCoord = _settings.x;
                    yCoord = _settings.y;
                } else {
                    yCoord += _settings.size;
                }
                _canvas.drawLine({
                    strokeStyle: _colors.gridlines,
                    strokeWidth: 1,
                    x1: xCoord,
                    y1: yCoord,
                    x2: xCoord + _width,
                    y2: yCoord
                });
            }
        }

        function Draw() {
            $.each(_marks, function (index, value) {
                DrawMark(value);
            });
            _marks = [];

            $.each(_symbols, function (index, value) {
                DrawSymbol(value);
            });
            _symbols = [];

            DrawGrid();
        }

        function Mark(point) {
            var coords = $.extend({}, point);

            _marks.push(coords);
        }

        function DrawMark(point) {
            if (IsValid(point)) {
                var xCoord = _settings.x + (point.x * _settings.size);
                var yCoord = _settings.y + (point.y * _settings.size);
                var fillColor = _colors.marker;

                _canvas.drawRect({
                    strokeStyle: _colors.gridlines,
                    fillStyle: fillColor,
                    x: xCoord,
                    y: yCoord,
                    width: _settings.size,
                    height: _settings.size,
                    fromCenter: false
                });
            }
        }

        function DrawSymbol(symbol) {
            if (IsValid(symbol)) {
                var mid = _settings.size / 2;
                var xCoord = _settings.x + (symbol.x * _settings.size);
                var yCoord = _settings.y + (symbol.y * _settings.size);
                var fillColor = _colors.marker;

                switch (symbol.type) {
                    case Symbols.circle:
                        _canvas.drawArc({
                            radius: mid - 1,
                            fillStyle: fillColor,
                            x: xCoord + mid,
                            y: yCoord + mid
                        });
                        break;
                }
            }
        }

        function DrawLine(start, end) {
            var diff = Point.diff(start, end);
            var coords = {
                x: 0,
                y: 0
            };

            if (diff.x == 0) {
                var y = end.y;

                if (diff.y < 0) {
                    diff.y = Math.abs(diff.y);
                    y = start.y;
                }
                coords.x = start.x;
                coords.y = y;

                diff.y--;
                while (diff.y > 0) {
                    coords.y = y - diff.y;
                    Mark(coords);
                    diff.y--;
                }
            } else if (diff.y == 0) {
                var x = end.x;

                if (diff.x < 0) {
                    diff.x = Math.abs(diff.x);
                    x = start.x;
                }
                coords.x = x;
                coords.y = start.y;

                diff.x--;
                while (diff.x > 0) {
                    coords.x = x - diff.x;
                    Mark(coords);
                    diff.x--;
                }
            }
        }

        function MarkSymbol(type, point) {
            var symbol = {
                x: point.x,
                y: point.y,
                type: type
            };

            _symbols.push(symbol);
        }

        function IsEmpty(point) {
            var retVal = true;

            if (IsValid(point)) {
                if ($.inArray(point, _marks) > 0) retVal = false;
                if (!retVal) {
                    $.each(_symbols, function (index, value) {
                        if (Point.equals(point, value)) {
                            retVal = false;
                            return false;
                        }
                    });
                }
            } else {
                retVal = false;
            }

            return retVal;
        }

        function IsValid(point) {
            var retVal = true;

            if (point.x < 0) retVal = false;
            if (point.y < 0) retVal = false;
            if (point.x > _instance.columnLimit()) retVal = false;
            if (point.y > _instance.rowLimit()) retVal = false;

            return retVal;
        }

        var _instance = {
            init: Initialize,
            width: Width,
            height: Height,
            draw: Draw,
            drawPoint: Mark,
            drawLine: DrawLine,
            drawSymbol: MarkSymbol,
            rowLimit: RowLimit,
            columnLimit: ColumnLimit,
            isEmpty: IsEmpty
        };

        return _instance;
    };

    namespace.SnakeGrid = SnakeGrid;

}) (SnakeNamespace);