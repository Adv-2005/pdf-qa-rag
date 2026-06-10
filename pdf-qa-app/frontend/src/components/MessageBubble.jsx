function MessageBubble({
  role,
  content,
  source,
  sources
}) {

  const isUser =
    role === "user";

  return (

    <div
  className={`max-w-xl p-3 rounded-xl ${
    isUser
      ? "bg-blue-600 text-white"
      : "bg-white shadow"
  }`}
>

  {!isUser && source && (
    <div className="text-xs text-gray-500 mb-2">
      {source === "pdf"
        ? "📄 PDF"
        : "🌐 Web"}
    </div>
  )}

  {content}

  {!isUser &&
  sources &&
  sources.length > 0 && (

    <div className="mt-4 border-t pt-2">

      <div className="text-xs font-semibold text-gray-500 mb-2">
        Sources
      </div>

      {sources.map((source, index) => (

        <div
          key={index}
          className="text-xs text-gray-600 mb-2"
        >

          <div>
            Page {source.page}
          </div>

          <div className="italic">
            {source.content}
          </div>

        </div>

      ))}

    </div>

)}

</div>
  );
}

export default MessageBubble;