import random
import time

random.seed(time.clock())

drinks = {
    "Hot":["Tea","Coffee","Herbal Tea","Mint Tea", "Green Tea", "Hot Choc", "Mocha", "Chai Latte", "Dirty Chai", "Decaf Coffee"], 
    "Cold":["Iced Tea","Iced Coffee","Iced Herbal Tea", "Iced Black Tea", "Iced Chai Latte", "Iced Peach Tea", "Iced Mocha", "Flavored Frap", "Coffee Frap", "Iced Choc"], 
    "Coffee":["Iced Coffee","Coffee", "Mocha", "Dirty Chai", "Iced Mocha", "Coffee Frap", "Decaf Coffee"], 
    "Tea":["Tea","Iced Tea","Herbal Tea","Iced Herbal Tea","Mint Tea", "Green Tea", "Iced Green Tea", "Iced Peach Tea", "Black Tea", "Iced Black Tea"], 
    "Decaf":["Mint Tea","Iced Herbal Tea","Herbal Tea","Mint Tea", "Chai Latte", "Iced Chai Latte", "Iced Choc", "Hot Choc", "Iced Peach Tea"], 
    "Caff.":["Tea","Iced Tea","Iced Green Tea", "Iced Black Tea", "Dirty Chai", "Iced Dirty Chai", "Flavored Frap", "Coffee","Iced Coffee", "Coffee Frap", "Mocha", "Iced Mocha"],
    "Flavor":["Hot Choc", "Chai Latte", "Dirty Chai", "Iced Chai Latte", "Iced Peach Tea", "Iced Mocha", "Mocha", "Flavored Frap", "Mint Tea", "Iced Green Tea", "Iced Black Tea"],
    "Plain":["Coffee Frap", "Iced Coffee", "Coffee", "Tea", "Iced Tea", "Iced Green Tea"]
    }
    
def your_order(answers):
    drink_result = []
    for answer in answers:
        drink_result.append(drinks[answer])

    drink_result = set.intersection(*map(set,drink_result))

    return random.choice((list((drink_result))))
