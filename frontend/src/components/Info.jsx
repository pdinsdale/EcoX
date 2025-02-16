import React, { useState, useEffect } from 'react';
import "../App.css";
import ItemInfo from './ItemInfo';

function Info() {

  const [messages, setMessages] = useState([])
  const [messageComponents, setMessageComponents] = useState([]);
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

      setMessageComponents(prevComponents => [...prevComponents, <ItemInfo key={Date.now()}
                                                                           label={parsedData.item}
                                                                           impact={parsedData.impact}
                                                                           current_impact={parsedData.current_impact}
                                                                           alternatives={parsedData.alternatives} />]);
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
      <div>{messageComponents}</div>
      {/* <ul>
        {messages.map((msg, index) => (
            <div key={index}>
                <ItemInfo label={msg.item} impact={msg.impact} current_impact={msg.current_impact} alternatives={msg.alternatives} />
            </div>
        //   <li key={index}>
        //     {typeof msg === "object" ? JSON.stringify(msg) : msg}
        //   </li>
        ))}
      </ul> */}
    </div>
  );
}

export default Info;