import tkinter as tk
import random
from tkinter.messagebox import *

end_of_game, stop, first_time = False, False, True  # definition of global variables
size, dealer_y, player_y, sum_x_delta, sum_y_delta, delta, first_card_coord_x = 7, 10, 270, -70, 20, 30, 330
bet, balance, additional_cards_player, additional_cards_dealer = 0, 1000, 0, 1
sum_dealer, sum_player, dealer_hand, player_hand, = [], [], [], []
commands = [['Stand on it        ', 0], ['Additional card', 1]]
precnt, dealer, player, bg_color, empty_string = "precounted_dealer", "dealer", "player", "#175724", "               "
deck = ['D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'H2', 'H3', 'H4', 'H5', 'H6',
        'H7', 'H8', 'H9', 'H10', 'H11', 'H12', 'H13', 'H14', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10',
        'S11',
        'S12', 'S13', 'S14', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14'] * 4
deck_default = deck

root = tk.Tk()  # window settings
root.title('Blackjack ONLINE')
root.geometry('900x400+150+150')
root.resizable(False, False)
root.configure(background=bg_color)


def restart():  # this function is called when button "New game" has been clicked. It mainly calls handout() function
    global first_time, balance, bet
    flag = 1
    bet_local = entry.get()
    for i in bet_local:
        if not i.isnumeric():
            flag = 0
    if bet_local and flag and 1 <= int(bet_local) <= balance:
        bet = int(bet_local)
        balance -= bet
        if first_time or end_of_game and stop:
            first_time = False
            handout()
    else:
        tk.Label(root, text='Balance', bg=bg_color).place(x=10, y=70)
        tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
        tk.Label(root, text='Bet', bg=bg_color).place(x=90, y=70)
        showerror(message='You are trying to fool me!')


def additional_card_dealer():  # this function is called when the dealer has to take another card
    global stop, additional_cards_dealer, balance
    if end_of_game and not stop:
        additional_cards_dealer += 1
        dealer_hand.append(pick_card())
        show_sum(dealer)
        ph = tk.PhotoImage(file='img/' + dealer_hand[-1] + '.png').subsample(size, size)
        tk.Label(root, image=ph).place(x=first_card_coord_x + additional_cards_dealer * delta, y=dealer_y)
        if sum_dealer[-1] > 21:
            showinfo(message='You won')
            balance += 2 * bet
            tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
            stop = True
        elif sum_dealer[-1] >= 17:
            if sum_dealer[-1] > sum_player[-1]:
                showerror(message='You lost')
                stop = True
            elif sum_dealer[-1] == sum_player[-1]:
                showinfo(message='Draw')
                balance += bet
                tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
                stop = True
            else:
                showinfo(message='You won')
                balance += 2 * bet
                tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
                stop = True
        elif sum_dealer[-1] > sum_player[-1]:
            showerror(message='You lost')
            stop = True
        root.mainloop()


def show_sum(name: str):  # this function is capable of showing the sum of the hand (both player and dealer)
    global sum_dealer, sum_player
    num_of_aces, sum = 0, 0
    if name == dealer or name == precnt:
        sum_dealer = []
        for i in dealer_hand:
            val = int(i[1:])
            if val <= 10:
                sum += val
            elif val == 14:
                sum += 11
                num_of_aces += 1
            else:
                sum += 10
        for i in range(num_of_aces, -1, -1):
            if sum - 10 * i <= 21:
                sum_dealer.append(sum - 10 * i)
        if not sum_dealer:
            sum_dealer.append(sum - 10 * num_of_aces)
        if name == dealer:
            tk.Label(root, text=empty_string, bg=bg_color).place(x=first_card_coord_x + sum_x_delta,
                                                                 y=dealer_y + sum_y_delta)
            if len(sum_dealer) > 1 and sum_dealer[-1] <= 21:
                tk.Label(root, text=str(sum_dealer[-1]), bg=bg_color).place(x=first_card_coord_x + sum_x_delta,
                                                                            y=dealer_y + sum_y_delta)
            else:
                tk.Label(root, text=str(sum_dealer[0]), bg=bg_color).place(x=first_card_coord_x + sum_x_delta,
                                                                           y=dealer_y + sum_y_delta)
    if name == player:
        sum_player = []
        for i in player_hand:
            val = int(i[1:])
            if val <= 10:
                sum += val
            elif val == 14:
                sum += 11
                num_of_aces += 1
            else:
                sum += 10
        for i in range(num_of_aces, -1, -1):
            if sum - 10 * i <= 21:
                sum_player.append(sum - 10 * i)
        if not sum_player:
            sum_player.append(sum - 10 * num_of_aces)
        tk.Label(root, text=empty_string, bg=bg_color).place(x=first_card_coord_x + sum_x_delta,
                                                             y=player_y + sum_y_delta)
        if len(sum_player) > 1 and sum_player[-1] <= 21:
            tk.Label(root, text=str(sum_player[0]) + ' or ' + str(sum_player[1]), bg=bg_color).place(
                x=first_card_coord_x + sum_x_delta, y=player_y + sum_y_delta)
        else:
            tk.Label(root, text=str(sum_player[0]), bg=bg_color).place(x=first_card_coord_x + sum_x_delta,
                                                                       y=player_y + sum_y_delta)


def show_up_dealer():  # this funtion is called when the player stands on his cards, so dealer has to show his hand
    global stop, balance
    show_sum(dealer)
    if sum_player[-1] > 21 or sum_player[-1] < sum_dealer[-1]:
        showerror(message='You lost')
        stop = True
    elif sum_player[-1] == sum_dealer[-1] and sum_player[-1] >= 17:
        showinfo(message='Draw')
        balance += bet
        tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
        stop = True
    elif sum_player[-1] > sum_dealer[-1] >= 17:
        showinfo(message='You won')
        balance += 2 * bet
        tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
        stop = True
    root.mainloop()


def pick_card():  # function for picking new card
    card = random.choice(deck)
    deck.remove(card)
    return card


def additional_card_player():  # function for adding player additional card, if he asks so
    global end_of_game, stop
    if not end_of_game:
        global additional_cards_player
        additional_cards_player += 1
        player_hand.append(pick_card())
        photo = tk.PhotoImage(file='img/' + player_hand[-1] + '.png').subsample(size, size)
        tk.Label(root, image=photo).place(x=first_card_coord_x + (additional_cards_player + 1) * delta, y=player_y)
        show_sum(player)
        if sum_player[0] > 21:
            showerror(message='You lost')
            stop, end_of_game = True, True
        root.mainloop()


def players_choice():  # this function processes the radio buttons
    global end_of_game
    if not end_of_game:
        m = str(comm.get())
        if m == '0':
            end_of_game = True
            photo = tk.PhotoImage(file='img/' + dealer_hand[1] + '.png').subsample(size, size)
            tk.Label(root, image=photo).place(x=first_card_coord_x + delta, y=dealer_y)
            show_up_dealer()
        else:
            if sum_player[0] < 21:
                additional_card_player()
            else:
                show_up_dealer()


def handout():  # this function is used to clear the previous table, to recharge the deck (if necessary), to give 2 starting cards to the player and 2 starting cards to the dealer
    global dealer_hand, player_hand, sum_player, sum_dealer, additional_cards_dealer, additional_cards_player, stop, end_of_game, deck
    stop, end_of_game = False, False
    additional_cards_player, additional_cards_dealer = 0, 1
    dealer_hand, player_hand, sum_player, sum_dealer = [], [], [], []

    if len(deck) < 70:
        deck = deck_default
    dealer_hand.append(pick_card())
    dealer_hand.append(pick_card())
    player_hand.append(pick_card())
    player_hand.append(pick_card())
    for widget in root.winfo_children():
        if type(widget) == tk.Label:
            widget.destroy()

    upcoming_card = tk.PhotoImage(file='img/unknown.png').subsample(size, size)
    tk.Label(root, image=upcoming_card).place(x=10, y=160)
    tk.Label(root, image=upcoming_card).place(x=17, y=160)
    tk.Label(root, image=upcoming_card).place(x=24, y=160)
    tk.Label(root, image=upcoming_card).place(x=31, y=160)
    tk.Label(root, image=upcoming_card).place(x=38, y=160)

    photo1 = tk.PhotoImage(file='img/' + dealer_hand[0] + '.png').subsample(size, size)
    tk.Label(root, image=photo1).place(x=first_card_coord_x, y=dealer_y)
    photo2 = tk.PhotoImage(file='img/unknown.png').subsample(size, size)
    tk.Label(root, image=photo2).place(x=first_card_coord_x + delta, y=dealer_y)
    photo3 = tk.PhotoImage(file='img/' + player_hand[0] + '.png').subsample(size, size)
    tk.Label(root, image=photo3).place(x=first_card_coord_x, y=player_y)
    photo4 = tk.PhotoImage(file='img/' + player_hand[1] + '.png').subsample(size, size)
    tk.Label(root, image=photo4).place(x=first_card_coord_x + delta, y=player_y)
    tk.Label(root, text='Balance', bg=bg_color).place(x=10, y=70)
    tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
    tk.Label(root, text='Bet', bg=bg_color).place(x=90, y=70)
    show_sum(player)
    show_sum(precnt)
    root.mainloop()


comm = tk.StringVar(value=' ')  # creating default buttons and labels
tk.Radiobutton(root, text=commands[0][0], value=commands[0][1], variable=comm, bg='white').place(x=750, y=173)
tk.Radiobutton(root, text=commands[1][0], value=commands[1][1], variable=comm, bg='white').place(x=750, y=200)
tk.Button(root, text="Confirm", command=players_choice, bg='white').place(x=750, y=240)
tk.Button(root, text="Dealer", command=additional_card_dealer, bg='white').place(x=750, y=20)
tk.Button(root, text="New game", command=restart, bg='white').place(x=20, y=20)
bet_field = tk.StringVar(value=' ')
tk.Label(root, text='Balance', bg=bg_color).place(x=10, y=70)
tk.Label(root, text=balance, bg=bg_color).place(x=10, y=90)
tk.Label(root, text='Bet', bg=bg_color).place(x=90, y=70)
entry = tk.Entry(root, width=10)
entry.place(x=90, y=90)

root.mainloop()
