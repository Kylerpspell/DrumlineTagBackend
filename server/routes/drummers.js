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

// get drummer by id
drummerRoutes.route("/drummers/:id").get(function (req, res) {
  console.log("GET /drummers/:id");
  let db_connect = dbo.getDb("drumlineData");
  let myquery = { _id: ObjectId(req.params.id) };
  db_connect.collection("drummers").findOne(myquery, function (err, result) {
	if (err) throw err;
	res.json(result);
  });
});

// add a drummer
drummerRoutes.route("/drummers/add").post(function (req, res) {
	console.log("POST /drummers/add");
	let db_connect = dbo.getDb("drumlineData");
	
	optionalYear = req.body.year;
	if (optionalYear == '') {
		optionalYear = "N/A";
	}

	optionalSection = req.body.section;
	if (optionalSection == '') {
		optionalSection = "N/A";
	}
	
	let myobj = {
		name: req.body.name,
		year: optionalYear,
		section: optionalSection,
		isMostWanted: false,
	};
	db_connect.collection("drummers").insertOne(myobj, function (err, result) {
		if (err) throw err;
		res.json(result);
	});
});

// Delete a drummer
drummerRoutes.route("/drummers/:id/remove").delete(function (req, res) {
	console.log("DELETE /drummers/:id");
	let db_connect = dbo.getDb("drumlineData");
	let myquery = { _id: ObjectId(req.params.id) };
	db_connect.collection("drummers").deleteOne(myquery, function (err, result) {
		if (err) throw err;
		res.json(result);
	});
});

// Update a drummer Section
drummerRoutes.route("/drummers/:id/updateSection").put(function (req, res) {
	console.log("PUT /drummers/:id/updateSection");
	let db_connect = dbo.getDb("drumlineData");
	let myquery = { _id: ObjectId(req.params.id) };
	let newvalues = { $set: { section: req.body.section } };
	db_connect.collection("drummers").updateOne(myquery, newvalues, function (err, result) {
		if (err) throw err;
		res.json(result);
	});
});

// Update a drummer Year
drummerRoutes.route("/drummers/:id/updateYear").put(function (req, res) {
	console.log("PUT /drummers/:id/updateYear");
	let db_connect = dbo.getDb("drumlineData");
	let myquery = { _id: ObjectId(req.params.id) };
	let newvalues = { $set: { year: req.body.year } };
	db_connect.collection("drummers").updateOne(myquery, newvalues, function (err, result) {
		if (err) throw err;
		res.json(result);
	});
});

// Update a drummer isMostWanted
drummerRoutes.route("/drummers/:id/updateIsMostWanted").put(function (req, res) {
	console.log("PUT /drummers/:id/updateIsMostWanted");
	let db_connect = dbo.getDb("drumlineData");
	let myquery = { _id: ObjectId(req.params.id) };
	let newvalues = { $set: { isMostWanted: req.body.isMostWanted } };
	db_connect.collection("drummers").updateOne(myquery, newvalues, function (err, result) {
		if (err) throw err;
		res.json(result);
	});
});

// reset a drummer
drummerRoutes.route("/drummers/:id/reset").put(function (req, res) {
	console.log("PUT /drummers/:id/reset");
	let db_connect = dbo.getDb("drumlineData");
	let myquery = { _id: ObjectId(req.params.id) };
	let newvalues = { $set: { numtags: 0, numtagged: 0 } };
	db_connect.collection("drummers").updateOne(myquery, newvalues, function (err, result) {
		if (err) throw err;
		res.json(result);
	});
});

module.exports = drummerRoutes;