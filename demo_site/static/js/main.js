/*
 * Use the DataProxy.post / DataProxy.jsonPost methods. This will ensure the savedData event gets triggered.
 */
var DataProxy = function () {
    $.ajax({ cache: false });

    this.classify = function(term, callback, error_callback) {
        var data = {};
        data.term = term;
        var url = '/api/classify';
        this.jsonPost({
            url: url,
            data: data,
            success: function (data) {
                callback(data);
            },
            error: error_callback
        });
    }

    this.correction = function(id, correction, callback, error_callback) {
        var data = {};
        data.id = id;
        data.correction = correction
        var url = '/api/correction';
        this.jsonPost({
            url: url,
            data: data,
            success: function (data) {
                callback(data);
            },
            error: error_callback
        });
    }

    this.jsonPost = function (cfg) {
        console.log(cfg.url);
        cfg.data = $.toJSON(cfg.data);
        cfg.contentType = 'application/json';
        cfg.cache = false;
        cfg.processData = false;

        // Default to post, but also allow this method to create delete and update requests.
        if (cfg.type === undefined)
            cfg.type = 'POST';

        $.ajax(cfg);
    };
};

var Proxy = new DataProxy();


var show_error = function() {
    $.notify('An error occurred, sorry :(');
};