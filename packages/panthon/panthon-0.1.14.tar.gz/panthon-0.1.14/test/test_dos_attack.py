import pytest
from unittest.mock import patch, MagicMock
from dos_attack import DoSAttack
import panthon.dos_attack


class TestDoSAttack:
    @patch('socket.socket')
    def test_slowloris_attack(self, mock_socket):
        url = "http://panthon.app"
        target_port = 80
        num_connections = 100

        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock

        dos = DoSAttack()
        dos.slowloris_attack(url, target_port, num_connections)

        assert mock_socket.call_count == num_connections
        assert mock_sock.connect.call_count == num_connections
        assert mock_sock.send.call_count == num_connections * 3