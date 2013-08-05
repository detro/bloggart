#!/usr/local/bin/node

const MAX_PAGE_SIZE = 50;

var host = null,
    modelsSavers = null,
    destDir = null,
    downloader = null;

require("./console++.js");

if (process.argv.length !== 4) {
    console.log("\nUsage:\n   %s %s %s", __filename, "BLOG_HOSTNAME", "DESTINATION_DIR\n");
    process.exit(1);
} else {
    host = process.argv[2];
    destDir = process.argv[3];
}

// Configure Model-Savers Map
modelsSavers = {
    "post" : require("./content_saver.js").create(destDir + "/posts_archive", [
        "path",     //< convert to "slug" if available
        "updated",
        "published",
        "tags",
        "title",    //< +body, +body_markup (to extension), +slug (from title - to filename)
    ], "post", "detro"),
    "page" : require("./content_saver.js").create(destDir + "/pages_archive", [
        "path",     //< convert to "slug" if available
        "updated",
        "published",
        "title",    //< +body, +body_markup (to extension), +slug (from title - to filename)
    ], "page", "detro")
};

// Configure Downloader
downloader = require("./content_downloader.js").create(host, MAX_PAGE_SIZE, modelsSavers);
downloader.onEnd(function() {
    console.info("ALL DONE!");
    process.exit();
});

downloader.start();

