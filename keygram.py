#!/usr/bin/python3

import json
import asyncio
from subprocess import Popen, PIPE
from telethon import TelegramClient, events


class KeyBase():

	_module_ = "KeyBase "

	def KeyBase_send_attachment(self, conversationID, attachment, message = ""):

		command={
					"method": "attach",
					"params": {
						"options": {
							"conversation_id": conversationID,
							"filename"       : attachment,
							"title"          : message}
					}
				}

		self.KeyBase_format_command(command, True)


	def KeyBase_send_msg(self, conversationID, message):

		command={
					"method": "send",
					"params": {
						"options": {
							"conversation_id": conversationID,
							"message": {
								"body": message
							}
						}
					}
				}

		self.KeyBase_format_command(command, True)


	def KeyBase_format_command(self, command, execCMD = False):

		encodedCommand = None

		try:

			encodedCommand = json.dumps(command).encode("utf-8")

			if encodedCommand is None:

				print("E | {} | command has invalid structure".format(self._module_))

				return False

			elif execCMD is True:

				return self.KeyBase_execute_command(encodedCommand)

			else:

				return encodedCommand

				
		except Exception as e:

			print(e)


	def KeyBase_execute_command(self, command):

		process = Popen(['keybase', 'chat', 'api'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = process.communicate(command)

		if process.returncode != 0:

			print(f"[{command!r} exited with {process.returncode}]")
			print(stderr.decode())

		response = stdout.decode("utf-8")

		try:

			parsed_response = json.loads(stdout)

			if "error" in parsed_response:

				raise Exception(parsed_response["error"])

			return parsed_response

		except Exception as e:

			print(e)


		return False


class Telegram():

	_module_ = "Telegram"

	async def Telegram_iter_dialogs(self, client):

		async for dialog in client.iter_dialogs():

			print('{:}: {}'.format(dialog.id, dialog.title))


	def exec(self, name, apiID, apiHash, sourceID, targetID):

		client = TelegramClient(name, apiID, apiHash)

		@client.on(events.NewMessage(chats=(sourceID, )))
		async def handler_new_message(event):

			try:

				message = event.message.to_dict()['message']

				KeyBase().KeyBase_send_msg(targetID, message)

			except Exception as e:

				print(e)


		with client:

			client.loop.run_until_complete(self.Telegram_iter_dialogs(client))

			client.start()
			client.run_until_disconnected()


if __name__ == "__main__":

	#--Telegram--
	TGSessionName = ""
	TGapiID       = ""
	TGapiHash     = ""
	TGSource      = 0
	#--KeyBase---
	KBTarget      = ""

	Telegram().exec(TGSessionName, TGapiID, TGapiHash, TGSource, KBTarget)