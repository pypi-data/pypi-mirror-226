TRAIN_INPUT = [[30,40],[25,50],[20,30],[5,15],[10,15]] # Temprature min:max
TRAIN_OUTPUT = [0,0,0,1,1] # Wear Jacket: 1,  No need to wear:0
LABEL = {0: "No need to wear jacket", 1: "Wear Jacket"}

from sklearn.linear_model import LinearRegression

predictor = LinearRegression(n_jobs=-1)
predictor.fit(X=TRAIN_INPUT, y=TRAIN_OUTPUT)
X_TEST = [[1,3]]
outcome = predictor.predict(X=X_TEST)
coefficients = predictor.coef_

print('Outcome : {}\nCoefficients : {}'.format(outcome, coefficients))
print("For temprature min,max:{0}".format(X_TEST))
print(LABEL.get(round(outcome[0])))
# for test [[3,9]]
#Outcome : [1.14253612]
#Coefficients : [-0.03467095 -0.0105939 ]

# for test [[17,26]]
#Outcome : [0.47704655]
#Coefficients : [-0.03467095 -0.0105939 ]

# for test [[20,30]]
#Outcome : [0.33065811]
#Coefficients : [-0.03467095 -0.0105939 ]
# for test [5,10]
#Outcome : [1.06260032]
#Coefficients : [-0.03467095 -0.0105939 ]
#For temprature min,max:[[5, 10]]
#Wear Jacket
 
