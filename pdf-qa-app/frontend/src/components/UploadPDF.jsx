import { useState } from "react";
import API from "../api";

function UploadPDF() {

  const [file, setFile] = useState(null);

  const handleUpload = async () => {

    const formData = new FormData();

    formData.append("file", file);

    await API.post(
      "/upload",
      formData
    );

    alert("PDF Uploaded");
  };

  return (
    <>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <button onClick={handleUpload}>
        Upload
      </button>
    </>
  );
}

export default UploadPDF;