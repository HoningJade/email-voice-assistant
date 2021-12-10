import React, { useState, useEffect, useRef } from 'react';
import './scoped.css';
// import RobIcon from '../../img/RobIcon.png';
// import UserIcon from '../../img/UserIcon.png';
import BoyIcon from '../../img/Boy.jpeg';
import GirlIcon from '../../img/Girl.jpeg';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { AudioOutlined } from '@ant-design/icons';
import axios from 'axios';

const ChatBox = () => {
  const {
    transcript,
    finalTranscript,
    resetTranscript,
  } = useSpeechRecognition();
  const chatRef = useRef(null);
  const [isBlocked, setIsBlocked] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [msg, setMsg] = useState([]);
  const [speaker, setSpeaker] = useState([]); //0 for assistant, 1 for user
  navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);
  useEffect (() => {
    navigator.getUserMedia({ audio: true },
      () => {
        console.log('Permission Granted');
        setIsBlocked(false);
      },
      () => {
        console.log('Permission Denied');
        setIsBlocked(true);
      },
    );
    var openMsg =
      "Hi, I am your intelligent voice email assistant. What can I help you?";
    setMsg([openMsg]);
    setSpeaker([0]);
    setTimeout(() => {
      var voices = speechSynthesis.getVoices();
      var msg = new SpeechSynthesisUtterance(openMsg);
      if (voices.length === 0) {
          window.speechSynthesis.addEventListener("voiceschanged", () => {
          voices = speechSynthesis.getVoices();
          msg.voice = voices[49]; 
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(msg);
        })
      }
      else {
        msg.voice = voices[49]; 
        window.speechSynthesis.speak(msg);
      }
    }, 1000);
  }, [])

  async function speak(message) {
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance(message);
    var voices = window.speechSynthesis.getVoices();
    msg.voice = voices[49]; 
    window.speechSynthesis.speak(msg);
  }

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  function punctuate(string){
    // Punctuate according to rule
    const question = ["what", "who", "how", "when", "which", "whom", "whose", "why", "may", "can", "could"];
    var first_word = string.split(" ")[0];
    if (question.includes(first_word.toLowerCase())) {
      string += "?";
    } else {
      string += ".";
    }
    return string;
  }

  function generateResponse(bot) { // TODO - if
    // object with keys {body, bot_text_end, bot_text_start, sender, summary}).
    return (
      <div>
        {bot.bot_text_start} {bot.from && <text>This email is from {bot.from}.</text>} {bot.summary}  
        {bot.subject && <div className="mail-subject">{bot.subject}</div>}
        {bot.body && <div className="mail-message">{bot.body}</div>} 
        {bot.bot_text_end}
      </div>
    );
  }

  function generateText(bot) {
    var text = "";
    text += bot.bot_text_start + " ";
    if (bot.from) {
    text += " This email is from " + bot.from + ". ";
    };
    if (bot.summary) {
      text += " " + bot.summary;
    };
    if (bot.subject) {
      text += " The subject is " + bot.subject;
    };
    if (bot.body) {
      text += " The body is: " + bot.body;
    };
    if (bot.bot_text_end){
      text += bot.bot_text_end;
    };
    return text;
  }

  function removeLink(text) {
    if (text) {
      var new_text = text.replace(/<*(?:https?|ftp):\/\/[\n\S]+>*/g, '');
      return new_text;
    } else {
      return text;
    }
  }

  const startSpeak = () => {
    window.speechSynthesis.cancel();
    setIsRecording(true);
    resetTranscript();
    setMsg([...msg, '...']);
    setSpeaker([...speaker, 1]);
    SpeechRecognition.startListening({ language: 'en-US' });
  }
  
  const stopSpeak = async () => {
    setIsRecording(false);
    SpeechRecognition.stopListening();
    var trans = "";
    var trans_cur = String(transcript);
    var trans_final = String(finalTranscript);
    if (trans_final) {  // if the final transcript is ready, use the final one
      trans = trans_final;
    } else {
      trans = trans_cur;
    }
    console.log(trans);
    trans = punctuate(trans);
    trans = capitalizeFirstLetter(trans);
    trans = trans.replace("start","star");
    trans = trans.replace("rat","read");
    trans = trans.replace("female", "email");
    trans = trans.replace("hungry", "Hangrui");
    trans = trans.replace("henry", "Hangrui")
    trans = trans.replace("hungray", "Hangrui")
    trans = trans.replace("Mass", "math")
    trans = trans.replace("Caillou", "Can you")
    trans = trans.replace("nearest", "next")
    trans = trans.replace("Starburst", "star this email")
    trans = trans.replace("nest","next")
    trans = trans.replace("stop", "star")
    trans = trans.replace("Start", "Star")
    trans = trans.replace("Stop", "Star")
    trans = trans.replace("mass", "math")
    trans = trans.replace("nasty", "next")
    trans = trans.replace("Sorry", "Star")
    trans = trans.replace("positioning", "position")
    trans = trans.replace("mass", "math")
    trans = trans.replace("publishing", "position")
    trans = trans.replace("style","star")
    trans = trans.replace("Not","mark")
    



    var msgArr = [...msg.slice(0,-1), trans];
    setMsg(msgArr);
    await axios.get('/response/',{
      headers: {
                'Access-Control-Allow-Origin': '*'
      },
      params: {
          text: trans
      }
    }).then(res => {
        res.data.bot.body = removeLink(res.data.bot.body);
        var struct_response = generateResponse(res.data.bot);
        setMsg([...msgArr, struct_response]);
        setSpeaker([...speaker, 0]);
        var s = generateText(res.data.bot);
        console.log(s);
        setTimeout(() => {
          speak(s);
        }, 1000);
      }
    ).then (err=>{
      console.log(err);
    })
  }

  useEffect(()=>{
    chatRef.current.scrollIntoView({ behavior: 'smooth',block: "end" });
  })

  return (
    <div className="chat-box-div">
      <div className="chat-box">
        {
          msg.map((m,i) => (
              !speaker[i] ? (
                <div className="assistant-box">
                  <img  className="assistant-avatar" src={BoyIcon} />
                  <div className="assistant-msg">
                    {m}
                  </div>
                </div>
              ) : (
                speaker[i] && (
                <div className="user-box">
                  <img  className="user-avatar" src={GirlIcon} />
                  <div className="user-msg">
                    {m}
                  </div>
                </div>
              )
              )
            )
          )
        }
        <div ref={chatRef}></div>
      </div>
      <div className="record-listen">
            {
              isRecording && (
                <div className="mic-box" onClick={stopSpeak} style={{"backgroundColor": "#00274C", color: "white"}} >
                  <AudioOutlined style={{ fontSize: 27 }}/><br/>
                </div>
              )
            }
            {
              !isRecording && (
                <div className="mic-box" onClick={startSpeak} >
                  < AudioOutlined style={{ fontSize: 27}}/><br/>
                </div>
              )
            }
      </div>
    </div>
  );
}

export default ChatBox;
