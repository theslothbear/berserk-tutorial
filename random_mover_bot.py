import berserk
import threading
import chess
import random
import traceback

class Game(threading.Thread):
    def __init__(self, client, game_id, color, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.color = color
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)

    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)

    def handle_state_change(self, state):
        if self.color.upper() == 'BLACK' and len(state['moves'].split()) % 2 == 0:
        	board = chess.Board()
        	for move in state['moves'].split():
        		board.push(chess.Move.from_uci(move))
        	sp = []
        	for a in board.legal_moves:
        		sp.append(a)
        	if sp:
        		try:
        			client.bots.make_move(self.game_id, random.choice(sp))
        		except Exception as e:
        			print(e)
        elif self.color.upper() == 'WHITE' and len(state['moves'].split()) % 2 == 1:
        	board = chess.Board()
        	for move in state['moves'].split():
        		board.push(chess.Move.from_uci(move))
        	sp = []
        	for a in board.legal_moves:
        		sp.append(a)
        	if sp:
        		try:
        			client.bots.make_move(self.game_id, random.choice(sp))
        		except Exception as e:
        			print(e)
    def handle_chat_line(self, line):
    	if line['username'].upper() != 'BERSERKRANDOMMOVER':
    		try:
    			client.bots.post_message(self.game_id, 'Hi! You can find my source code in my profile:)')
    		except:
    			print(traceback.format_exc())

session = berserk.TokenSession('ТОКЕН')
client = berserk.Client(session=session)


for event in client.bots.stream_incoming_events():
	if event['type'] == 'challenge':
		if event['challenge']['variant']['key'] == 'standard':
			try:
				client.bots.accept_challenge(event['challenge']['id'])
			except Exception as e:
				print(e)
	elif event['type'] == 'gameStart':
		if event['game']['color'] == 'white':
			c = 'black'
			board = chess.Board(fen=event['game']['fen'])
			sp = []
			for a in board.legal_moves:
				sp.append(a)
			client.bots.make_move(event['game']['gameId'], random.choice(sp))
			game = Game(client, event['game']['gameId'], c)
			game.start()
		else:
			c = 'white'
			game = Game(client, event['game']['gameId'], c)
			game.start()
		
