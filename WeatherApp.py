import googlemaps
import urllib
import requests
import json
import csv
import pygame
import pygame.font
import pygame.freetype
from datetime import datetime
from datetime import date

# --- Functions --- #
# Open external file and read API key into program. This way key is never stored on public side code.
def getAPIkey(filename):
    with open(filename,'r') as f:   
        keys = f.readline()
    return keys

# Send a urllib.request.urlopen() and after validating response, print the json response.
def getRequest(apistring):
    response = urllib.request.urlopen(apistring)
    if response.getcode() == 200:
        now = datetime.now()
        print("Successfully fetched the data: " + str(now.strftime("%H:%M:%S")))
    else:
        print("There was an issue with the request: ",response.getcode()) #status_code
    text = response.read()
    #print("Response:\n",text)
    answer = json.loads(text.decode("utf-8"))
    return answer

def getForecastWeather(APIstring):
    weather = getRequest(APIstring)
    for data in range(0,7):
        Nxt7MinMaxTemps.append(str(weather['data'][data]['app_min_temp']) +" / "+ str(weather['data'][data]['app_max_temp'])+"F")
        Nxt7CloudPerc.append("Clouds: "+str(weather['data'][data]['clouds'])+"%")
        SunsetDateTime = datetime.fromtimestamp(weather['data'][data]['sunset_ts'])
        Nxt7SunsetTime.append("Sunset: "+str(SunsetDateTime.time()))
    return Nxt7MinMaxTemps, Nxt7CloudPerc, Nxt7SunsetTime

def getCurrentWeather(APIstring):
    weather = getRequest(APIstring)
    currentTemp = str(weather['data'][0]['app_temp']) + "F"
    return currentTemp

def getDate():
    today = date.today()
    TdDate = today.strftime("%d") # number day
    TdMonth = today.strftime("%B") # string month
    TdOfWeek = today.weekday() # number day of week
    datetextnew = datetext[TdOfWeek:]
    datetextnew.extend(datetext[:TdOfWeek])
    for i in range(0,7):
        datetextnew[i] = datetextnew[i] + " - " + (str(int(TdDate)+i))
    return datetextnew

# Ping Google API to get lat & lon for an input Location. Probably only run on setup to avoid continually pinging Google's API for the same information.
def getGeoCode(keystring, location):
    gmaps = googlemaps.Client(key=keystring)
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    return lat, lon

# --- Classes --- #
class DayBox(pygame.sprite.Sprite):
    def __init__(self,boxcolor,textcolor,width,height,datetext,datetextsize,cloudtext,cloudtextsize,sunsettext,sunsettextsize,temptext,temptextsize,ID):
        super().__init__()
        self.datetext = datetext
        self.datetextsize = datetextsize
        self.cloudtext = cloudtext
        self.cloudtextsize = cloudtextsize
        self.sunsettext = sunsettext
        self.sunsettextsize = sunsettextsize
        self.temptext = temptext
        self.temptextsize = temptextsize
        self.boxcolor = boxcolor
        self.textcolor = textcolor
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE) # Anything on this Surface that is the color 'WHITE' will appear transparent 
        self.fontDate = pygame.freetype.SysFont('Arial', self.datetextsize)
        self.fontClouds = pygame.freetype.SysFont('Arial', self.cloudtextsize)
        self.fontSunset = pygame.freetype.SysFont('Arial', self.sunsettextsize)
        self.fontTemps = pygame.freetype.SysFont('Arial', self.temptextsize)
        pygame.draw.rect(self.image, self.boxcolor, pygame.Rect(0,0,self.width,self.height), 5, 5)
        self.fontDate.render_to(self.image, (10,10), self.datetext, self.textcolor)
        self.fontClouds.render_to(self.image, (7,self.height-self.cloudtextsize-5), self.cloudtext, self.textcolor)
        self.fontSunset.render_to(self.image, (self.width/2,self.height-self.sunsettextsize-5), self.sunsettext, self.textcolor)
        self.fontTemps.render_to(self.image, (9,(self.height-self.temptextsize)/2), self.temptext, self.textcolor)
        self.rect = self.image.get_rect()
        self.ID = ID
    def update(self): # Called when .update is called for all sprites in sprite list below 
        self.image.fill(WHITE)    
        pygame.draw.rect(self.image, self.boxcolor, pygame.Rect(0,0,self.width,self.height), 5, 5)
        self.fontDate.render_to(self.image, (10,10), self.datetext, self.textcolor)
        self.fontClouds.render_to(self.image, (7,self.height-self.cloudtextsize-5), self.cloudtext, self.textcolor)
        self.fontSunset.render_to(self.image, (self.width/2,self.height-self.sunsettextsize-5), self.sunsettext, self.textcolor)
        self.fontTemps.render_to(self.image, (9,(self.height-self.temptextsize)/2), self.temptext, self.textcolor)

class CurrentBox(pygame.sprite.Sprite):
    def __init__(self,textcolor,width,height,text,textsize):
        super().__init__()
        self.text = text
        self.textsize = textsize
        self.textcolor = textcolor
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.font = pygame.freetype.SysFont('Arial', self.textsize)
        self.font.render_to(self.image, (0,0), self.text, self.textcolor)
        self.rect = self.image.get_rect()
    def update(self):
        self.image.fill(WHITE)
        self.font.render_to(self.image, (0,0), self.text, self.textcolor)

# --- Variables --- #
ans=0
running = True
SURFACE_COLOR_BLACK = BLACK = (0,0,0)
WHITE = (255,255,255)
boxcolor = BLUE = (0,100,255)
boxtextcolor = GREEN = (0,255,0)
boxwidth = 100
boxheight = 150
datetext = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
datetextsize = 20
cloudtext = ""
cloudtextsize = 17
sunsettext = ""
sunsettextsize = 17
temptext = ""
temptextsize = 36
Nxt7MinMaxTemps = []
Nxt7CloudPerc = []
Nxt7SunsetTime = []
currentboxtextcolor = ORANGE = (255,165,0)
currentboxwidth = 300
currentboxheight = 300
currenttextsize = 75

# --- Main --- #
# Ask for user input on weather tracker location. If needed, use Google API to grab lat & lon. 
while not (ans==1 or ans==2 or ans==3):
    ans = input("Where would you like to set up this Weather Tracker for the first time? Type the number of your answer: \n[1] Yes! Westwood, Los Angeles, CA.\n[2] Yes, but a different location\n[3] No, I've already set it up before.\n")
    try:
        ans=int(ans)
    except:
        print("Please try again, input the number only.")
    if ans==1:
        lat = 34.0635016
        lon=-118.4455164
    if ans==2:
        Location = input("Where would you like to set up this Weather Tracker for? Please type in 'city, state' format for best results.\n")
        Gkey = getAPIkey('Google_key.txt') # Grab private API key from local txt file
        lat, lon = getGeoCode(Gkey,Location)
        with open('latlon.csv', 'a', newline='') as l:
            field_names = ['RegionName','Lat','Lon']
            lDict = csv.DictWriter(l, fieldnames=field_names)
            lDict.writerow({'RegionName': Location, 'Lat': lat, 'Lon': lon})
    if ans==3:
        lat = 34.0635016
        lon =-118.4455164

# --- Create The Weather API URL --- #
#API_Url_String = 'https://api.openweathermap.org/data/2.5/weather?' # This is the preferred weather service but I can't get to work!
API_Url_String_Hourly = 'https://api.weatherbit.io/v2.0/forecast/hourly?'
API_Url_String_Daily = 'https://api.weatherbit.io/v2.0/forecast/daily?'
#Wkey = getAPIkey('OpenWeatherMap_key.txt')
Wkey = getAPIkey('WeatherBit_key.txt')
API_Url_String_Hourly = API_Url_String_Hourly+'lat='+str(lat)+'&lon='+str(lon)+'&units=I&key='+str(Wkey)
API_Url_String_Daily = API_Url_String_Daily+'lat='+str(lat)+'&lon='+str(lon)+'&units=I&key='+str(Wkey)
#print(API_Url_String_Daily)

# Start the Pygame display. Ping the WeatherBit API every 15 minutes and update display.
# --- Initiatilize The Pygame --- # runs once
pygame.init()
clock = pygame.time.Clock()

# - Create The Screen & Local Variables -
screenflags = pygame.FULLSCREEN
screen = pygame.display.set_mode((0,0))#,screenflags) # Add screenflags back in to go fullscreen.

pygame.display.set_caption("Weather Tracker")
screenH = screen.get_height() # Grab whatever screen size resulted from (0,0) above.
screenW = screen.get_width() # Grab whatever screen size resulted from (0,0) above.
boxwidth = screenW / 7
boxheight = screenH / 10

# - Sprite Group Creation - #
all_sprites_list = pygame.sprite.Group()
day_box_list = pygame.sprite.Group() # Creates group for all pygame sprites for iterating through later
current_box_list = pygame.sprite.Group()

# - Initial Date Data Creation - #
datetextnew = getDate()

# - Initial Weather & Date Data Collection - #
Nxt7MinMaxTemps, Nxt7CloudPerc, Nxt7SunsetTime = getForecastWeather(API_Url_String_Daily)
currenttext = getCurrentWeather(API_Url_String_Hourly)

# - Initial Sprite Creation - #
for i in range(0,7):
    daybox = DayBox(boxcolor,boxtextcolor,boxwidth,boxheight,datetextnew[i],datetextsize,Nxt7CloudPerc[i],cloudtextsize,Nxt7SunsetTime[i],sunsettextsize,Nxt7MinMaxTemps[i],temptextsize,i)
    daybox.rect.x = (i)*boxwidth
    daybox.rect.y = screenH / 3
    day_box_list.add(daybox)
    all_sprites_list.add(daybox)
currentbox = CurrentBox(currentboxtextcolor,currentboxwidth,currentboxheight,currenttext,currenttextsize)
currentbox.rect.x = (screenW-currentboxwidth)/2
currentbox.rect.y = screenH/5
current_box_list.add(currentbox)
all_sprites_list.add(currentbox)

# --- Pygame Loop --- #
while running:
        
    # - User Events - #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # More user events go here
    
    # - Updates (without draws) - #
    datetextnew = getDate() 
    Nxt7MinMaxTemps, Nxt7CloudPerc, Nxt7SunsetTime = getForecastWeather(API_Url_String_Daily)
    for sprite in day_box_list:
        sprite.datetext = datetextnew[sprite.ID]
        sprite.cloudtext = Nxt7CloudPerc[sprite.ID]
        sprite.sunsettext = Nxt7SunsetTime[sprite.ID]
        sprite.temptext = Nxt7MinMaxTemps[sprite.ID]
    currenttext = getCurrentWeather(API_Url_String_Hourly)
    for sprite in current_box_list:
        sprite.currenttext = currenttext

    all_sprites_list.update()
    
    # - Draws (without updates) - #
    screen.fill(SURFACE_COLOR_BLACK)
    all_sprites_list.draw(screen)
    pygame.display.flip() # Updates the contents of the entire display.
    
    # - Tick the Clock - #
    clock.tick(60) # Prevents program from running faster than 60 frames per second. Uses SDL_Delay function which is not that accurate but saves CPU.
    pygame.time.wait(1000*60*15) # 15m of delay before runnning loop again
    
# --- End while loop when running=False --- #
pygame.quit()



