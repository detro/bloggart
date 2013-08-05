exports.create = function(dir, props, layout, author) {
    var
    fs = require('fs'),

    // public:
    _save = function(contentJson) {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }
        var fname = normalizeFilename(contentJson),
            fdesc = fs.openSync(dir + "/" + fname + ".md", "w+"),
            i;

        console.info("Storing Content to file: %s", fname);

        // Process "props" in the given content
        fs.writeSync(fdesc, "---\n");
        fs.writeSync(fdesc, "layout: " + layout + "\n");
        fs.writeSync(fdesc, "author: " + author + "\n");
        fs.writeSync(fdesc, "published: true\n");
        for (i = props.length -1; i >= 0; --i) {
            if (contentJson.hasOwnProperty(props[i])) {
                console.debug("   - %s: %s", props[i], normalizeContent(props[i], contentJson[props[i]]));

                if (props[i] === "published") {
                    fs.writeSync(fdesc, "date" + ": " + normalizeContent(props[i], contentJson[props[i]]) + "\n");
                } if (props[i] === "path") {
                    fs.writeSync(fdesc, "permalink" + ": " + normalizeContent(props[i], contentJson[props[i]]) + "\n");
                } else {
                    fs.writeSync(fdesc, props[i] + ": " + normalizeContent(props[i], contentJson[props[i]]) + "\n");
                }
            }
        }
        fs.writeSync(fdesc, "---\n");
        fs.writeSync(fdesc, "\n");

        // Process "body"
        if (contentJson.hasOwnProperty("body")) {
            console.debug("   - %s: ... (size: %d)", "body", contentJson["body"].length);

            fs.writeSync(fdesc, contentJson["body"] + "\n");
        }
        fs.closeSync(fdesc);
    };

    return {
        save : _save
    }
};

function normalizeDate(d) {
    return "\""
        + d.getUTCFullYear()
        + "-" + pad(d.getUTCMonth()+1)
        + "-" + pad(d.getUTCDate())
        + " " + pad(d.getUTCHours())
        + ":" + pad(d.getUTCMinutes())
        + ":" + pad(d.getUTCSeconds())
        + "\"";
}

function normalizeContent(property, content) {
    var util = require("util");

    switch(property) {
        case "tags":
            return "[" + (Array.isArray(content.item) ? content.item.join(", ") : content.item) + "]";
        case "published":
        case "updated":
            return normalizeDate(new Date(Date.parse(content)));
        case "title":
            return "\"" + content + "\"";
        default:
            return content;
    }
}

function normalizeFilename(contentJson) {
    var d = new Date(Date.parse(contentJson.published));

    return d.getUTCFullYear()
        + "-" + pad(d.getUTCMonth()+1)
        + "-" + pad(d.getUTCDate())
        + "-" + slug(contentJson.title);
}

function slug(str)
{
    str = str.toLowerCase();
    str = str.replace(/[^a-z0-9]+/g, '-');
    str = str.replace(/^-|-$/g, '');
    return str;
}

function pad(n) {
    return n < 10 ? '0' + n : n;
}
