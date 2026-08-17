import { useEffect, useRef, useState } from "react";

function usePageSocket(pageId, onPageUpdate) {
  const socketRef = useRef(null);
  const typingTimerRef = useRef(null);

  const [connected, setConnected] = useState(false);
  const [onlineUsers, setOnlineUsers] = useState(0);
  const [someoneTyping, setSomeoneTyping] = useState(false);

  useEffect(() => {
    if (!pageId) {
      return;
    }

    const socket = new WebSocket(`ws://127.0.0.1:8001/ws/pages/${pageId}`);

    socketRef.current = socket;

    socket.onopen = () => {
      setConnected(true);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "presence") {
          setOnlineUsers(data.online_users || 0);
        }

        if (data.type === "typing") {
          setSomeoneTyping(Boolean(data.is_typing));
        }

        if (data.type === "page_update" && typeof onPageUpdate === "function") {
          onPageUpdate({
            title: data.title,
            content: data.content,
          });
        }
      } catch (error) {
        console.error("Unable to process WebSocket message:", error);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
      setConnected(false);
      setOnlineUsers(0);
      setSomeoneTyping(false);
    };

    return () => {
      if (typingTimerRef.current) {
        clearTimeout(typingTimerRef.current);
      }

      socket.close();
    };
  }, [pageId, onPageUpdate]);

  const sendPageUpdate = (title, content) => {
    if (socketRef.current?.readyState !== WebSocket.OPEN) {
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        type: "page_update",
        title,
        content,
      }),
    );
  };

  const sendTyping = () => {
    if (socketRef.current?.readyState !== WebSocket.OPEN) {
      return;
    }

    socketRef.current.send(
      JSON.stringify({
        type: "typing",
        is_typing: true,
      }),
    );

    if (typingTimerRef.current) {
      clearTimeout(typingTimerRef.current);
    }

    typingTimerRef.current = setTimeout(() => {
      if (socketRef.current?.readyState === WebSocket.OPEN) {
        socketRef.current.send(
          JSON.stringify({
            type: "typing",
            is_typing: false,
          }),
        );
      }
    }, 1200);
  };

  return {
    connected,
    onlineUsers,
    someoneTyping,
    sendPageUpdate,
    sendTyping,
  };
}

export default usePageSocket;
