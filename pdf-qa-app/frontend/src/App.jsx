import UploadPDF from "./components/UploadPDF";
import ChatBox from "./components/ChatBox";

function App() {

  return (
    <div>

      <h1>
        PDF Q&A Agent
      </h1>

      <UploadPDF />

      <ChatBox />

    </div>
  );
}

export default App;