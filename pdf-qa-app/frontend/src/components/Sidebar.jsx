import UploadPDF from "./UploadPDF";

function Sidebar() {

  return (
    <div className="w-80 bg-white border-r p-5">

      <h1 className="text-2xl font-bold mb-6">
        PDF Agent
      </h1>

      <UploadPDF />

    </div>
  );
}

export default Sidebar;