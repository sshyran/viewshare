define([
    "jquery", "exhibit", "./freemix"
], function($, Exhibit, Freemix) {
    "use strict";


    function createDatabase() {
        var database = Exhibit.DatabaseUtilities.create();
//        if (database._properties) {
//            var ns = "http://simile.mit.edu/2006/11/exhibit#";
//            var ps = database._properties;
//            if (ps.change && typeof ps.change._uri == 'undefined') {
//                database._properties.change._uri=ns+"changed";
//            }
//            if (ps.changedItem && typeof ps.changedItem._uri == 'undefined') {
//                database._properties.changedItem._uri=ns+"changedItem";
//            }
//            if (ps.modified && typeof ps.modified._uri == 'undefined') {
//                database._properties.modified._uri=ns+"modified";
//            }
//        }
        return database;

    }

    Freemix.exhibit = {

        initializeDatabase: function(data, fDone) {

            var database = Freemix.exhibit.database = createDatabase();

            if (data.constructor == Array) {
                if (fDone) {
                    $(document.body).one("dataload.exhibit", fDone);
                }
                database._loadLinks(data, database);

            } else {
                database.loadData(data);
                if (fDone) fDone();
            }
            return database;
        },
        createExhibit: function(root) {
            var exhibit;
            exhibit = Exhibit.create(Freemix.exhibit.database);
            exhibit.configureFromDOM(root.get(0));
            return exhibit;
        }
    };
});
