import telebot;
import feed_operations as feed;
import music_operations as music;
import profile_operations as profile;
import service_operations as service;
from data_storage import BotUser, MusicTrack

GREETING_KEYWORDS = ["hello", "hi", "greetings", "sup", "whats up", "hey"]
GREETING_RESPONSES = ["Hi there", "Greetings", "Salute", "Hello" "Loading...Here I am!"]


class Responder:
	action_dictionary = service.tree();

	# Connect service common methods
	insert_callback = service.insert_callback;
	edit_callback = service.edit_callback;
	edit_action = service.edit_action
	cancel = service.cancel;
	get_genres_menu = service.get_genres_menu;
	add_genres_actions = service.add_genres_actions;
	set_genres_markup = service.set_genres_markup;
	add_genre = service.add_genre;
	clear_genres = service.clear_genres;
	# Connect on music operation methods
	add_crud_actions = music.add_crud_actions;
	get_main_menu = music.get_main_menu;
	add_music_track = music.add_music_track;
	view_music_collection = music.view_music_collection;
	delete_action = music.delete_action;
	delete_yes = music.delete_yes;
	publish = music.publish;
	set_link_markup = music.set_link_markup;
	# Connect feed operations methods
	add_feed_actions = feed.add_feed_actions;
	generate_post_message = feed.generate_post_message;
	request_music = feed.request_music;
	comment_action = feed.comment_action;
	comment_callback = feed.comment_callback;
	notify_publisher = feed.notify_publisher;
	upvote = feed.upvote;
	downvote = feed.downvote;
	# Connect on user profile operation methods;
	add_profile_actions = profile.add_profile_actions;
	get_user = profile.get_user;
	registration = profile.registration;
	save_profile = profile.save_profile;
	save_yes = profile.save_yes;

	def __init__(self, bot):
		self.bot = bot

	@service.send_typing_action
	def respond(self, message):
		queried_users = BotUser.objects(chat_id=message.chat.id);
		if not queried_users:
			self.registration(message);
		elif message.text == music.INSERT_REPLY:
			self.add_music_track(message);
		elif message.text == music.VIEW_REPLY:
			self.view_music_collection(message);
		elif message.text == music.REQUEST_REPLY:
			self.request_music(message);

	def subscribe_actions(self, call):
		action_nodes = call.data.split("/");
		if MusicTrack.objects(pk=action_nodes[-1]):
			document = MusicTrack.objects(pk=action_nodes[-1]).get();
		elif BotUser.objects(pk=action_nodes[-1]):
			document = BotUser.objects(pk=action_nodes[-1]).get();
		self.get_action(action_nodes[:-1])(call, document);

	def command_handler(self, command, message):
		user = self.get_user(message);
		if command == "start":
			self.bot.send_message(
				message.chat.id,
				"Greetings my friend! I'm here to help you share music with your friends. Let's begin then, shall we?"
			);
		elif command == "menu":
			self.bot.send_message(
				message.chat.id,
				"Hi mate, here's what you can do. Go for it!",
				reply_markup=self.get_main_menu(user)
			);
		elif command == "add":
			self.add_music_track(message);
		elif command == "view":
			self.view_music_collection(message);
		elif command == "get":
			if user and MusicTrack.objects(publisher=user).count() >= 1:
				self.request_music(message);
			else:
				self.bot.send_message(
					message.chat.id,
					"Sorry but you must earn ability to request music by adding at least one track"
				);

	def get_action(self, nodes):
		action_node = self.action_dictionary;
		for node in nodes:
			action_node = action_node[node];
		return action_node;

	def init_action_dictionary(self):
		self.add_profile_actions();
		self.add_crud_actions();
		self.add_genres_actions();
		self.add_feed_actions();
