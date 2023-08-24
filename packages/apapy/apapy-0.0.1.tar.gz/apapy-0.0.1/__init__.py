import requests


class Video:
	def __init__(self, link, res, fileName):
		self.link = link
		self.res = res
		self.fileName = fileName

	def downloadVideo(self):
		
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)

		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'

		response = requests.get(url)

		if response.status_code == 200:
			data = response.json()
			files = data['video']['file_link_all']
			
			file_ = data['video']['file_link']
			
			file_name = data['video']['title']
			
			if self.res == True or self.fileName == True:
				
				if self.res == True and self.fileName == True:
					url = file_
					
					response = requests.get(url)
					
					if response.status_code == 200:
					
						with open(f'{file_name}.mp4', 'wb') as rf:
							rf.write(response.content)
							
					else:
						print('An error occurred')
						
				elif self.res == True:
					url = file_
					
					response = requests.get(url)
					
					if response.status_code == 200:
						
						with open(self.fileName, 'wb') as r:
							r.write(response.content)
							
					else:
						print('An error occurred')
						
				elif self.fileName == True:
					
					if self.res == '144p':
						for file in files:
							if file['profile'] == '144p':
								url = file['urls'][0]
		
								response = requests.get(url)
		
								if response.status_code == 200:
									with open(f'{file_name}.mp4', 'wb') as v:
										v.write(response.content)
										
								else:
									print('An error occurred')
		
								break
		
					elif self.res == '240p':
						for file in files:
							if file['profile'] == '240p':
								url = file['urls'][0]
		
								response = requests.get(url)
		
								if response.status_code == 200:
									with open(f'{file_name}.mp4', 'wb') as v:
										v.write(response.content)
										
								else:
									print('An error occurred')
		
								break
								
					elif self.res == '360p':
						for file in files:
							if file['profile'] == '360p':
								url = file['urls'][0]
		
								response = requests.get(url)
		
								if response.status_code == 200:
									with open(f'{file_name}.mp4', 'wb') as v:
										v.write(response.content)
										
								else:
									print('An error occurred')
		
								break
								
					elif self.res == '480p':
						for file in files:
							if file['profile'] == '480p':
								url = file['urls'][0]
		
								response = requests.get(url)
		
								if response.status_code == 200:
									with open(f'{file_name}.mp4', 'wb') as v:
										v.write(response.content)
										
								else:
									print('An error occurred')
		
								break
								
					elif self.res == '720p':
						for file in files:
							if file['profile'] == '720p':
								url = file['urls'][0]
		
								response = requests.get(url)
		
								if response.status_code == 200:
									with open(f'{file_name}.mp4', 'wb') as v:
										v.write(response.content)
										
								else:
									print('An error occurred')
		
								break
								
					elif self.res == '1080p':
						for file in files:
							if file['profile'] == '1080p':
								url = file['urls'][0]
		
								response = requests.get(url)
		
								if response.status_code == 200:
									with open(f'{file_name}.mp4', 'wb') as v:
										v.write(response.content)
										
								else:
									print('An error occurred')
		
								break
				
			else:

				if self.res == '144p':
					for file in files:
						if file['profile'] == '144p':
							url = file['urls'][0]
	
							response = requests.get(url)
	
							if response.status_code == 200:
								with open(self.fileName, 'wb') as v:
									v.write(response.content)
									
							else:
								print('An error occurred')
	
							break
	
				elif self.res == '240p':
					for file in files:
						if file['profile'] == '240p':
							url = file['urls'][0]
	
							response = requests.get(url)
	
							if response.status_code == 200:
								with open(self.fileName, 'wb') as v:
									v.write(response.content)
									
							else:
								print('An error occurred')
	
							break
							
				elif self.res == '360p':
					for file in files:
						if file['profile'] == '360p':
							url = file['urls'][0]
	
							response = requests.get(url)
	
							if response.status_code == 200:
								with open(self.fileName, 'wb') as v:
									v.write(response.content)
									
							else:
								print('An error occurred')
	
							break
							
				elif self.res == '480p':
					for file in files:
						if file['profile'] == '480p':
							url = file['urls'][0]
	
							response = requests.get(url)
	
							if response.status_code == 200:
								with open(self.fileName, 'wb') as v:
									v.write(response.content)
									
							else:
								print('An error occurred')
	
							break
							
				elif self.res == '720p':
					for file in files:
						if file['profile'] == '720p':
							url = file['urls'][0]
	
							response = requests.get(url)
	
							if response.status_code == 200:
								with open(self.fileName, 'wb') as v:
									v.write(response.content)
									
							else:
								print('An error occurred')
	
							break
							
				elif self.res == '1080p':
					for file in files:
						if file['profile'] == '1080p':
							url = file['urls'][0]
	
							response = requests.get(url)
	
							if response.status_code == 200:
								with open(self.fileName, 'wb') as v:
									v.write(response.content)
									
							else:
								print('An error occurred')
	
							break
							
		else:
			print('An error occurred')
						
						
class Cover:
	def __init__(self, link, fileName):
		self.link = link
		self.fileName = fileName
		
	def downloadCover(self):
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)
		
		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'
		
		response = requests.get(url)
		
		if response.status_code == 200:
			data = response.json()
			
			url = data['video']['big_poster']
			file_name = data['video']['title']
			
			if self.fileName == True:
				
				response = requests.get(url)
				
				if response.status_code == 200:
					with open(f'{file_name}.jpg', 'wb') as c:
						c.write(response.content)
						
				else:
					print('An error occurred')
				
			else:
			
				response = requests.get(url)
				
				if response.status_code == 200:
					with open(self.fileName, 'wb') as c:
						c.write(response.content)
						
				else:
					print('An error occurred')
						
						
		else:
			print('An error occurred')
					
class Title:
	def __init__(self, link):
		self.link = link
		
	def getTitle(self):
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)
		
		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'
		
		response = requests.get(url)
		
		if response.status_code == 200:
			data = response.json()
			
			title = data['video']['title']
			
			return title
			
		else:
			print('An error occurred')
			
class channelName:
	def __init__(self, link):
		self.link = link
		
	def getChannelName(self):
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)
		
		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'
		
		response = requests.get(url)
		
		if response.status_code == 200:
			data = response.json()
			
			name = data['video']['sender_name']
			
			return name
			
		else:
			print('An error occurred')
			
class Description:
	def __init__(self, link):
		self.link = link
		
	def getDescription(self):
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)
		
		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'
		
		response = requests.get(url)
		
		if response.status_code == 200:
			data = response.json()
			
			description = data['video']['description']
			
			return description
			
		else:
			print('An error occurred')
			
class likeCount:
	def __init__(self, link):
		self.link = link
		
	def getLikeCount(self):
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)
		
		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'
		
		response = requests.get(url)
		
		if response.status_code == 200:
			data = response.json()
			
			count = data['video']['like_cnt']
			
			return count
			
		else:
			print('An error occurred')
			
class visitCount:
	def __init__(self, link):
		self.link = link
		
	def getVisitCount(self):
		code = self.link.replace(
			'https://www.aparat.com/v/',
			''
		)
		
		url = f'https://www.aparat.com/etc/api/video/videohash/{code}'
		
		response = requests.get(url)
		
		if response.status_code == 200:
			data = response.json()
			
			visit = data['video']['visit_cnt']
			
			return visit
			
		else:
			print('An error occurred')