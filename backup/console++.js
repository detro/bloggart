/**
 * TODO
 */
var _ANSICODES = {
        'reset'     : '\033[0m',
        'bold'      : '\033[1m',
        'italic'    : '\033[3m',
        'underline' : '\033[4m',
        'blink'     : '\033[5m',
        'black'     : '\033[30m',
        'red'       : '\033[31m',
        'green'     : '\033[32m',
        'yellow'    : '\033[33m',
        'blue'      : '\033[34m',
        'magenta'   : '\033[35m',
        'cyan'      : '\033[36m',
        'white'     : '\033[37m'
    },
    _LEVELS     = {
        ERROR   : 0,
        WARN    : 1,
        INFO    : 2,
        DEBUG   : 3
    },
    _LEVELS_COLOR = [
        "red",
        "yellow",
        "cyan",
        "reset"
    ],
    _LEVELS_NAME = [
        "ERROR",
        "WARN",
        "INFO",
        "DEBUG"
    ],
    _console    = {
        error   : console.error,
        warn    : console.warn,
        info    : console.info,
        debug   : console.log,
        log     : console.log
    };

// Configuration
/** Possible logging levels */
console.LEVELS  = console.LEVELS || _LEVELS;
/** Logging level */
console.level   = console.level || console.LEVELS.DEBUG;
/** Colors enabled */
console.colored = console.colored || true;
/** Time added to logs entries */
console.timed   = console.timed || true;

/**
 * Take a string and apply console ANSI colors for expressions "#color{msg}"
 * NOTE: Does nothing if "console.colored === false".
 *
 * @param str Input String
 * @returns Same string but with colors applied
 */
var applyColors = function(str){
    var tag = /#([a-z]+)\{|\}/,
        cstack = [],
        matches = null,
        orig = null,
        name = null,
        code = null;

    while (tag.test(str))
    {
        matches = tag.exec(str);
        orig = matches[0];

        if (console.colored)
        {
            if (orig === '}')
                cstack.pop();
            else
            {
                name = matches[1];
                if (name in _ANSICODES)
                {
                    code = _ANSICODES[name];
                    cstack.push(code);
                }
            }

            str = str.replace(orig, _ANSICODES.reset + cstack.join(''));
        }
        else
            str = str.replace(orig, '');
    }
    return str;
};

/**
 * Decorate the Arguments passed to the console methods we override.
 * First element, the message, is now colored, timed and more (based on config).
 *
 * @param argsArray Array of Artuments to decorate
 * @param level Logging level to apply (regulates coloring and text)
 * @returns Array of Arguments, decorated.
 */
var decorateArgs = function(argsArray, level) {
    var args = Array.prototype.slice.call(argsArray, 1),
        msg = argsArray[0];

    if (console.timed === true) {
        msg = "[" + _LEVELS_NAME[level] + " - " + new Date().toJSON() + "] " + msg;
    }
    if (console.colored === true) {
        msg = "#" + _LEVELS_COLOR[level] + "{" + msg + "}";
        msg = applyColors(msg);
    }
    args.splice(0, 0, msg);

    return args;
};

// Overrides some key "console" Object methods
console.error = function() {
    if (arguments.length > 0 && this.level >= _LEVELS.ERROR) {
        _console.error.apply(this, decorateArgs(arguments, _LEVELS.ERROR));
    }
};
console.warn = function() {
    if (arguments.length > 0 && this.level >= _LEVELS.WARN) {
        _console.warn.apply(this, decorateArgs(arguments, _LEVELS.WARN));
    }
};
console.info = function() {
    if (arguments.length > 0 && this.level >= _LEVELS.INFO) {
        _console.info.apply(this, decorateArgs(arguments, _LEVELS.INFO));
    }
};
console.debug = function() {
    if (arguments.length > 0 && this.level >= _LEVELS.DEBUG) {
        _console.debug.apply(this, decorateArgs(arguments, _LEVELS.DEBUG));
    }
};
console.log = function() {
    if (arguments.length > 0 && this.level >= _LEVELS.DEBUG) {
        _console.log.apply(this, decorateArgs(arguments, _LEVELS.DEBUG));
    }
};

exports = console;
