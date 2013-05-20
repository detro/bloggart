exports.create = function(dir, props) {
    var

    // public:
    _save = function(contentJson) {
        var i;

        console.info("Storing Content...");

        // Process "props" in the given content
        for (i = props.length -1; i >= 0; --i) {
            if (contentJson.hasOwnProperty(props[i])) {
                console.debug("   - %s: %s", props[i], contentJson[props[i]]);
            }
        }

        // Process "body"
        if (contentJson.hasOwnProperty("body")) {
            console.debug("   - %s: ... (size: %d)", "body", contentJson["body"].length);
        }
    };

    return {
        save : _save
    }
};
