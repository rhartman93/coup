#Author: Joe DiSabito
#Description: Allows automation of Coup game without cards. Requires moderator
#to operate. Python is weird about dictionaries (no list elements allowed),
#which made the Ambassador ability very difficult. Would have liked
#each person's hand to be a list of cards, but that was not possible.
#Anyways, enjoy!
#!/usr/bin/python

import sys, os, random, time

class Player(object):
        def __init__(self, card1, card2):
                self.coins = 2
                self.cards = [card1, card2]
        def aboutMe(self):
                pCards = ""
                for card in self.cards:
                        pCards += card + " "
                return "Coins: " + str(self.coins) + "\nCards: " + pCards
        def draw(self, newCard):
                self.cards.append(newCard)
        def lookAtHand(self):
                for card in self.cards:
                        print card
        def loseCoins(self, amt):
                if self.coins -  amt <= 0:
                        print "Not enough coins"
                else:
                        self.coins -= amt
                
class Deck(object):
        def __init__(self):
                self.cards = self.cards = ['Contessa', 'Contessa', 'Contessa', 'Duke', 'Duke', 'Duke', 'Captain', 'Captain', 'Captain', 'Assassin', 'Assassin', 'Assassin', 'Ambassador' ,'Ambassador' ,'Ambassador']
                self.numCards = 15

        def shuffle(self):
                random.seed()
                random.shuffle(self.cards)
                
        def deal(self):
                self.numCards -= 1
                print "Dealing Card: numCards = ", self.numCards
                return self.cards.pop()

        def fanUp(self):
                for i, card in enumerate(self.cards):
                        print i, " ", card

        def addCard(self, card):
                self.cards.append(card)

        


        
        

class CoupGame(object):
        def __init__(self):
                #self.cards = ['Contessa', 'Contessa', 'Contessa', 'Duke', 'Duke', 'Duke', 'Captain', 'Captain', 'Captain', 'Assassin', 'Assassin', 'Assassin', 'Ambassador' ,'Ambassador' ,'Ambassador']
                self.deck = Deck()
                #self.numCards = 15
                self.destroyedCards = []
                self.menu = "(s)tatus\ncoun(t)s\n(e)xchange\ns(h)uffle\n(c)oins\n(a)ssasinate\ncou(p)\nta(x)\nstea(l)\n(i)ncome\n(f)oreign aid\n(o)ptions\n(q)uit: "
                self.players = {}
                self.numPlayers = input("Number of players (2-6): ")
                self.playerList = [] #Creating a list of player names to keep track of turns
                                     #Might have to change in networked version
                                     
                if self.numPlayers >= 2 and self.numPlayers <= 6:
	                #coins dispersed
	                self.treasury = 50 - 2 * self.numPlayers #50 is starting amt

	                #deck shuffled
	                self.deck.shuffle()

	                #cards dealt
	                for i in range(self.numPlayers):
		                name = raw_input("Player name: ")
                                newPlayer = Player(self.deck.deal(), self.deck.deal())
		                #players.append((name,cards[numCards - 1], cards[numCards - 2], 2))
	                        self.players[name] = newPlayer
                                self.playerList.append(name) #Now each player also has a number
	                        print self.players[name].aboutMe()

                self.currTurn = random.randrange(self.numPlayers) #-1 Needed? Not sure if inclusive
                self.currPlayer = self.playerList[self.currTurn]
                self.active = True
                
        def nextTurn(self):
                if self.currTurn == len(self.playerList) -1:
                        self.currTurn = 0
                else:
                        self.currTurn += 1
                self.currPlayer = self.playerList[self.currTurn]
                
        def checkBluff(self, role):
                caller = raw_input("Does anyone think " + self.currPlayer + " is bluffing?")

                bluffed = False
                if not caller == "no":
                        if role not in self.players[self.currPlayer].cards:
                                print "Bluff Succesfully Called"
                                self.destroyCard(self.currPlayer)
                                bluffed = True
                        else:
                                print caller + " loses a card"
                                self.destroyCard(caller)
                return bluffed

        def destroyCard(self, poorSoul):
                print self.players[poorSoul].aboutMe()
                
                if len(self.players[poorSoul].cards) == 1:
                       self.eliminatePlayer(poorSoul) #Will eliminate player
                else:
                       remove = input("Which to remove(0-1):")
                       self.destroyedCards.append(self.players[name].cards[int(remove)]) 
                       self.players[name].cards.remove(self.players[name].cards[int(remove)])
                       print self.players[name].aboutMe()
                       return
                       
        def eliminatePlayer(self, loser):
                       
                try:
                       self.players.pop(loser)
                except KeyError:
                       print "Player name not found"

                self.playerList.remove(loser)

                if len(self.playerList) == 1:
                       print "YAY " + self.playerList[0] + " has won!"
                       self.active = False
        



print "Welcome to COUP!\n"
cg = CoupGame()





while cg.active:
        print cg.active
        print "It's " + cg.currPlayer + "'s turn."
        response = raw_input(cg.menu)

        #Because response is updated at the end of the loop
        #Any continue statements must be preceeded by a response
        #prompt
        while response != 'q':
                
                
                #Prints out raw statistics of the current game
                if response == 's':
                        for player in cg.players.iterkeys():
                                print player, cg.players[player].aboutMe()
                                cg.deck.fanUp() #Print all cards in deck
                                print "Cards in deck:", cg.deck.numCards
                                print "Treasury: ", cg.treasury
                                
                                #Allows for Ambassador ability
                elif response == 'e':
                        name = cg.currPlayer
                        print cg.players[name].aboutMe()

                        if not cg.checkBluff("Ambassador"):
                                
                                print "2 cards dealt to", name
                                
                                #Same line twice, not sure if its worth consolidating
                                cg.players[name].draw(cg.deck.deal())
                                cg.players[name].draw(cg.deck.deal())
                                
                                cg.players[name].lookAtHand()
                                #print cards[numCards - 1], cards[numCards - 2]
                                
                                #This will enforce handsizes. This is the only time someone's
                                #hand should be bigger than 2
                                
                                to_deck = raw_input("which card will you discard first? (0-3): ")
                                cg.deck.addCard(cg.players[name].cards[int(to_deck)])
                                cg.players[name].cards.remove(cg.players[name].cards[int(to_deck)])
                                
                                cg.players[name].lookAtHand()
                                
                                to_deck = raw_input("which card will you discard second? (0-2): ")
                                cg.deck.addCard(cg.players[name].cards[int(to_deck)])
                                cg.players[name].cards.remove(cg.players[name].cards[int(to_deck)])
                                
                                
                                
                                cg.deck.shuffle()
                        
                        #Coin counts (without held cards)
                elif response == 't':
                        for player in cg.players.iterkeys():
                                print player, ":", cg.players[player].coins
                                print "Treasury:", treasury
                                
                                #Shuffle option
                elif response == 'h':
                        cg.deck.shuffle()
                        continue #shuffling won't change turns
                
                        #Adjust coin amount of one player
                elif response == 'c':
                        name = raw_input("Player name:")
                        print name, "current coins:", cg.players[name].coins
                        newVal = input("New coin count:")
                        cg.players[name].coins = newVal

                        continue #will eventually remove
                        
                        #Duke ability - Tax
                        
                elif response == 'x':
                        name = cg.currPlayer
                        cg.players[name].coins += 3
                        cg.treasury -= 3
                        
                        #Income
                elif response == 'i':
                        name = cg.currPlayer
                        cg.players[name].coins += 1
                        cg.treasury -= 1
                        
                        #Foreign Aid
                elif response == 'f':
                        name = cg.currPlayer
                        cg.players[name].coins += 2
                        cg.treasury -= 2
                        
                        #Captain Ability - Steal
                elif response == 'l':
                        name1 = cg.currPlayer
                        name2 = raw_input("Target:")
                        cg.players[name1].coins += 2
                        cg.players[name2].coins -= 2
                        
                        #Destruction of a card (Coup or Assassination or failed bluff/challenge)
                elif response == 'a':
                        if cg.players[cg.currPlayer].coins < 3:
                                print "You do not have enough coins for that"
                                
                                response = raw_input("Make your move: ")
                                continue
                        cg.players[cg.currPlayer].coins -= 3
                        name = raw_input("Who are you going to assasinate?")
                        if not cg.checkBluff("Assasin"):
                                cg.destroyCard(name)
                                
                elif response == 'p':
                        if cg.players[cg.currPlayer].coins < 7:
                                print "You do not have enough coins for that"
                                response = raw_input("Make your move: ")
                                continue
                        cg.players[cg.currPlayer].coins -= 7
                        name = raw_input("Who's card are you launching a coup against? ")
                        cg.destroyCard(name)
                elif response == 'o':
                        print cg.menu
                        name = raw_input("Make your move: ")
                        continue #Printing menu won't end turn
                elif response == 'q':
                        cg.active = False
                        print "Quatting with cg.active = ", cg.active
                        break #break the loop

                #At this point game could be inactive due to a winner
                #if so, just end it
                
                if cg.active:
                       cg.nextTurn() #After someone takes a turn, increment
                       print "It's " + cg.currPlayer + "'s turn."
                       response = raw_input("Make your move: ")
                else:
                       break

        #Covers the case where q is the first option chosen
        if response == 'q':
                cg.active = False
