const ChatBubble = ({ role, text }) => {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} my-2`}>
      <div className={`max-w-[75%] px-4 py-2 rounded-lg ${isUser ? 'bg-blue-600 text-white' : 'bg-gray-200 text-black'}`}>
        {text}
      </div>
    </div>
  );
};

export default ChatBubble;
