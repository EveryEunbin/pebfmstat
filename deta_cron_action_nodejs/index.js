const { Octokit } = require("octokit");
const { app } = require('deta');
require('dotenv').config()

const octokit = new Octokit({
    auth: process.env.GITHUB_TOKEN
});

app.lib.cron(async (event) => {
    try {
        await octokit.request("POST /repos/{owner}/{repo}/dispatches", {
            owner: "EveryEunbin",
            repo: "pebfmstat",
            headers: {
                "authorization": `token ${process.env.GITHUB_TOKEN}`,
                "accept": "application/vnd.github.v3+json",
            },
            data: {
                "event_type": "run_from_rest_api"
            }
        });
    } catch (error) {
        console.log(`Error! Status: ${error.status}. Message: ${error.response.data.message}`)
    }
    
    const date = new Date();
    return `running on a schedule ${date.toUTCString()}`
});

module.exports = app;
