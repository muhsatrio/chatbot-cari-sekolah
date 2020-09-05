import React, {useState, useEffect} from 'react';
import {Button, Form, Container} from 'react-bootstrap';
import './App.css';
import io from "socket.io-client";

const endPoint = "http://localhost:5000";

const socket = io.connect(endPoint);

function App() {

  const [messages, setMessages] = useState([
    {
      person: "BOT Sekolah Bandung",
      message: "Hai dik, silahkan sapa kami dengan hai/halo, untuk memulai BOT. Atau kalau mau ajak kenalan dengan mengetik 'kenalan dong' buat kepo soal BOT ini juga bisa! :)"
    }
  ]);

  const [message, setMessage] = useState("");

  const [waktu, setWaktu] = useState(0);

  useEffect(() => {
    getMessages();
  }, [messages.length]);

  useEffect(() => {
    const timer = setInterval(() => {
      setWaktu(waktu + 1);
      if (waktu==31) {
        setMessages([...messages, {
          person: "BOT Sekolah Bandung",
          message: "Karena kamu tidak merespon selama 30 detik, BOT mengakhir percakapan. :("
        }])
      }
    }, 1000);
               // clearing interval
    return () => clearInterval(timer);
  });

  const getMessages = () => {
    socket.on("message", msg => {
      setMessages([...messages, {
        person: "BOT Sekolah Bandung",
        message: msg.message
      }]);
      if (msg.type === 'finish') {
        setWaktu(32);
      }
      else {
        setWaktu(0);
      }
    });
  }

  const onChange = e => {
    setMessage(e.target.value);
  }

  const onClick = () => {
    if (message !== "") {
      setMessages([...messages, {
        person: "Me",
        message: message
      }]);
      socket.emit("message", message);
      setMessage("");
    }
  }

  // setInterval(() => {
  //   setWaktu(waktu + 1);
  //   console.log(waktu);
  // }, 1000);

  return (
    <div className="App">
      <h3>BOT Sekolah Bandung</h3>
      <h5>Baru Pindah ke Bandung? Cari Sekolah Barumu dengan BOT ini :)</h5>
      <hr/>
      <Container>
        {waktu<=30 ? (
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Message</Form.Label>
            <Form.Control onKeyPress={e => e.key === 'Enter' ? onClick() : null} value={message} type="text" name="message" placeholder="Type the message..." onChange={e => onChange(e)} />
            <br/>
            <Button variant="primary" onClick={() => onClick()}>Send Message</Button>
          </Form.Group>
        ) : null}
        <div className="dialogBox" style={{maxHeight: 'calc(100vh - 210px)', overflowY: 'auto'}}>
          {messages.length>0 ? messages.map((msg, i) => (
            <p style={{whiteSpace: "pre-line"}} key={i}><b>{msg.person}</b>:<br />{msg.message}</p>
          )) : null}
        </div>
      </Container>
    </div>
  );
}

export default App;
