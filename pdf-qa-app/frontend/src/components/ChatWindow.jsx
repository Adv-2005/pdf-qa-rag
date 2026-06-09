import { useState } from "react";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";

function ChatWindow({
  messages,
  setMessages
}) {

  const [loading, setLoading] =
    useState(false);

  return (
    <div className="flex-1 flex flex-col">

      <div className="flex-1 overflow-y-auto p-6">

        {messages.map(
          (message, index) => (
            <MessageBubble
              key={index}
              role={message.role}
              content={message.content}
            />
          )
        )}

        {loading && (
          <div className="text-gray-500">
            Thinking...
          </div>
        )}

      </div>

      <ChatInput
        messages={messages}
        setMessages={setMessages}
        setLoading={setLoading}
      />

    </div>
  );
}

export default ChatWindow;