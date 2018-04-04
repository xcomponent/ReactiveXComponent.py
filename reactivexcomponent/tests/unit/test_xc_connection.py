import unittest
import mock_socket


class TestConnection(unittest.TestCase):

	def setUp(self):
		self.url = "wss:"
		self.client = mock_socket.MockWebSocket(self.url)
		self.server = mock_socket.MockServer(self.url)
		self.client.server = self.server
		self.server.client = self.client