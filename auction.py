import csv
import sys
import random

max_bidders=10

def main():
    print("-- AUCTION SIMULATOR --")

    bidder_amount=get_valid_int("How many bidders? ", min_number=2, max_number=max_bidders)
    max_valuation=get_valid_int("Max valuation? ", min_number=0, max_number=None)
    number_of_simulations=get_valid_int("How many simulations? ", min_number=0, max_number=None)

    print("Auction Types: \n1 - English\n2 - Dutch\n3 - First-price sealed bid\n4- Vickrey")
    auction_type = input("Choose auction type (1-4): ")
    if auction_type.isdigit():
        auction_input=int(auction_type)
        if 1<=auction_input<=4:
            if auction_input == 1:
                english_auction(bidder_amount, max_valuation, number_of_simulations)
            elif auction_input == 2:
                dutch_auction(bidder_amount, max_valuation, number_of_simulations)
            elif auction_input == 3:
                first_price_auction(bidder_amount, max_valuation, number_of_simulations)
            elif auction_input == 4:
                vickrey_auction(bidder_amount, max_valuation, number_of_simulations)
        else: print("Invalid auction type! Please select a value 1-4")
    else:
        print("Invalid auction type! Please select an integer value 1-4")
        return False

def english_auction(number_of_bidders, max_value, number_of_simulations):
    print("-- ENGLISH AUCTION --")
    auction_type="English"
    start_price=get_valid_int("Enter starting price: ", min_number=0, max_number=max_value-1)
    increment=get_valid_int("Enter minimum bid increment: ", min_number=1, max_number=None)

    sims_completed=0
    efficiency=0
    highest_bidder_wins=0
    revenue=0
    while sims_completed<number_of_simulations:
        active_bidders, initial_valuations= generate_valuations(number_of_bidders, max_value)

        print("\nInitial bidder valuations (hidden in real auction): ", initial_valuations)

        round_number = 1
        current_price = start_price
        last_price=current_price
        while len(active_bidders)>1:
            print(f"\nRound {round_number}, Current Price: {current_price}")
            for bidder in active_bidders[:]:
                if initial_valuations[bidder] < current_price:
                    active_bidders.remove(bidder)
                    print(f"\nBidder {bidder} was removed")
                    print(f"{len(active_bidders)} bidders left")
                if len(active_bidders) <= 1:
                    break
            if len(active_bidders) == 0:
                print("All bidders dropped out. No winner this simulation.")
                sims_completed += 1
                continue
            round_number+=1
            last_price = current_price
            current_price += increment
        winner = active_bidders[0]
        winning_price = last_price
        print(f"\nBidder {winner} won with a bid of {winning_price}")

        max_valuation = max(initial_valuations.values())
        if initial_valuations[winner]==max_valuation:
            highest_bidder_wins+=1
        efficiency+=initial_valuations[winner]/max_valuation
        sims_completed+=1
        revenue+=winning_price
    calculate_results(revenue, number_of_simulations, efficiency, auction_type, highest_bidder_wins)

def dutch_auction(number_of_bidders, max_value, number_of_simulations):
    print("-- DUTCH AUCTION --")
    auction_type="Dutch"
    start_price = get_valid_int("Enter starting price: ", min_number=max_value, max_number=None)
    decrement=get_valid_int("Enter minimum bid decrement: ", min_number=1, max_number=None)

    sims_completed=0
    efficiency=0
    highest_bidder_wins=0
    revenue=0
    while sims_completed<number_of_simulations:
        active_bidders, initial_valuations= generate_valuations(number_of_bidders, max_value)

        round_number = 1
        current_price = start_price
        winner=-1
        while winner==-1:
            print(f"\nRound {round_number}, Current Price: {current_price}")
            for bidder in active_bidders:
                if initial_valuations[bidder]>=current_price:
                    winner = bidder
                    winning_price=current_price
                    break
            round_number+=1
            current_price-=decrement
        max_valuation =max(initial_valuations.values())
        print(f"\nBidder {winner} won with a bid of {winning_price}")
        revenue += winning_price
        if initial_valuations[winner]==max_valuation:
            highest_bidder_wins+=1
        efficiency+=initial_valuations[winner]/max_valuation
        sims_completed+=1

    calculate_results(revenue, number_of_simulations, efficiency, auction_type, highest_bidder_wins)

def first_price_auction(number_of_bidders, max_value, number_of_simulations):
    print("\n-- FIRST-PRICE SEALED BID AUCTION --")
    auction_type="First-Price Sealed Bid"

    sims_completed=0
    efficiency=0
    highest_bidder_wins=0
    revenue=0

    while sims_completed<number_of_simulations:
        active_bidders, initial_valuations= generate_valuations(number_of_bidders, max_value)
        max_valuation =max(initial_valuations.values())
        for j in range(len(initial_valuations)):
            if initial_valuations[j]==max_valuation:
                winner=j
        revenue+=max_valuation
        efficiency+=initial_valuations[winner]/max_valuation
        if initial_valuations[winner]==max_valuation:
            highest_bidder_wins+=1

        print(f"\nBidder {winner} won with a bid of {max_valuation}. They pay {max_valuation}")
        sims_completed+=1

    calculate_results(revenue, number_of_simulations, efficiency, auction_type, highest_bidder_wins)

def vickrey_auction(number_of_bidders, max_value, number_of_simulations):
    print("\n-- VICKREY BID AUCTION --")
    auction_type="Vickrey"

    sims_completed=0
    efficiency=0
    highest_bidder_wins=0
    revenue=0

    while sims_completed<number_of_simulations:
        active_bidders, initial_valuations= generate_valuations(number_of_bidders, max_value)
        max_valuation =max(initial_valuations.values())
        for j in range(len(initial_valuations)):
            if initial_valuations[j]==max_valuation:
                winner=j
        sorted_initial_valuations = sorted(initial_valuations.items(), key=lambda item: item[1],reverse=True)
        second_valuation = sorted_initial_valuations[1]
        print(f"Bidder {winner} won with a bid of {max_valuation}. They pay {second_valuation[1]}")
        sims_completed+=1

        revenue+=second_valuation[1]
        efficiency+=initial_valuations[winner]/max_valuation
        if initial_valuations[winner]==max_valuation:
            highest_bidder_wins+=1

    calculate_results(revenue, number_of_simulations, efficiency, auction_type, highest_bidder_wins)

def show_results(auction_type, number_of_simulations, average_winning_price, efficiency, highest_bidder_win):
    show_stats = input("\nShow stats (y/n)? ")
    if show_stats=="y":
        print(f"\nAuction type: {auction_type}\nSimulations run: {number_of_simulations}\n\nAverage winning price: {average_winning_price}\nEfficiency (Does the item goes to the bidder who values it most?): {efficiency}%\nHighest valuation bidder won {highest_bidder_win}% of auctions")
    elif show_stats=="n":
        return False
    else:
        print("Invalid! Please type 'y' or 'n'")


def get_valid_int(prompt, min_number=None, max_number=None):
    value=input(prompt)
    if not value.isdigit():
        print("Invalid! Must be a positive whole number.")
        sys.exit()
    else:
        value=int(value)
    if min_number is not None and value < min_number:
        print(f"Value must be greater than {min_number}")
        sys.exit()
    if max_number is not None and value > max_number:
        print(f"Value must be less than {max_number}")
        sys.exit()
    return value

def generate_valuations(number_of_bidders, max_value):
    active_bidders = []
    initial_valuations = dict()
    for i in range(number_of_bidders):
        active_bidders.append(i)
        initial_valuations[i] = random.randint(0, max_value)
    return active_bidders, initial_valuations

def calculate_results(revenue, number_of_simulations, efficiency, auction_type, highest_bidder_wins):
    average_winning_price= round((revenue/number_of_simulations), 2)
    efficiency = round(((efficiency/number_of_simulations)*100), 2)
    average_highest_bidder_wins = round(100*(highest_bidder_wins/number_of_simulations), 2)
    show_results(auction_type, number_of_simulations, average_winning_price, efficiency, average_highest_bidder_wins)


if __name__=="__main__":
    main()


