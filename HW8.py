import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ db_filename)
    cur = conn.cursor()
    rest_list=[]
    cur.execute("SELECT name, building, category, rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id JOIN categories ON restaurants.category_id = categories.id")
    this = cur.fetchall()
    for i in this:
        dict ={}
        dict['name'] = i[0]
        dict['category'] = i[2]
        dict['building'] = i[1]
        dict['rating'] = i[3]
        rest_list.append(dict)
    return rest_list
    pass

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(categories.category), categories.category FROM restaurants JOIN categories ON restaurants.category_id = categories.id GROUP BY category")
    this = cur.fetchall()
    dict ={}
    for i in this:
        count = i[0]
        category = i[1]
        dict[category] = count
    num_restaurants = []
    category = []
    for i in dict:
        num_restaurants.append(i)
        category.append(dict[i])
    plt.barh(num_restaurants, category)
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.title("Types of Restaurants on South University Ave")
    plt.show()
    return dict

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    
    dict = {} 
    cur.execute("SELECT id, category FROM categories")
    build = cur.fetchall()
    for i in build:
        cur.execute(f'SELECT AVG(rating) FROM restaurants WHERE restaurants.category_id = {i[0]}')
        dict[str(i[1])] = round(cur.fetchone()[0], 1)

    tup = sorted(dict.items(), key = lambda x:x[1])
    categories = [] 
    ratings = [] 
    for x in tup:
        categories.append(x[0])
        ratings.append(x[1])

    plt.barh(categories, ratings)
    plt.xlabel("Ratings")
    plt.ylabel("Categories")
    plt.title("Average Restaurant Ratings by Category")
    plt.show()
    # print(tup[-1])
    return tup[-1]

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
