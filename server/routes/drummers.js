const express = require('express');
const drummerRoutes = express.Router();
const ObjectId = require('mongodb').ObjectID;
const dbo = require("../db/conn");


drummerRoutes.route('/drummers').get(async function (req, res) {
    let dbConnect = dbo.getDb();
    dbConnect.collection('drummers').find({}).toArray(function (err, result) {
        if (err) throw err;
        res.json(result);
    });
});

module.exports = drummerRoutes;