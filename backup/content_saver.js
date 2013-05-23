exports.create = function(dir, props) {
    var
    fs = require('fs'),

    // public:
    _save = function(contentJson) {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir);
        }
        var fname = new Date(Date.parse(contentJson.published)).getTime() + "",
            fdesc = fs.openSync(dir + "/" + fname + ".md", "w+"),
            i;

        console.info("Storing Content to file: %s", fname);

        // Process "props" in the given content
        for (i = props.length -1; i >= 0; --i) {
            if (contentJson.hasOwnProperty(props[i])) {
                console.debug("   - %s: %s", props[i], normalizeContent(props[i], contentJson[props[i]]));
                fs.writeSync(fdesc, props[i] + ": " + normalizeContent(props[i], contentJson[props[i]]) + "\n");
            }
        }
        fs.writeSync(fdesc, "\n");

        // Process "body"
        if (contentJson.hasOwnProperty("body")) {
            console.debug("   - %s: ... (size: %d)", "body", contentJson["body"].length);

            // Wrap lines at 80 columns
            // FIXME: This truncates words - FIX THIS
            i = 0;
            do {
                fs.writeSync(fdesc, contentJson["body"].substr(i, 80) + "\n");
                i += 80;
            } while (i < contentJson["body"].length);
        }
        fs.closeSync(fdesc);
    };

    return {
        save : _save
    }
};

function normalizeContent(property, content) {
    switch(property) {
        case "tags":
            return Array.isArray(content.item) ? content.item.join(",") : content.item;
        case "published":
        case "updated":
            return new Date(Date.parse(content)).toISOString();
        default:
            return content;
    }
}
