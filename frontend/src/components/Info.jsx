import React, { useState, useEffect } from 'react';
import "../App.css";

function Info() {

  const [messages, setMessages] = useState([])
  const [isStreaming, setIsStreaming] = useState(true);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8080/stream_api");

    eventSource.onmessage = (event) => {
      let parsedData;
      try {
        parsedData = JSON.parse(event.data);
      } catch (error) {
        parsedData = event.data;
      }

      if (typeof parsedData === "object" && parsedData.status === "stop") {
        setIsStreaming(false);
        eventSource.close();
      }

      setMessages(prevMessages => [...prevMessages, parsedData]);
      console.log(parsedData)
    };

    eventSource.onerror = (error) => {
      console.error("EventSource error:", error);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div className="Info">
      <h2>API Messages</h2>
      {isStreaming ? <p>Streaming data...</p> : <p>Streaming stopped.</p>}
      <ul>
        {messages.map((msg, index) => (
          <li key={index}>
            {typeof msg === "object" ? JSON.stringify(msg) : msg}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Info;