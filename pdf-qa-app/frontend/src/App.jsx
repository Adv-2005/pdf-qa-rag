import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";

function App() {

  const [messages, setMessages] = useState([]);
  const [sessionId] = useState(() => {

    let id =
      localStorage.getItem(
        "session_id"
      );

    if (!id) {

      id = crypto.randomUUID();

      localStorage.setItem(
        "session_id",
        id
      );
    }

    return id;

  });

  return (
    <div className="h-screen flex bg-gray-100">

      <Sidebar />

      <ChatWindow
        messages={messages}
        setMessages={setMessages}
        sessionId={sessionId}
      />

    </div>
  );
}

export default App;