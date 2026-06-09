import { useState } from "react";
import API from "../api";

function ChatInput({
  messages,
  setMessages,
  setLoading
}) {

  const [question, setQuestion] =
    useState("");

  const sendMessage =
    async () => {

      if (!question.trim())
        return;

      const userMessage = {
        role: "user",
        content: question
      };

      setMessages(
        prev => [
          ...prev,
          userMessage
        ]
      );

      setQuestion("");

      setLoading(true);

      try {

        const response =
          await API.post(
            "/chat",
            {
              question
            }
          );

        const botMessage = {
          role: "assistant",
          content:
            response.data.answer
        };

        setMessages(
          prev => [
            ...prev,
            botMessage
          ]
        );

      } catch (err) {

        console.error(err);

        setMessages(
          prev => [
            ...prev,
            {
              role:
                "assistant",
              content:
                "Error communicating with backend."
            }
          ]
        );

      } finally {

        setLoading(false);

      }
    };

  return (

    <div className="bg-white border-t p-4">

      <div className="flex gap-2">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(
              e.target.value
            )
          }
          onKeyDown={(e) =>
            e.key === "Enter" &&
            sendMessage()
          }
          placeholder="Ask a question..."
          className="flex-1 border rounded-lg px-4 py-2"
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-6 rounded-lg"
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default ChatInput;