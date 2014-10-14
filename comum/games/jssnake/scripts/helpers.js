
var Direction = {
    Up: 0,
    Down: 1,
    Left: 2,
    Right: 3
};

var Symbols = {
    circle: 0
};

var Point = (function () {

    function Equals(point1, point2) {
        return (point1.x == point2.x) && (point1.y == point2.y);
    }

    function Intersect(point, start, end) {
        var retVal = false;

        if (point.x == start.x && point.x == end.x) {
            if (IsBetween(point.y, start.y, end.y)) retVal = true;
        }

        if (point.y == start.y && point.y == end.y) {
            if (IsBetween(point.x, start.x, end.x)) retVal = true;
        }

        return retVal;
    }

    function IsBetween(value, min, max) {
        var retVal = false;

        if (min > max) {
            var tmp = min;

            min = max;
            max = tmp;
        }
        if (value >= min && value <= max) retVal = true;

        return retVal;
    }

    function Difference(point1, point2) {
        var retVal = {
            x: point2.x - point1.x,
            y: point2.y - point1.y
        };

        return retVal;
    }

    function GetDirection(start, end) {
        var retVal = null;

        if (start.x < end.x) retVal = Direction.Right;
        if (start.x > end.x) retVal = Direction.Left;
        if (start.y < end.y) retVal = Direction.Down;
        if (start.y > end.y) retVal = Direction.Up;

        return retVal;
    }

    var _instance = {
        equals: Equals,
        intersect: Intersect,
        diff: Difference,
        direction: GetDirection
    };

    return _instance;
})();

function ExecEvent(event, param) {
    $.each(event, function (index, value) {
        value(param);
    });
}