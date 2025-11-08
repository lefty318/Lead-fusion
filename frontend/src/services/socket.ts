import { io, Socket } from 'socket.io-client';

class SocketService {
  private socket: Socket | null = null;

  connect(token: string) {
    if (this.socket?.connected) return;

    this.socket = io('http://localhost:8000', {
      auth: {
        token,
      },
    });

    this.socket.on('connect', () => {
      console.log('Connected to server');
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from server');
    });

    this.socket.on('new_message', (data) => {
      // Handle new message event
      console.log('New message:', data);
    });

    this.socket.on('conversation_updated', (data) => {
      // Handle conversation update event
      console.log('Conversation updated:', data);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  joinConversation(conversationId: number) {
    if (this.socket) {
      this.socket.emit('join_conversation', { conversation_id: conversationId });
    }
  }

  leaveConversation(conversationId: number) {
    if (this.socket) {
      this.socket.emit('leave_conversation', { conversation_id: conversationId });
    }
  }

  on(event: string, callback: (...args: any[]) => void) {
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  off(event: string, callback?: (...args: any[]) => void) {
    if (this.socket) {
      if (callback) {
        this.socket.off(event, callback);
      } else {
        this.socket.off(event);
      }
    }
  }
}

export const socketService = new SocketService();