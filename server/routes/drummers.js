const express = require("express");


const drummerRoutes = express.Router();
const dbo = require("../db/conn");
const ObjectId = require("mongodb").ObjectId;

// get all drummers
drummerRoutes.route("/drummers").get(function (req, res) {
	  console.log("GET /drummers");
	  let db_connect = dbo.getDb("drumlineData");
	  db_connect.collection("drummers").find({}).toArray(function (err, result) {
			if (err) throw err;
			res.json(result);
		});
	});

module.exports = drummerRoutes;