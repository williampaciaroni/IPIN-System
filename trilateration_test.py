from numpy import power, array, random

""" #Array which contains the three landmarks positions
P = array([[1, 2], [3, 4], [5, 6]])

#Array which contains the distance between each landmark and our supposed position
R = [1, 2, 3]

#Number of trilaterations
repeat = 1000 """

def trilateration(P, R):
    """Implementation of trilateration."""
    if len(R) < 3: return None
    # To avoid division by 0 rotate anchors and measurements
    if abs(P[1,0] - P[0,0]) < 1e-5:
        P[[2,0,1]] = P[[0,1,2]]
        R[2], R[0], R[1] = R[0], R[1], R[2]
    ps = power(P[2, 0], 2) - power(P[1, 0], 2) + \
         power(P[2, 1], 2) - power(P[1, 1], 2)
    pt = power(P[0, 0], 2) - power(P[1, 0], 2) + \
         power(P[0, 1], 2) - power(P[1, 1], 2)
    bs = (P[1, 0] - P[2, 0]) * (P[0, 1] - P[1, 1]) - \
         (P[2, 1] - P[1, 1]) * (P[1, 0] - P[0, 0])
    s = (ps + power(R[1], 2) - power(R[2], 2)) / 2.0
    t = (pt + power(R[1], 2) - power(R[0], 2)) / 2.0
    if bs == 0:
        return None
    try:
        y = (t * (P[1, 0] - P[2, 0]) - s * (P[1, 0] - P[0, 0])) / bs
    except:
        return None
    x = (y * (P[0, 1] - P[1, 1]) - t) / (P[1, 0] - P[0, 0])
    return [x, y]

""" #Print the results to two files, one where error is included in calculations and one where is excluded
results_error = open(r"results_error.txt", "w")
results_no_error = open(r"results_no_error.txt", "w") """

""" #Variable to store the values which will be used to calculate the mean (just for the errors one)
avg = [0, 0]

#Repeat the trilateration n times
for i in range(repeat):
    #Add a randomically generated array which simulates error and sum it to the supposed distances to make them realistic
    R_err = R + random.normal(0, 1, 3)
    
    #Print both results to their corrispondant file, the one with the error is also used to calculate the average
    result = trilateration(P, R_err)
    results_error.write(str(result).replace("[", "").replace("]", "") + "\n")
    results_no_error.write(str(trilateration(P, R)).replace("[", "").replace("]", "") + "\n")
    
    #Add the results values to calculate the final average
    avg += array(result) """

""" #Calculate and print the average
print([x / repeat for x in avg])

#Close the two files after writing
results_error.close()
results_no_error.close() """
