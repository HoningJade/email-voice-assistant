import React from "react";
import "./scoped.css";
import VoicEmail from "../../img/VoicEmail.png";
import FootImg from "../../img/foot.png";
import ChatBox from "../ChatBox/index";

const App = () => {
  return (
    <div className="App">
      <div className="container">
        <div className="nav-bar">
          {/* <img style={{height:50,paddingRight:15}} src={VoicEmail} alt="voicemail"></img> */}
          <div className="nav-text">— VoicEmail &#128231; —</div>
        </div>
        <div className="chat-box-container">
          <ChatBox></ChatBox>
        </div>
        <div id="footer">
          <ul class="copyright">
            <li>&copy; LinguAI.</li>
            <li>
              Src:{" "}
              <a href="https://github.com/xingjian-zhang/email-voice-assistant">
                GitHub Repo
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default App;
