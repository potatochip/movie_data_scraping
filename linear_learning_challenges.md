### Challenges


##### Challenge 1

Fit a model to your data. Now you know the coefficients (the beta
values).
Write a python function to simulate outcomes.
(The sigma of the normal noise distribution will be the std deviation
of the residuals.)
For the same observed input variables, simulate the outcome.
Plot the observed data and the simulated data.


##### Challenge 2

Generate (fake) data that is linearly related to log(x).
Basically write an underlying model just like in challenge 1, but
instead of a fitted model, you are making this model up. It is of the
form B0 + B1log(x) + epsilon. You are making up the parameters.
Simulate some data from this model.
Then fit two models to it:
a) quadratic [second degree polynomial]
b) logarithmic [log(x)]
(the second one should fit really well, since it has the same form as
the underlying model!)


##### Challenge 3

Fit a model to your training set. Calculate mean squared error on your
training set. Then calculate it on your test set.
(You can use `sklearn.metrics.mean_squared_error`.)


##### Challenge 4

For one continuous feature (like budget, choose one that strongly
affects the outcome), try polynomial fits from 0th (just constant) to
7th order (highest term x^7). Over the x axis of model degree (8
points), plot:

 * training error
 * test error
 * R squared
 * AIC


##### Challenge 5

Fit a model to only the first 5 of your data points (m=5). Then to
first 10 (m=10). Then to first 15 (m=15). In this manner, keep fitting
until you fit your entire training set. For each step, calculate the
training error and the test error. Plot both (in the same plot) over
m. This is called a learning curve.
