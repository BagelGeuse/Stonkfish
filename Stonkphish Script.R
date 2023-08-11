closing_price <- read.table("C:/Users/Lex/Desktop/R.test.txt", sep = ",")
close1 <- as.matrix(closing_price[, 1:9])
close2 <- as.matrix(closing_price[, 2:10])
# Grabs stock closing price and locates the data I want to focus on.

close_difM <- close1 - close2
# Calculates the rate of change of stock price.

close_difV <- c(close_difM) # Turns a matrix into a vector
dayV <- as.numeric(c(1:9)) # Creates a vector with integers 1 through 9
close_dif_day <- as.data.frame(cbind(dayV = dayV, close_difV = close_difV))
# Combines and properly formats the change in closing price and which day the change happened into one matrix.

plot(close_dif_day , xlab = "days ago", ylab = "Change in price")
# Gives me visual confirmation the code is doing what I expect so far.

Model <- nls(close_difV ~ a * I(dayV^2)+b * dayV + c, data = close_dif_day, start = list(a = 0, b = 0, c = 0))
# Calculates a quadratic function that best fits my data.

plot(residuals(Model))
# Provides visual confirmation the function created is accurate.

summary(Model)
# Displays necessary data relating to the quadratic function.
ccoeff <-  coef(Model)["c"]
print(ccoeff)
se_c <- coef(summary(Model))["c", "Std. Error"]
print(se_c)

cum_prob <- 1 - pnorm( (0 - ccoeff) / se_c)

