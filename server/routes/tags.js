const express = require("express");


const tagRoutes = express.Router();
const dbo = require("../db/conn");
const ObjectId = require("mongodb").ObjectId;

// get all tags
tagRoutes.route("/tags").get(function (req, res) {
    console.log("GET /tags");
    let db_connect = dbo.getDb("drumlineData");
    db_connect.collection("tags").find({}).toArray(function (err, result) {
        if (err) throw err;
        res.json(result);
        });
    });


// add a tag
tagRoutes.route("/tags/add").post(function (req, res) {
    console.log("POST /tags/add");
    let db_connect = dbo.getDb("drumlineData");
    let myobj = {
        tagger: req.body.tagger,
        tagged: req.body.tagged,
        date: req.body.date
    };

    db_connect.collection("tags").insertOne(myobj, function (err, result) {
        if (err) throw err;
        res.json(result);
    });
});

// get tags by tagger
tagRoutes.route("/tags/tagger/:id").get(function (req, res) {
    console.log("GET /tags/:id");
    let db_connect = dbo.getDb("drumlineData");
    let myquery = { tagger: req.params.id };
    db_connect.collection("tags").find(myquery).toArray(function (err, result) {
        if (err) throw err;
        res.json(result);
    });
});

// get tags by tagged
tagRoutes.route("/tags/tagged/:id").get(function (req, res) {
    console.log("GET /tags/:id");
    let db_connect = dbo.getDb("drumlineData");
    let myquery = { tagged: req.params.id };
    db_connect.collection("tags").find(myquery).toArray(function (err, result) {
        if (err) throw err;
        res.json(result);
    });
});

// Delete a tag
tagRoutes.route("/tags/:id/remove").delete(function (req, res) {
    console.log("DELETE /tags/:id");
    let db_connect = dbo.getDb("drumlineData");
    let myquery = { _id: ObjectId(req.params.id) };
    db_connect.collection("tags").deleteOne(myquery, function (err, result) {
        if (err) throw err;
        res.json(result);
    });
});



module.exports = tagRoutes;