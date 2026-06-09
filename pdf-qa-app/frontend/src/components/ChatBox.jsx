import { useState } from "react";
import API from "../api";

function ChatBox() {

  const [question, setQuestion] =
    useState("");

  const [answer, setAnswer] =
    useState("");

  const askQuestion = async () => {

    const response =
      await API.post(
        "/chat",
        {
          question
        }
      );

    setAnswer(
      response.data.answer
    );
  };

  return (
    <>
      <input
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <p>{answer}</p>
    </>
  );
}

export default ChatBox;