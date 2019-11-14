"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    "*** YOUR CODE HERE ***"
    return min(centroids, key=lambda centroid: distance(location, centroid))
    #returns element of list evaluated by key loops through the function in keyes
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)  # Values from pairs that start with 1, 3, and 2 respectively
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]

def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. Each item in
    restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.
    """
    # BEGIN Question 4
    "*** YOUR CODE HERE ***"
    # END Question 4
    pairs = []
    for r in restaurants:
        pairs += [[find_closest(restaurant_location(r), centroids), r]]

    return group_by_first(pairs) #returns a list of clusters

def find_centroid(cluster): #takes in one cluster of a list of clusters
    """Return the centroid of the locations of the restaurants in cluster."""
    # BEGIN Question 5
    "*** YOUR CODE HERE ***"
    restaurant_lat, restaurant_long = [], []
    for c in cluster:

        restaurant_lat += [restaurant_location(c)[0]]
        restaurant_long += [restaurant_location(c)[1]]

    return [mean(restaurant_lat), mean(restaurant_long)]
    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0

    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        "*** YOUR CODE HERE ***"
        centroids = []
        restaurant_clusters = group_by_centroid(restaurants, old_centroids) #gives a list of clusters

        for cluster in restaurant_clusters: #adds the true centroid to the centroids list
            centroids += [find_centroid(cluster)] #needed brackets
            #was adding [lat,long] + [centroid] which gives [lat,long,lat,long]
            #instead of [[lat,long],[lat,long]]
        # END Question 6
        n += 1
    return centroids


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    xs = [feature_fn(r) for r in restaurants] #the extracted feature value for each restaurant in restaurants
    ys = [user_rating(user, restaurant_name(r)) for r in restaurants] #user's ratings for the restaurants in restaurants

    # BEGIN Question 7
    "*** YOUR CODE HERE ***"
    feature_mean = mean(xs)
    rating_mean = mean(ys)
    pair_x_y = zip(xs, ys) #pairs [r1_feature, r1_user_rating]

    S_xy = sum([(pair[0] - feature_mean) * (pair[1] - rating_mean) for pair in pair_x_y])
    S_xx = sum([pow(x - feature_mean,2) for x in xs])
    S_yy = sum([pow(y - rating_mean,2) for y in ys])

    b = S_xy / S_xx
    a = rating_mean - b * feature_mean
    r_squared = pow(S_xy, 2) / (S_xx * S_yy)
    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared #returns a tuple (predictor, r_squared)


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predictor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants) #a sub-list of restaurants
    # BEGIN Question 8
    "*** YOUR CODE HERE ***"
    predictor_list = [find_predictor(user, reviewed, f) for f in feature_fns]
    #returns a list of tuples
    return (max(predictor_list, key=lambda x: x[1])[0])
    #returns tuple with max value at index one, then returns first element of that
    #tuple which is a function
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns) #best_pred func
    reviewed = user_reviewed_restaurants(user, restaurants) #list of restaurants

    # BEGIN Question 9
    "*** YOUR CODE HERE ***"
    complete_dictionary = []

    for r in restaurants:
        if r not in reviewed:
            complete_dictionary += [[restaurant_name(r), predictor(r)]] #[[name,pred], [name,pred]]
        else:
            complete_dictionary += [[restaurant_name(r), user_rating(user, restaurant_name(r))]]
            #not enough brackets again

    return dict(complete_dictionary)
    # END Question 9


def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    "*** YOUR CODE HERE ***"
    return [x for x in restaurants if query in restaurant_categories(x)]

    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [lambda r: mean(restaurant_ratings(r)),
            restaurant_price,
            lambda r: len(restaurant_ratings(r)),
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)
