const BASE_PATH = "/rest/";

var http = require("http");

exports.create = function(host, maxPageSize, modelsSaversMap) {
    var
    // private:
    onEndCallback = null,

    // public:
    _onEnd = function(callback) {
        onEndCallback = callback;
    },
    _start = function() {
        var modelName,
            modelCounter = 0,
            saver,
            handler;

        // For every "modelName", start fetching
        for (modelName in modelsSaversMap) {
            ++modelCounter;

            console.info("*** Downloading model #%d: %s ***", modelCounter, modelName)

            // prepare "saver" and "fetch handler"
            saver = modelsSaversMap[modelName];
            handler = createFetchContentPageHandler(host, modelName, saver, maxPageSize, function() {
                --modelCounter;

                if (modelCounter === 0) {
                    console.info("*** Finished downloading all Models ***");
                    onEndCallback(null);
                } else {
                    console.info("*** Still %d models to go ***", modelCounter);
                }
            });

            // fetch the first page
            fetchContentPage(host, modelName, 0, maxPageSize, handler);
        }
    };

    return {
        onEnd : _onEnd,
        start : _start
    }
};

function fetchContentPage(host, modelName, offset, maxPageSize, callback) {
    http.get({
        "host"      : host,
        "port"      : 80,
        "method"    : "GET",
        "path"      : BASE_PATH + modelName +
            "?ordering=published" +
            "&offset=" + offset +
            "&page_size=" + maxPageSize,
        "headers"   : {
            "Accept"            : "application/json;charset=UTF-8",
            "Accept-Charset"    : "UTF-8"
        }
    },
    function(res) {
        var responseBody = "";

        res.on("data", function(chunk) {
            responseBody += chunk;
        });
        res.on("end", function() {
            var page = JSON.parse(responseBody);

            console.debug("Content JSON fetched (size: %d, offset: %d)", page["list"][modelName].length, page["list"]["@offset"]);
            callback(null, page);
        });
    })
    .on("error", function(e) {
        console.error(e.message);
        callback(e);
    });
}

function createFetchContentPageHandler(host, modelName, saver, maxPageSize, callback) {
    var handler = function(err, page) {
        var i, pageOffset;

        for (i = page["list"][modelName].length -1; i >= 0; --i) {
            // Save
            saver.save(page["list"][modelName][i]);
        }

        // Check if an Offset was provided and, if so, schedule a new fetch
        pageOffset = parseInt(page["list"]["@offset"]);
        if (!isNaN(pageOffset) && isFinite(pageOffset)) {
            fetchContentPage(host, modelName, pageOffset, maxPageSize, handler);
        } else {
            callback(null);
        }
    };

    return handler;
}
