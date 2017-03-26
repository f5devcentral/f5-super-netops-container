#!/usr/bin/env node
//TODO Check if internet connectivity exists, handle errors if not.
//sno_bootstrap.js
//get the Super-NetOps container up and runnning.

var http = require('https');
var fs = require('fs');
var git = require('/usr/lib/node_modules/simple-git');  // add node_modules path to NODE_PATH in Dockerfile
var npm = require('npm');
var noInputs = 0;  //Remove??
var DEBUG = true;
var base_dir = process.argv[2];

// Set defaults for initial load. These may be overriden during runtime by updateInputs();
var inputs = {
  "inputs_path":"/npearce/super-netops/develop/sno_inputs.json",
  "inputs_poll_interval":"60000",
  "local_base_path":"/home/"
};

//var sys = require('util');
var exec = require('child_process').exec;
var child;

function onStart() {

  console.log("Super-NetOps Enablement Program... \n Programmable Infrastructure for the Win!");

  var ifs = require('os').networkInterfaces();
  var clientIp = Object.keys(ifs)
    .map(x => ifs[x].filter(x => x.family === 'IPv4' && !x.internal)[0])
    .filter(x => x)[0].address;

  console.log("Super-NetOps Web Server running at: http://" +clientIp+ " \n\n \
  WANRING: On Docker for  Mac (and maybe Windows?) you must map this to a \n \
  local address:port using the '-p' option. For example, to map the containers \n \
  port 8080 to your localhost:8081 (e.g. to access via http://localhost:8081), \n \
  run the container using: \n \
     \'docker run -p 8081:8080 --rm -it super-netops\'");   //this doesn't work as require mapping on Mac. Check Windows.

}

if (DEBUG) {
  console.log('local_base_path: ' +inputs.local_base_path);
  console.log('sno_inputs: ' +JSON.stringify(inputs));
  console.log('sno_inputs.version: ' +inputs.version);
}

function updateContent() {
//TODO Handle error

  if (DEBUG) {  console.log("unptadeContent: inputs.gitRepos: " +JSON.stringify(inputs.gitRepos, ' ', '\t')); }
  if (DEBUG) {  console.log("unptadeContent: inputs.gitRepos: " +JSON.stringify(inputs.gitRepos, ' ', '\t')); }

  for (var i in inputs.gitRepos) {
    if (DEBUG) { console.log("name: " +inputs.gitRepos[i].name+ "  repo: " +inputs.gitRepos[i].repo+ " gitFile: " +inputs.gitRepos[i].gitFile); }
    //git(inputs.local_base_path).clone(inputs.gitRepos[i].gitFile, (inputs.local_base_path+inputs.gitRepos[i].repo));    // how do we overwrite....
  }
}


function updateInputs() {  //Retreives operational settings from git repo

  if (inputs.alive === "false") {
    console.log("Kill triggered. Exiting...");
    process.exit();
  }
  else {

    var options = {
      "method": "GET",
      "hostname": "raw.githubusercontent.com",
      "port": null,
      "path": inputs.inputs_path,
      "headers": {
        "cache-control": "no-cache"
      }
    };

    var req = http.request(options, function (res) {

      var chunks = [];

      res.on("data", function (chunk) {
        chunks.push(chunk);
      });

      res.on("end", function () {
        var body = Buffer.concat(chunks);
        inputs = JSON.parse(body);

        if (DEBUG == true) { console.log("DEBUG: inputs: " +JSON.stringify(inputs, ' ', '\t')) };

      });
    });

    req.on('error', function(err) {       //handle 'request' error

      console.log("Error reaching https://raw.githubusercontent.com" +inputs.inputs_path);
      console.log(err);

    });

    req.end();

    if (!inputs.alive) {   //Not yet reached the Inputs file.
      noInputs++;
      updateInputsTimeout = setTimeout( function () {
        updateInputs();
      }, 10000);  // Retry inputs.inputs_path in 10 seconds.
    }
    else {  //We phoned home!!! Time to 'do stuff'

      updateInputsTimeout = setTimeout( function () {  // Resetting the poll interval to that of new inputs value
        console.log("Checking for run-time updates in "+(inputs.inputs_poll_interval/60000)+" minutes....");
        updateInputs();
      }, inputs.inputs_poll_interval);  // Retry iot_client_inputs.json in 2 seconds.

      updateContent();  // We got internets. Time to clone the git repo's

    }
  }
}

onStart();
updateInputs();
//updateContent();  //Call this from within updateInputs, once successfully phone home...
