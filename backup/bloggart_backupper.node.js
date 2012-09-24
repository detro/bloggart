#!/usr/local/bin/node

var http = require("http"),
    ordering = "published",
    offset = 935,
    pageSize = 1,
    host = null,
    basePath = "/rest/",
    entities = ["post", "page"],
    destDir = null,
    url = null;

require("./console++.js");

if (process.argv.length !== 4) {
    console.warn(" Usage:\n  %s %s %s", __filename, "BLOG_URL", "DESTINATION_DIR\n");
    process.exit(1);
}

host = process.argv[2];
destDir = process.argv[3];

// "http://HOST/rest/post?offset=OFFSET&page_size=PAGE_SIZE&ordering=ORDERING"
http.get({
    "host" : host,
    "port" : 80,
    "method" : "GET",
    "path" : basePath + entities[0] +
        "?ordering=" + ordering +
        "&offset=" + offset +
        "&page_size=" + pageSize,
    "headers" : {
        "Accept" : "application/json"
    }
}, function(res) {
    var resBody = "";

    console.debug("StatusCode %d", res.statusCode);
    console.info("Headers %s", JSON.stringify(res.headers, null, "  "));
    res.on("data", function(chunk) {
        resBody += chunk;
    });
    res.on("end", function() {
        var resJSON = JSON.parse(resBody);
        console.warn("Response Body");
        console.error(JSON.stringify(resJSON, null, "  "));
    });
}).on("error", function(e) {
    console.error(e.message);
});

