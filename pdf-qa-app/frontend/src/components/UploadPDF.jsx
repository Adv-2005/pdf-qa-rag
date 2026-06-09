import { useState } from "react";
import API from "../api";

function UploadPDF() {

  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const uploadFile = async () => {

    if (!file) return;

    const formData = new FormData();

    formData.append(
      "file",
      file
    );

    try {

      await API.post(
        "/upload",
        formData
      );

      setStatus(
        `✓ ${file.name} uploaded`
      );

    } catch (err) {

      console.error(err);

      setStatus(
        "Upload failed"
      );
    }
  };

  return (
    <div className="bg-gray-50 p-4 rounded-xl shadow">

      <h2 className="font-semibold mb-3">
        Upload PDF
      </h2>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <button
        onClick={uploadFile}
        className="mt-3 w-full bg-blue-600 text-white py-2 rounded-lg"
      >
        Upload
      </button>

      <p className="mt-3 text-sm text-green-600">
        {status}
      </p>

    </div>
  );
}

export default UploadPDF;