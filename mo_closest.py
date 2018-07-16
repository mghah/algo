#Uses python3
import sys
import math
import statistics as stats

# helper functions:

# helper functions:
def two_point_distance(p0,p1):
    # returns distance between two (x,y) pairs
    return math.sqrt( ((p0[0]-p1[0])*(p0[0]-p1[0])) + 
                     ((p0[1] - p1[1])*(p0[1] - p1[1])) )

def combine_xy(x_arr,y_arr):
    # combine x_arr and y_arr to combined list of (x,y) tuples 
    return list(zip(x_arr,y_arr))

def find_closest_distance_brute(xy_arr):
    # brute force approach to find closest distance 
    dmin = math.inf
    for i, pnt_i in enumerate(xy_arr[:-1]):      
        dis_storage_min = min( two_point_distance(pnt_i, pnt_j) for pnt_j in xy_arr[i+1:])      
        if dis_storage_min < dmin:
            dmin = dis_storage_min  
    return dmin

def calc_median_x(xy_arr):
    # return median of x values in list of (x,y) points
    return stats.median( val[0] for val in xy_arr )
    
def filter_set(xy_arr_y_sorted, median, distance):
# filter initial set such than |x-med|<=d
    return [ val for val in xy_arr_y_sorted if abs(val[0] - median) <= distance ]

def x_sort(xy_arr):
    # sort array according to x value
    return sorted(xy_arr, key=lambda val: val[0])

def y_sort(xy_arr):
    # sort array according to y value
    return sorted(xy_arr, key=lambda val: val[1])


def split_array(arr_x_sorted, arr_y_sorted,median):
    # split array of size n to two arrays of n/2
    # input is the same array twice, one sorted wrt x, the other wrt y
    leq_arr_x_sorted = [ val for val in arr_x_sorted if val[0] < median ]
    geq_arr_x_sorted = [ val for val in arr_x_sorted if val[0] > median ]
    eq_arr_x        = [ val for val in arr_x_sorted if val[0] == median ]
   
    n = len(eq_arr_x)//2
    leq_arr_x_sorted = leq_arr_x_sorted + eq_arr_x[:n]
    geq_arr_x_sorted = eq_arr_x[n:] + geq_arr_x_sorted
   
    leq_arr_y_sorted = [ val for val in arr_y_sorted if val[0] < median ]
    geq_arr_y_sorted = [ val for val in arr_y_sorted if val[0] > median ]
    eq_arr_y        = [ val for val in arr_y_sorted if val[0] == median ]
   
    n = len(eq_arr_y)//2
    leq_arr_y_sorted = leq_arr_y_sorted + eq_arr_y[:n]
    geq_arr_y_sorted = eq_arr_y[n:] + geq_arr_y_sorted
    

    return leq_arr_x_sorted, leq_arr_y_sorted, geq_arr_x_sorted, geq_arr_y_sorted

def find_min_distance_in_rec(xy_arr_y_sorted,dmin):
    # takes in array sorted in y, and minimum distance of n/2 halves
    # for each point it computes distance to 7 subsequent points
    # output min distance encountered
    
    dmin_rec = dmin
    
    if len(xy_arr_y_sorted) == 1:
        return math.inf
    
    if len(xy_arr_y_sorted) > 7:       
        for i, pnt_i in enumerate(xy_arr_y_sorted[:-7]):
            dis_storage_min = min(two_point_distance(pnt_i, pnt_j) 
                                 for pnt_j in xy_arr_y_sorted[i+1:i+1+7])
            if dis_storage_min < dmin_rec:
                dmin_rec = dis_storage_min
                
        dis_storage_min = find_closest_distance_brute(xy_arr_y_sorted[-7:])
        if dis_storage_min < dmin_rec:
            dmin_rec = dis_storage_min
    else:
        for k, pnt_k in enumerate(xy_arr_y_sorted[:-1]):      
            dis_storage_min = min( two_point_distance(pnt_k, pnt_l) for pnt_l in xy_arr_y_sorted[k+1:])      
            if dis_storage_min < dmin_rec:
                dmin_rec = dis_storage_min 
    
    return dmin_rec             

def find_closest_distance_recur(xy_arr_x_sorted, xy_arr_y_sorted):
    # recursive function to find closest distance between points
    if len(xy_arr_x_sorted) <=3 :
        return find_closest_distance_brute(xy_arr_x_sorted)
    
    median = calc_median_x(xy_arr_x_sorted)
    leq_arr_x_sorted, leq_arr_y_sorted , grt_arr_x_sorted, grt_arr_y_sorted = split_array(xy_arr_x_sorted, xy_arr_y_sorted, median)
    
    distance_left = find_closest_distance_recur(leq_arr_x_sorted, leq_arr_y_sorted)
    distance_right = find_closest_distance_recur(grt_arr_x_sorted, grt_arr_y_sorted)
    distance_min = min(distance_left, distance_right)
    
    filt_out = filter_set(xy_arr_y_sorted, median, distance_min)
    distance_filt = find_min_distance_in_rec(filt_out, distance_min)
    
    return min(distance_min, distance_filt)

def find_closest_point(x_arr, y_arr):
    # input is x,y points in two arrays, all x's in x_arr, all y's in y_arr
    xy_arr = combine_xy(x_arr,y_arr)
    xy_arr_x_sorted = x_sort(xy_arr)
    xy_arr_y_sored = y_sort(xy_arr)
    
    min_distance = find_closest_distance_recur(xy_arr_x_sorted, xy_arr_y_sored)
    
    return min_distance

def minimum_distance(x, y):
    #write your code here
    return find_closest_point(x,y)
  
def test_minimum_distance():
    # correct answer is sqrt(2)
    x_arr = [4,-2,-3,-1,2,-4,1,-1,3,-4,-2]
    y_arr = [4,-2,-4,3,3,0,1,-1,-1,2,4]
    print ('combined array', combine_xy(x_arr, y_arr))
    print ('closest distance' , minimum_distance(x_arr, y_arr))
    return None
test_minimum_distance()
