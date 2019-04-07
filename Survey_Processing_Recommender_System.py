import pandas as pd
from rake_nltk import Rake
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# finding the first location that contains the inputed tag
#needs the indexing to be numbers not name so use before (data = data.set_index('name'))
def find_business(tag, data):
    wanted_business = data.iloc[0]
    #3 in data.iloc[0,3] is the number of the column of categories
    r = data.iloc[0,3]
    if r.find(tag) != -1:
        wanted_business = data.iloc[0]
        print (wanted_business['name'])
    else:
        i = 1
        while i < data.size:
            r = data.iloc[i,3]
            if r.find(tag) != -1:
                wanted_business = data.iloc[i]
                print (wanted_business['name'])
                break
            if i == data.size - 1:
                print ('N/a')
            i += 1

#top 100 recommended locations similar to the inputed location
#needs the indexing to be names (data = data.set_index('name'))
def top100(title, data):
    count = CountVectorizer()
    count_matrix = count.fit_transform(data['categories'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    indices = pd.Series(data.index)
    recommended_places = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
    top_100_indexes = list(score_series.iloc[1:100].index)
    for i in top_100_indexes:
        recommended_places.append(list(data.index)[i])
    return recommended_places

#Creating the final list
def final_list(list1,num1,list2,num2,list3,num3,list4,num4,list5,num5):
    final_list = []
    list_of_lists = [list1,list2,list3,list4,list5]
    numbers_of_lists = [num1,num2,num3,num4,num5]
    # top3_lists_locations = []
    #numbers_of_lists_2 = [num1,num2,num3,num4,num5]
    quater_of_numbers_list = [round(num1/4),round(num2/4),round(num3/4),round(num4/4),round(num5/4)]

    # #getting top 3 favorite lists locations
    # i = 0
    # while i < 3:
    #     j = 0
    #     max = numbers_of_lists_2[0]
    #     max_location = 0
    #     while j < len(numbers_of_lists):
    #         if max < numbers_of_lists_2[j]:
    #             max = numbers_of_lists_2[j]
    #             max_location = j
    #         if j == (len(numbers_of_lists) - 1):
    #             numbers_of_lists_2[max_location] = -1
    #             top3_lists_locations.append(max_location)
    #         j += 1
    #     i += 1

    #getting the final list
    c = 0
    list_of_locations = []
    j = 0
    even_num_list = []
    even_list_of_lists = []

    for i in numbers_of_lists:
        if i > 15:
            list_of_locations.append(j)
        j += 1

    for i in list_of_locations:
        num = quater_of_numbers_list[i]
        even_num_list.append(num)

    for i in list_of_locations:
        l = list_of_lists[i]
        even_list_of_lists.append(l)

    while c < 4:
        if c % 2 == 0:
            flag = True
            clone_even_num_list = even_num_list
            while flag:
                count = 0
                flag_counter = 0
                while count < len(clone_even_num_list):
                    if clone_even_num_list[count] == 0:
                        flag_counter += 1
                        count += 1
                    else:
                        flag_counter = 0
                        current_list = even_list_of_lists[count]
                        final_list.append(current_list.pop(0))
                        even_list_of_lists[count] = current_list
                        clone_even_num_list[count] = clone_even_num_list[count] - 1
                        count += 1
                    if flag_counter >= len(clone_even_num_list):
                        flag = False

        else:
            flag = True
            clone_quarter_of_numbers_list = quater_of_numbers_list
            while flag:
                count = 0
                flag_counter = 0
                while count < len(clone_quarter_of_numbers_list):
                    if clone_quarter_of_numbers_list[count] == 0:
                        flag_counter += 1
                        count += 1
                    else:
                        flag_counter = 0
                        current_list = list_of_lists[count]
                        final_list.append(current_list.pop(0))
                        list_of_lists[count] = current_list
                        clone_quarter_of_numbers_list[count] = clone_quarter_of_numbers_list[count] - 1
                        count += 1
                    if flag_counter >= len(clone_quarter_of_numbers_list):
                        flag = False



    return final_list

#importing the dataset and cleaning it from null value
df = pd.read_csv("yelp_business.csv")
data = df[["business_id", "name", "city", "categories"]]
data = data.fillna("Giza")
data = data.sample(frac=0.01, replace=True)
data = data.set_index('name')

#preparing the values that will be inputed in the final list function
def recommendations(books, crafts, culture, food, outdoor,data = data):
    final_recommendation = []
    tag1 = 'Books'
    tag2 = 'Crafts'
    tag3 = 'Arts'
    tag4 = 'Restaurant'
    tag5 = 'Active life'
    book_store = find_business(tag1, data)
    crafts_store = find_business(tag2, data)
    cultural_center = find_business(tag3, data)
    restaurant = find_business(tag4, data)
    travel = find_business(tag5, data)
    book_stores_list = top100(book_store)
    crafts_stores_list = top100(crafts_store)
    cultural_centers_list = top100(cultural_center)
    restaurants_list = top100(restaurant)
    travel_list = top100(travel)
    total_ratings = books + crafts + culture + food + outdoor
    number_of_book_stores = round((books / total_ratings)*100)
    number_of_crafts = round((crafts / total_ratings)*100)
    number_of_cultural_center = round((culture / total_ratings)*100)
    number_of_restaurants = round((food / total_ratings)*100)
    number_of_activities = round((travel / total_ratings)*100)



