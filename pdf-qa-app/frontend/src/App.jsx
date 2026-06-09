import { useState } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";

function App() {

  const [messages, setMessages] = useState([]);

  return (
    <div className="h-screen flex bg-gray-100">

      <Sidebar />

      <ChatWindow
        messages={messages}
        setMessages={setMessages}
      />

    </div>
  );
}

export default App;