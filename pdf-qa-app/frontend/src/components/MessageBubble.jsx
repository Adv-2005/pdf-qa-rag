function MessageBubble({
  role,
  content
}) {

  const isUser =
    role === "user";

  return (

    <div
      className={`flex mb-4 ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >

      <div
        className={`max-w-xl p-3 rounded-xl ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-white shadow"
        }`}
      >

        {content}

      </div>

    </div>
  );
}

export default MessageBubble;