const dialogflow = require("dialogflow").v2beta1;
const uuid = require("uuid");
const projectId = "chat-to-eu-hbadgs"

runSample = msg => {
    const sessionClient = new dialogflow.SessionsClient();
    const sessionPath = sessionClient.sessionPath(projectId, uuid.v4());
    const request = {
        session: sessionPath,
        queryInput: {
            text: {
                text: msg,
                languageCode: "en"
            }
        }
    };
    return sessionClient.detectIntent(request);
}

exports.handler = (req, res) => {
    res.set('Access-Control-Allow-Origin', '*');

    if (req.method === 'OPTIONS') {
        res.set('Access-Control-Allow-Methods', 'GET');
        res.set('Access-Control-Allow-Headers', 'Content-Type');
        res.set('Access-Control-Max-Age', '3600');
        res.status(204).send('');
    } else {
        runSample(req.body.msg).then(val => { res.send(val[0].queryResult.fulfillmentMessages[0].text) });;
    }
};
