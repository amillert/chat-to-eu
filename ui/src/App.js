import React from 'react';

const CHATBOT_ENDPOINT = "http://localhost:5000/chatbot"
const USER_MSG = "user"
const CHATBOT_MSG = "chatbot"

export default class App extends React.Component {
  state = {
    messages: [],
  }
  render() {
    const sendToChatbot = msg => {
      fetch(CHATBOT_ENDPOINT, {
        method: 'PUT',
        body: JSON.stringify({ msg: msg }),
        headers: { "Content-type": "application/json; charset=UTF-8" }
      }).then(res => { return res.json() }).then(json => {
        this.setState({ messages: [...this.state.messages, { msg: json.text[0], type: CHATBOT_MSG }] });
      })
    }
    const sendMsg = e => {
      e.preventDefault();
      let msg = e.target.elements.input.value;
      this.setState({ messages: [...this.state.messages, { msg: msg, type: USER_MSG }] });
      sendToChatbot(msg);
      e.target.reset();
    }
    return (
      <section className="hero is-fullheight">
        <div className="hero-head">
          <header className="hero is-link is-bold">
            <div className="hero-body has-background-link">
              <div className="container">
                <p className="title"> Chat to EU </p>
                <p className="subtitle">chatbot made during hackyeah by Albert Millert & Wojciech Niedbała</p>
              </div>
            </div>
          </header>
        </div>
        <div className="hero-body"><Messages messages={this.state.messages} /></div>
        <form onSubmit={(e) => sendMsg(e)}>
          <div className="field has-addons">
            <div className="control is-expanded">
              <input className="input" name="input" type="text" placeholder="Ask chatbot" />
            </div>
            <div className="control">
              <button className="button is-link">Send</button>
            </div>
          </div>
        </form>
      </section>
    )
  }
}

const Messages = ({ messages }) => {
  return (
    <div style={{ heigth: '100%', width: '100%' }}>
      {messages.map((m, i) => {
        const userMsg = m.type === USER_MSG
        return (
          <div key={i} style={{ padding: '.25em', textAlign: userMsg ? 'left' : 'right', overflowWrap: 'normal' }}>
            <span key={i} className={userMsg ? 'is-medium tag is-info' : 'is-small content'}>{m.msg}</span>
          </div>
        )
      }
      )}
    </div>
  );
};