const dialogflow = require("dialogflow").v2beta1;
const uuid = require("uuid");
const express = require('express');
var cors = require('cors')
const app = express();
const port = 5000;
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

app.use(express.json());
app.use(cors());

app.put('/chatbot', (req, res) => {
  runSample(req.body.msg).then(val => { res.json(val[0].queryResult.fulfillmentMessages[0].text) });;
});


app.listen(port, () => console.log(`Listening on port ${port}`))
